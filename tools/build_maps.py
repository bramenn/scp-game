"""Builds every map in tools/maps/*.py into data/maps/*.json and validates links.
Usage: python3 tools/build_maps.py [module ...]"""
import importlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE / "maps"))


def main(mods):
    mods = mods or sorted(p.stem for p in (HERE / "maps").glob("*.py") if p.stem != "test")
    for mod in mods:
        importlib.import_module(mod).build()
    maps = {p.stem: json.loads(p.read_text()) for p in (HERE.parent / "data/maps").glob("*.json")}
    errors = []
    for mid, m in maps.items():
        for e in m["exits"]:
            if e["to"] not in maps:
                errors.append(f"{mid}: exit to missing map {e['to']}")
            elif e["at"] not in maps[e["to"]]["spawns"]:
                errors.append(f"{mid}: exit to {e['to']} uses missing spawn {e['at']}")
        for name, (x, y, _f) in m["spawns"].items():
            if m["grid"][y][x] not in ".~":
                errors.append(f"{mid}: spawn {name} at ({x},{y}) is not floor")
    print(f"{len(maps)} maps;", "OK" if not errors else f"{len(errors)} errors")
    for e in errors:
        print("  ", e)
    return not errors


if __name__ == "__main__":
    sys.exit(0 if main(sys.argv[1:]) else 1)
