"""Shared world data: combat enemies, SCP-939 voice lines."""
from common import L

STORY = {
    "enemies": {
        "zombie": dict(name=L("SCP-049-2", "SCP-049-2"), tag=L("'Cured' patient", "Paciente 'curado'"), sprite="zombie",
                       hp=34, atk=11, def_=4, flee=0.6, bg="#1b2226",
                       intro=L("A 'cured' patient lurches at you, stitches pulling apart.", "Un paciente 'curado' se abalanza sobre ti, con los puntos abriéndose."),
                       win=L("It folds to the floor like an empty coat.", "Se desploma en el suelo como un abrigo vacío."),
                       moves=[dict(name=L("Grab", "Agarrar"), power=16), dict(name=L("Bite", "Morder"), power=20),
                              dict(name=L("Moan", "Gemido"), power=6, fx="sanity")]),
        "zombie_guard": dict(name=L("SCP-049-2", "SCP-049-2"), tag=L("'Cured' guard", "Guardia 'curado'"), sprite="zombie_guard",
                             hp=46, atk=13, def_=7, flee=0.5, bg="#1b2226",
                             intro=L("A dead guard stands up, its baton still on its belt.", "Un guardia muerto se levanta, con la porra aún en el cinturón."),
                             win=L("It stops. For good this time.", "Se detiene. Esta vez para siempre."),
                             moves=[dict(name=L("Strangle", "Estrangular"), power=20), dict(name=L("Charge", "Embestir"), power=16)]),
        "rats": dict(name=L("Rat swarm", "Enjambre de ratas"), tag=L("Dozens of them", "Decenas"), sprite="rat",
                     hp=24, atk=8, def_=2, flee=0.8, bg="#1f1a14",
                     intro=L("The floor moves. It is all rats.", "El suelo se mueve. Son todo ratas."),
                     win=L("The swarm scatters into the pipes.", "El enjambre se dispersa por las tuberías."),
                     moves=[dict(name=L("Swarm", "Enjambrar"), power=12), dict(name=L("Bites", "Mordiscos"), power=9)]),
        "939": dict(name=L("SCP-939", "SCP-939"), tag=L("Keter · With Many Voices", "Keter · Con Muchas Voces"), sprite="scp939",
                    hp=90, atk=18, def_=9, flee=0.35, bg="#241214", cry="939_call",
                    intro=L("It opens its jaws and says your name. In Ortega's voice.", "Abre las fauces y dice tu nombre. Con la voz de Ortega."),
                    win=L("It retreats into the dark, wheezing through a dozen stolen voices.", "Se retira a la oscuridad, jadeando con una docena de voces robadas."),
                    moves=[dict(name=L("Bite", "Mordisco"), power=26), dict(name=L("Amnestic breath", "Aliento amnésico"), power=14, fx="sanity"),
                           dict(name=L("Pounce", "Salto"), power=22)]),
        "106": dict(name=L("SCP-106", "SCP-106"), tag=L("Keter · The Old Man", "Keter · El Viejo"), sprite="scp106",
                    hp=999, atk=16, def_=30, flee=0.9, bg="#140f14", immune=True,
                    intro=L("The Old Man grins at you from the other end of its world.", "El Viejo te sonríe desde el otro extremo de su mundo."),
                    moves=[dict(name=L("Corrode", "Corroer"), power=18), dict(name=L("Laugh", "Risa"), power=10, fx="sanity")]),
        "682": dict(name=L("SCP-682", "SCP-682"), tag=L("Keter · Hard-to-Destroy Reptile", "Keter · Reptil Difícil de Destruir"), sprite="scp682",
                    hp=260, atk=24, def_=14, flee=0.0, bg="#1a2410", cry="682_roar", music="chase",
                    intro=L("DISGUSTING, it says. Then it comes out of the acid.", "REPUGNANTE, dice. Luego sale del ácido."),
                    win=L("It sinks back into the acid, screaming, and the tank seals over it.", "Se hunde de nuevo en el ácido, gritando, y el tanque se sella sobre él."),
                    moves=[dict(name=L("Maul", "Destrozar"), power=30), dict(name=L("Tail sweep", "Coletazo"), power=22),
                           dict(name=L("Regenerate", "Regenerar"), power=30, fx="heal"),
                           dict(name=L("Hatred", "Odio"), power=12, fx="sanity")],
                    special=dict(label=L("Open the HCl valves", "Abrir las válvulas de HCl"), cond="item:hcl",
                                 text=L("You slam the injector into the valve port. Acid floods the chamber.", "Clavas el inyector en la válvula. El ácido inunda la cámara."),
                                 dmg_pct=0.45, event_flag="682_acid")),
    },
    "voices939": [
        dict(text=L("Hello? Is someone there?", "¿Hola? ¿Hay alguien ahí?")),
        dict(text=L("Help me... I can't see...", "Ayúdame... no veo nada...")),
        dict(text=L("Security, respond. Security.", "Seguridad, responda. Seguridad.")),
        dict(text=L("Mom? Mom, I'm in here.", "¿Mamá? Mamá, estoy aquí.")),
        dict(text=L("Vega. Over here. I found a way out.", "Vega. Aquí. Encontré una salida."), cond="met_ortega"),
        dict(text=L("Kid? Nico? Is that you?", "¿Chico? ¿Nico? ¿Eres tú?"), cond="met_nico"),
        dict(text=L("It's alright. It's alright. Come closer.", "Tranquilo. Tranquilo. Acércate.")),
        dict(text=L("Dani, it's me. It's Elena.", "Dani, soy yo. Soy Elena."), cond="read:doc_elena_log1"),
    ],
}

# battle.gd reads "def"; "def" is a Python keyword so data uses def_ and is renamed here
for e in STORY["enemies"].values():
    e["def"] = e.pop("def_")
