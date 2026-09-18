"""PixelLab asset pipeline with a resumable manifest (never pays twice for an asset).

Usage:
  PIXELLAB_TOKEN=... python3 tools/pixellab.py run [key ...]   # submit + poll + download
  python3 tools/pixellab.py status

Specs live in tools/pixellab_specs.py. Results:
  characters -> art/chars/<key>/<dir>.png and art/chars/<key>/<anim>/<dir>/<i>.png
  objects    -> art/props/<key>.png
  portraits  -> art/portraits/<key>.png
The manifest (tools/pixellab_manifest.json) stores job/character ids and status.
"""
import base64
import json
import os
import sys
import time
import urllib.request
import urllib.error
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "tools/pixellab_manifest.json"
API = "https://api.pixellab.ai/v2"
TOKEN = os.environ.get("PIXELLAB_TOKEN", "")
DIRS = ["south", "east", "north", "west"]

sys.path.insert(0, str(Path(__file__).parent))
from pixellab_specs import SPECS  # noqa: E402


def log(*a):
    print(time.strftime("%H:%M:%S"), *a, flush=True)


def req(method, path, body=None, retries=4):
    for attempt in range(retries):
        r = urllib.request.Request(API + path, method=method,
                                   headers={"Authorization": "Bearer " + TOKEN, "Content-Type": "application/json"},
                                   data=json.dumps(body).encode() if body is not None else None)
        try:
            with urllib.request.urlopen(r, timeout=180) as resp:
                return json.loads(resp.read() or b"{}")
        except urllib.error.HTTPError as e:
            msg = e.read().decode()[:400]
            if e.code in (429, 500, 502, 503, 504) and attempt < retries - 1:
                log("retry", path, e.code, msg[:120])
                time.sleep(10 * (attempt + 1))
                continue
            raise RuntimeError(f"{method} {path} -> {e.code}: {msg}")
        except (urllib.error.URLError, TimeoutError) as e:
            if attempt < retries - 1:
                time.sleep(10)
                continue
            raise


def fetch(url, dest: Path):
    dest.parent.mkdir(parents=True, exist_ok=True)
    for attempt in range(4):
        try:
            r = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (scp-game asset pipeline)"})
            with urllib.request.urlopen(r, timeout=120) as resp:
                dest.write_bytes(resp.read())
            return
        except Exception:
            time.sleep(5)
    raise RuntimeError("download failed " + url)


def b64file(path: Path):
    return {"type": "base64", "base64": base64.b64encode(path.read_bytes()).decode()}


def load():
    return json.loads(MANIFEST.read_text()) if MANIFEST.exists() else {}


def save(m):
    MANIFEST.write_text(json.dumps(m, indent=1, sort_keys=True))


# ---------------------------------------------------------------- characters

def char_submit(key, spec, st):
    if "character_id" not in st:
        body = {
            "description": spec["desc"],
            "image_size": {"width": spec.get("size", 48), "height": spec.get("size", 48)},
            "view": spec.get("view", "low top-down"),
            "outline": "single color black outline",
            "shading": spec.get("shading", "detailed shading"),
            "detail": spec.get("detail", "high detail"),
        }
        if spec.get("template"):
            body["template_id"] = spec["template"]
        if spec.get("proportions"):
            body["proportions"] = {"type": "preset", "name": spec["proportions"]}
        r = req("POST", "/create-character-with-4-directions", body)
        st["character_id"] = r.get("character_id") or r.get("id")
        log(key, "character submitted", st["character_id"])
    return st


def char_ready(cid):
    d = req("GET", f"/characters/{cid}")
    return d


