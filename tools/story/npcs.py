from common import L

# sprite: art/chars/<id>; portrait: art/portraits/<file>; voice: blip pitch
NPCS = {
    "vega": dict(name=L("Vega", "Vega"), sprite="vega", portrait="res://art/portraits/p_vega.png", voice=0.92),
    "ortega": dict(name=L("Sgt. Ortega", "Sgto. Ortega"), sprite="ortega32", portrait="res://art/portraits/p_ortega.png", voice=0.82,
                   talk=[["done:main_breach", "ortega_late"], ["nico_safe", "ortega_after_nico"],
                         ["met_ortega", "ortega_again"], ["", "ortega_first"]]),
    "nico": dict(name=L("D-4417 \"Nico\"", "D-4417 \"Nico\""), sprite="nico", portrait="res://art/portraits/p_nico.png", voice=1.15,
                 talk=[["follow:nico", "nico_following"], ["nico_safe", "nico_safe_talk"], ["met_nico", "nico_again"],
                       ["", "nico_first"]]),
    "lin": dict(name=L("Dr. Lin", "Dra. Lin"), sprite="lin", portrait="res://art/portraits/p_lin.png", voice=1.05, talk=[]),
    "reyes": dict(name=L("Cpl. Reyes", "Cabo Reyes"), sprite="reyes", portrait="res://art/portraits/p_reyes.png", voice=0.9, talk=[]),
    "tomas": dict(name=L("Tomás", "Tomás"), sprite="tomas", portrait="res://art/portraits/p_tomas.png", voice=0.78, talk=[]),
    "adebayo": dict(name=L("Dr. Adebayo", "Dr. Adebayo"), sprite="adebayo", portrait="res://art/portraits/p_adebayo.png", voice=0.86, talk=[]),
    "elena": dict(name=L("Dr. Elena Vega", "Dra. Elena Vega"), sprite="elena", portrait="res://art/portraits/p_elena.png", voice=1.1, talk=[]),
    "mara": dict(name=L("Mara", "Mara"), sprite="mara", portrait="res://art/portraits/p_mara.png", voice=1.0, talk=[]),
    "scp049": dict(name=L("SCP-049", "SCP-049"), sprite="scp049", portrait="res://art/portraits/p_049.png", voice=0.7, talk=[]),
}
