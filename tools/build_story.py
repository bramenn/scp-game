"""Merges tools/story/*.py into data/{items,npcs,quests,docs,events,story}.json and validates
cross references (events used by maps and NPCs, items given, docs, quests).
Usage: python3 tools/build_story.py"""
import importlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA = HERE.parent / "data"
sys.path.insert(0, str(HERE / "story"))


def main():
    items, npcs, quests, docs, events, props, story, talk = {}, {}, {}, {}, {}, {}, {}, {}
    for p in sorted((HERE / "story").glob("*.py")):
        if p.stem == "common":
            continue
        mod = importlib.import_module(p.stem)
        items.update(getattr(mod, "ITEMS", {}))
        npcs.update(getattr(mod, "NPCS", {}))
        quests.update(getattr(mod, "QUESTS", {}))
        docs.update(getattr(mod, "DOCS", {}))
        events.update(getattr(mod, "EVENTS", {}))
        props.update(getattr(mod, "PROPS", {}))
        story.update(getattr(mod, "STORY", {}))
        talk.update(getattr(mod, "NPC_TALK", {}))
    for nid, t in talk.items():
        npcs[nid]["talk"] = t
    for d in docs:  # every document can lie on the floor as an item
        items.setdefault(d, {"type": "doc", "icon": "doc", "name": docs[d]["title"]})
    story["props"] = props
    errors = []

    def walk(actions, where):
        for a in actions:
            if isinstance(a, str):
                continue
            for k in ("then", "else"):
                walk(a.get(k, []), where)
            for c in a.get("choice", []):
                walk(c.get("do", []), where)
            for k in ("win", "lose", "flee"):
                walk(a.get(k, []), where)
            if "give" in a and a["give"] not in items:
                errors.append(f"{where}: gives unknown item {a['give']}")
            if "take" in a and a["take"] not in items:
                errors.append(f"{where}: takes unknown item {a['take']}")
            if "doc" in a and a["doc"] not in docs:
                errors.append(f"{where}: unknown doc {a['doc']}")
            if "quest" in a and a["quest"][0] not in quests:
                errors.append(f"{where}: unknown quest {a['quest'][0]}")
            if "run" in a and a["run"] not in events:
                errors.append(f"{where}: runs unknown event {a['run']}")
            if "who" in a and a["who"] not in npcs and a["who"] not in ("", "radio", "079"):
                errors.append(f"{where}: unknown speaker {a['who']}")

    for eid, acts in events.items():
        walk(acts, eid)
    for nid, n in npcs.items():
        for cond, ev in n.get("talk", []):
            if ev not in events:
                errors.append(f"npc {nid}: talk event {ev} missing")
    for mp in (DATA / "maps").glob("*.json"):
        m = json.loads(mp.read_text())
        for t in m["triggers"]:
            if t["event"] not in events:
                errors.append(f"{m['id']}: trigger event {t['event']} missing")
        for u in m["interact"]:
            if u["event"] not in events:
                errors.append(f"{m['id']}: interact event {u['event']} missing")
        for it in m["items"]:
            if it["id"] not in items:
                errors.append(f"{m['id']}: item {it['id']} unknown")
        for n in m["npcs"]:
            if n["id"] not in npcs:
                errors.append(f"{m['id']}: npc {n['id']} unknown")
    for name, obj in (("items", items), ("npcs", npcs), ("quests", quests), ("docs", docs), ("events", events),
                      ("story", story)):
        (DATA / f"{name}.json").write_text(json.dumps(obj, ensure_ascii=False, indent=0))
    print(f"story: {len(items)} items, {len(npcs)} npcs, {len(quests)} quests, {len(docs)} docs, {len(events)} events;",
          "OK" if not errors else f"{len(errors)} errors")
    for e in errors:
        print("  ", e)
    return not errors


if __name__ == "__main__":
    sys.exit(0 if main() else 1)