def char_step(key, spec, st):
    """Advance one character through: created -> animations queued -> downloaded."""
    d = char_ready(st["character_id"])
    if d.get("status") not in ("completed", None) and not d.get("rotation_urls", {}).get("south"):
        return False
    if not d.get("rotation_urls", {}).get("south"):
        return False
    have = {a.get("animation_type") or a.get("display_name") for a in d.get("animations") or []}
    queued = st.setdefault("anims_queued", [])
    for anim in spec.get("anims", []):
        if anim not in have and anim not in queued:
            req("POST", "/characters/animations", {"character_id": st["character_id"],
                "template_animation_id": anim, "animation_name": anim, "directions": DIRS})
            queued.append(anim)
            log(key, "animation queued", anim)
    # done when every requested animation has frames for all 4 directions
    ready = True
    by_name = {}
    for a in d.get("animations") or []:
        name = a.get("display_name") or a.get("animation_type")
        dirs = {x["direction"]: x for x in a.get("directions") or [] if x.get("frames")}
        by_name[name] = dirs
    for anim in spec.get("anims", []):
        if len(by_name.get(anim, {})) < 4:
            ready = False
    if not ready:
        return False
    out = ROOT / "art/chars" / key
    for dname, url in d["rotation_urls"].items():
        if url:
            fetch(url, out / f"{dname}.png")
    for anim, dirs in by_name.items():
        if anim not in spec.get("anims", []):
            continue
        for dname, x in dirs.items():
            for i, url in enumerate(x["frames"]):
                fetch(url, out / anim / dname / f"{i}.png")
    st["done"] = True
    log(key, "character downloaded")
    return True


# ------------------------------------------------------------------- objects

def obj_submit(key, spec, st):
    if "object_id" in st or "image" in st:
        return st
    size = spec.get("size", 32)
    if spec.get("mode") == "pixflux":
        r = req("POST", "/create-image-pixflux", {
            "description": spec["desc"], "image_size": {"width": size, "height": spec.get("h", size)},
            "view": spec.get("view", "low top-down"), "no_background": True,
            "background_removal_task": "remove_simple_background",
            "outline": "single color black outline", "shading": "detailed shading", "detail": "highly detailed"})
        out = ROOT / spec.get("dir", "art/props") / f"{key}.png"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_bytes(base64.b64decode(r["image"]["base64"]))
        st["image"] = str(out.relative_to(ROOT))
        st["done"] = True
        log(key, "pixflux saved")
        return st
    r = req("POST", "/map-objects", {
        "description": spec["desc"], "image_size": {"width": max(32, size), "height": max(32, spec.get("h", size))},
        "view": spec.get("view", "low top-down"), "outline": "single color outline",
        "shading": "detailed shading", "detail": "high detail"})
    st["object_id"] = r.get("object_id") or r.get("id")
    log(key, "map-object submitted", st["object_id"])
    return st


def find_image(d):
    """Return (kind, value) for the first image found in a response: url or base64."""
    if isinstance(d, dict):
        img = d.get("image")
        if isinstance(img, dict) and img.get("base64"):
            return ("b64", img["base64"])
        for k in ("image_url", "url", "download_url"):
            if isinstance(d.get(k), str) and d[k].startswith("http"):
                return ("url", d[k])
        for v in d.values():
            f = find_image(v)
            if f:
                return f
    elif isinstance(d, list):
        for v in d:
            f = find_image(v)
            if f:
                return f
    return None


def obj_step(key, spec, st):
    if st.get("done"):
        return True
    d = req("GET", f"/map-objects/{st['object_id']}")
    status = str(d.get("status", "")).lower()
    if status in ("failed", "error"):
        log(key, "FAILED", str(d)[:200])
        st.pop("object_id")
        return False
    f = find_image(d)
    if not f:
        return False
    out = ROOT / spec.get("dir", "art/props") / f"{key}.png"
    if f[0] == "b64":
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_bytes(base64.b64decode(f[1]))
    else:
        fetch(f[1], out)
    st["done"] = True
    log(key, "object downloaded")
    return True


# ----------------------------------------------------------------- portraits

