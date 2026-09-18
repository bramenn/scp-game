def L(en, es):
    """A localized string."""
    return {"en": en, "es": es}


def say(who, *lines, cond=None):
    a = {"say": list(lines), "who": who}
    if cond:
        a["cond"] = cond
    return a


def choice(who, prompt, *opts):
    """opts: (text, [actions], cond?)"""
    out = []
    for o in opts:
        d = {"text": o[0], "do": o[1]}
        if len(o) > 2 and o[2]:
            d["cond"] = o[2]
        out.append(d)
    return {"choice": out, "who": who, "prompt": prompt}