def portrait_submit(key, spec, st):
    if "job_id" in st:
        return st
    src = ROOT / spec["from"]
    if not src.exists():
        return st  # wait for the character first
    r = req("POST", "/portrait-character-pro", {"direction": "character_to_portrait", "image": b64file(src),
            "view": "low top-down", "result_size": spec.get("size", 64)})
    st["job_id"] = r.get("job_id") or r.get("id") or r.get("background_job_id")
    log(key, "portrait submitted", st["job_id"])
    return st


def portrait_step(key, spec, st):
    if "job_id" not in st:
        return False
    d = req("GET", f"/portrait-character-pro/{st['job_id']}")
    status = str(d.get("status", "")).lower()
    if status in ("failed", "error"):
        log(key, "FAILED", str(d)[:200])
        st.pop("job_id")
        return False
    f = find_image(d)
    if not f:
        return False
    out = ROOT / "art/portraits" / f"{key}.png"
    if f[0] == "b64":
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_bytes(base64.b64decode(f[1]))
    else:
        fetch(f[1], out)
    st["done"] = True
    log(key, "portrait downloaded")
    return True


# ------------------------------------------------------ object batches (Pro)
# One /create-1-direction-object call renders many different small objects in one style:
# size 16 -> up to 64 objects, size 32 -> up to 16. Frame i matches item_descriptions[i].

def batch_submit(key, spec, st):
    if "object_id" in st:
        return st
    names = list(spec["items"].keys())
    r = req("POST", "/create-1-direction-object", {
        "description": spec["desc"], "size": spec["size"], "view": "top-down",
        "item_descriptions": [spec["items"][n] for n in names]})
    st["object_id"] = r.get("object_id")
    st["names"] = names
    log(key, "batch submitted", st["object_id"], len(names), "items")
    return st


def batch_step(key, spec, st):
    d = req("GET", f"/objects/{st['object_id']}")
    urls = d.get("storage_urls") or {}
    if not urls:
        return False
    for i, name in enumerate(st["names"]):
        u = urls.get(f"frame_{i}")
        if u:
            fetch(u, ROOT / spec.get("dir", "art/props") / f"{name}.png")
    st["done"] = True
    log(key, "batch downloaded", len(st["names"]))
    return True


KIND = {"char": (char_submit, char_step), "obj": (obj_submit, obj_step), "portrait": (portrait_submit, portrait_step),
        "batch": (batch_submit, batch_step)}


def run(keys):
    m = load()
    todo = [k for k in (keys or SPECS) if not m.get(k, {}).get("done")]
    log("pending:", len(todo))
    for k in todo:
        spec = SPECS[k]
        try:
            m[k] = KIND[spec["kind"]][0](k, spec, m.get(k, {}))
        except Exception as e:
            log(k, "submit error:", e)
        save(m)
    deadline = time.time() + 3 * 3600
    while time.time() < deadline:
        pending = [k for k in todo if not m.get(k, {}).get("done")]
        if not pending:
            break
        for k in pending:
            spec = SPECS[k]
            try:
                if spec["kind"] == "portrait" and "job_id" not in m.get(k, {}):
                    m[k] = portrait_submit(k, spec, m.get(k, {}))
                elif spec["kind"] in ("obj", "batch") and not m.get(k, {}).get("object_id") and not m.get(k, {}).get("done"):
                    m[k] = KIND[spec["kind"]][0](k, spec, m.get(k, {}))
                else:
                    KIND[spec["kind"]][1](k, spec, m[k])
            except Exception as e:
                log(k, "step error:", str(e)[:300])
            save(m)
        time.sleep(20)
    log("finished; still pending:", [k for k in todo if not m.get(k, {}).get("done")])
    log("balance:", req("GET", "/balance"))


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "status"
    if cmd == "run":
        run(sys.argv[2:])
    else:
        m = load()
        for k in SPECS:
            print(("done " if m.get(k, {}).get("done") else "todo ") + k)
