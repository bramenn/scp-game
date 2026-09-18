"""Act III — Maintenance & Sewers. Tomás, the power, Josie, SCP-087."""
from common import L, say, choice

N, R, V, T = "", "radio", "vega", "tomas"

QUESTS = {
    "main_power": dict(main=True, name=L("Lights Out", "Apagón"), stages=[
        L("Levels -3 to -5 have no power. Find a way into the electrical substation.", "Los niveles -3 a -5 no tienen energía. Encuentra la forma de entrar en la subestación."),
        L("Tomás gave you his keys. Find the three 400 A fuses: pump room, spider tunnel, boiler room.", "Tomás te dio sus llaves. Encuentra los tres fusibles de 400 A: sala de bombas, túnel de las arañas, sala de calderas."),
        L("Put the fuses in the three breakers and throw the main panel.", "Pon los fusibles en los tres interruptores y activa el panel principal."),
    ]),
    "side_josie": dict(name=L("The half-cat", "La media gata"), stages=[
        L("Tomás' cat Josie is lost somewhere down here. She likes cheese.", "La gata de Tomás, Josie, anda perdida por aquí. Le gusta el queso."),
        L("Josie is following you. Take her home to Tomás.", "Josie te sigue. Llévala con Tomás."),
    ]),
    "side_087": dict(name=L("The Stairwell", "La escalera"), stages=[
        L("There is a door marked SCP-087 past the spider tunnel. Nobody is allowed down there.", "Hay una puerta marcada SCP-087 más allá del túnel de las arañas. Nadie puede bajar ahí."),
        L("Something is crying at the bottom of the stairs. Go down, or don't.", "Algo llora al fondo de la escalera. Baja, o no."),
    ]),
}

DOCS = {
    "doc_power_memo": dict(title=L("Maintenance memo", "Nota de mantenimiento"), body=L(
        "Main breakers for -3/-4/-5 were pulled at 03:13 by remote order. Fuses removed and 'secured' by the night crew, who "
        "then ran. If you find them: pump room, the old tunnel, boiler room. The substation door is on Tomás' ring. Good luck "
        "finding Tomás. - Shift lead",
        "Los interruptores de -3/-4/-5 se abrieron a las 03:13 por orden remota. Los fusibles los quitó y 'guardó' el turno de "
        "noche, que luego huyó. Si los encuentras: sala de bombas, el túnel viejo, calderas. La puerta de la subestación está en "
        "el llavero de Tomás. Suerte encontrando a Tomás. - Jefe de turno")),
    "doc_tomas_note": dict(title=L("Scrawled on a pipe", "Garabateado en una tubería"), body=L(
        "RATS = FRIENDS. PEOPLE = DANGER. CAT = MISSING. IF YOU FIND JOSIE BRING HER HOME. - T.",
        "RATAS = AMIGAS. GENTE = PELIGRO. GATA = PERDIDA. SI ENCUENTRAS A JOSIE TRÁELA A CASA. - T.")),
    "doc_substation": dict(title=L("Burnt logbook", "Bitácora quemada"), body=L(
        "03:13 - Remote shutdown. Authorization: CORE. Core? Core is a computer. Since when does it give orders?\n"
        "03:20 - Rodríguez tried to reset breaker 2 by hand. Rodríguez is dead.\n03:21 - Leaving.",
        "03:13 - Apagado remoto. Autorización: NÚCLEO. ¿Núcleo? El núcleo es un ordenador. ¿Desde cuándo da órdenes?\n"
        "03:20 - Rodríguez intentó rearmar el interruptor 2 a mano. Rodríguez está muerto.\n03:21 - Me voy.")),
    "doc_087_warning": dict(title=L("Warning sign, torn", "Cartel de aviso, rasgado"), body=L(
        "SCP-087. NO PERSONNEL ARE PERMITTED ACCESS. Light sources brighter than 75 W are ineffective: the stairwell absorbs "
        "the excess. If you hear a child asking for help, do not answer. It is not a child.",
        "SCP-087. NINGÚN PERSONAL TIENE PERMITIDO EL ACCESO. Las fuentes de luz de más de 75 W son ineficaces: la escalera "
        "absorbe el exceso. Si oye a un niño pidiendo ayuda, no responda. No es un niño."),
        source="SCP-087 by Zaeyde · scp-wiki.wikidot.com/scp-087 · CC BY-SA 3.0"),
    "doc_087_log": dict(title=L("Exploration log 087-I (excerpt)", "Registro de exploración 087-I (extracto)"), body=L(
        "An unlit stairwell, 38° descent, 13 steps per flight, then a semicircular landing. Visibility: about one and a half "
        "flights. Sounds of a child, estimated 200 m below, pleading for help. After 22 minutes the subject reports the voice is "
        "no closer. After 30 minutes a face is seen on the landing below. No pupils. No nostrils. No mouth. The subject runs. "
        "It takes him much longer to go up than it took him to go down.",
        "Una escalera sin luz, 38° de descenso, 13 escalones por tramo y un rellano semicircular. Visibilidad: tramo y medio. "
        "Sonidos de un niño, a unos 200 m por debajo, pidiendo ayuda. A los 22 minutos el sujeto informa de que la voz no está "
        "más cerca. A los 30 minutos se ve una cara en el rellano de abajo. Sin pupilas. Sin nariz. Sin boca. El sujeto corre. "
        "Tarda mucho más en subir de lo que tardó en bajar."), source="SCP-087 by Zaeyde · scp-wiki.wikidot.com/scp-087 · CC BY-SA 3.0"),
    "doc_087_bottom": dict(title=L("Scratched into the last landing", "Rayado en el último rellano"), body=L(
        "I came down to find her. There was no her. There is only down. - Dr. [name scratched out]",
        "Bajé a buscarla. No había ella. Solo hay abajo. - Dr. [nombre tachado]"), sanity=-6),
}

EVENTS = {
    "enter:C01": [{"if": "!c01_seen", "then": [{"mark": "c01_seen"}, {"wait": 0.5},
        say(N, L("Level -3. The only light is the red pulse of the emergency lamps. Water drips somewhere. Something small runs.",
                 "Nivel -3. La única luz es el pulso rojo de las lámparas de emergencia. Gotea agua en algún sitio. Algo pequeño corre.")),
        say(R, L("Vega, the power for the lower levels was cut from here. The medical wing and the Heavy Containment lift are dead without it.",
                 "Vega, la energía de los niveles inferiores se cortó desde aquí. Sin ella, el ala médica y el ascensor de Contención Pesada están muertos.")),
        {"quest": ["main_power", 1]},
        {"objective": L("Find a way into the electrical substation.", "Encuentra la forma de entrar en la subestación eléctrica.")}]}],
    "c04_spiders": [say(N, L("Webs hang from every pipe. Some of them twitch.", "Hay telarañas colgando de cada tubería. Algunas se mueven.")), {"sanity": -3}],
    "c07_burn": [{"sfx": "gas_hiss", "db": -4}, {"hp": -6, "cause": "wounds"}],
    # ------------------------------------------------------------ Tomás
    "tomas_first": [
        {"mark": "met_tomas"},
        say(T, L("Stop right there. Slow. Show me your hands. ...Foundation. Figures.", "Quieto ahí. Despacio. Enséñame las manos. ...Fundación. Cómo no."),
            L("Thirty-one years I've mopped this place. Nobody comes down here. Not even the things that got out. Too many rats. They like the rats.",
              "Treinta y un años fregando este sitio. Aquí no baja nadie. Ni siquiera las cosas que se escaparon. Demasiadas ratas. Les gustan las ratas.")),
        choice(T, "",
               (L("I need the substation keys.", "Necesito las llaves de la subestación."), [
                   say(T, L("Course you do. Everybody needs something from Tomás. Nobody brings Tomás anything.", "Claro. Todo el mundo necesita algo de Tomás. Nadie le trae nada a Tomás."))]),
               (L("How are you still alive?", "¿Cómo sigues vivo?"), [
                   say(T, L("I know where not to be. And I don't look at things. Twenty years ago a doctor told me: 'Tomás, the less you see, the longer you live.' He saw something. I didn't.",
                            "Sé dónde no estar. Y no miro las cosas. Hace veinte años un doctor me dijo: 'Tomás, cuanto menos veas, más vivirás.' Él vio algo. Yo no."))])),
        say(T, L("Here. Keys. And this card, Level 3. Took it off Dr. Mills in the pipes. He won't be needing it.",
                 "Toma. Llaves. Y esta tarjeta, nivel 3. Se la quité al Dr. Mills en las tuberías. No la va a necesitar."),
            L("Fuses? The night crew hid them where nobody'd go: pump room, the old tunnel with the spiders, the boilers. Idiots.",
              "¿Fusibles? El turno de noche los escondió donde nadie iría: sala de bombas, el túnel viejo de las arañas, las calderas. Idiotas."),
            L("And if you see a grey cat... half a grey cat... that's Josie. She's mine. She likes cheese.",
              "Y si ves una gata gris... media gata gris... es Josie. Es mía. Le gusta el queso.")),
        {"give": "janitor_keys"}, {"give": "card_3"},
        {"quest": ["main_power", 2]}, {"quest": ["side_josie", 1]},
        {"objective": L("Find the three fuses: pump room, spider tunnel, boiler room.", "Encuentra los tres fusibles: bombas, túnel de las arañas, calderas.")},
    ],
    "tomas_again": [
        {"if": "follow_josie", "then": [
            say(T, L("Josie! Josie, you stupid, beautiful half-a-cat. Come here.", "¡Josie! Josie, media gata tonta y preciosa. Ven aquí.")),
            {"unmark": "follow_josie"}, {"mark": "josie_found"}, {"quest": ["side_josie", -1]},
            say(T, L("...Thank you. Nobody's done a thing for me in this place in thirty years. Take these. And listen.",
                     "...Gracias. Nadie ha hecho nada por mí en este sitio en treinta años. Toma esto. Y escucha."),
                L("The kids in D-block. Tuesday. I cleaned the acid room after last time. They said it was a 'drill'. It wasn't a drill.",
                  "Los chicos del bloque D. El martes. Limpié la sala del ácido después de la última vez. Dijeron que era un 'simulacro'. No era un simulacro.")),
            {"give": "adrenaline"}, {"give": "battery", "n": 2}, {"mark": "tomas_told_acid"}],
         "else": [say(T, L("Fuses. Pump room, tunnel, boilers. Then the big panel. Don't touch the red cable. I mean it.",
                           "Fusibles. Bombas, túnel, calderas. Luego el panel grande. No toques el cable rojo. Lo digo en serio."))]},
    ],
    # ------------------------------------------------------------ Josie
    "josie_talk": [
        {"if": "follow_josie", "then": [say(N, L("Josie purrs and bumps her head against your boot. Her back half isn't there. She doesn't seem to mind.",
                                                 "Josie ronronea y te da cabezazos en la bota. Su mitad trasera no está. No parece importarle."))],
         "else": [
            say(N, L("A grey tabby cat. It ends at the ribcage: behind it there is only a flat, perfect black.", "Una gata atigrada gris. Termina en las costillas: detrás solo hay un negro plano y perfecto."),
                L("She walks as if her back legs were still there.", "Camina como si sus patas traseras siguieran ahí.")),
            {"if": "item:cheese", "then": [
                choice(N, "", (L("Offer the cheese", "Ofrecerle el queso"), [{"take": "cheese"}, {"sfx": "squeak", "pitch": 0.6},
                               say(N, L("She eats it in three bites, then decides you are her person now.", "Se lo come en tres bocados y decide que ahora eres su persona.")),
                               {"mark": "follow_josie"}, {"quest": ["side_josie", 2]}]),
                       (L("Leave her", "Dejarla"), []))],
             "else": [say(N, L("She ignores you with great dignity.", "Te ignora con gran dignidad."))]}]},
    ],
    # ------------------------------------------------------------ substation
    "enter:C06": [{"if": "!c06_seen", "then": [{"mark": "c06_seen"}, {"quest": ["main_power", 3]}]}],
    **{f"c06_breaker{i}": [
        {"if": f"breaker{i}", "then": [say(N, L(f"Breaker {i}: fuse seated. Ready.", f"Interruptor {i}: fusible colocado. Listo."))],
         "else": [{"if": "item:fuse", "then": [
             {"take": "fuse"}, {"sfx": "lock_click"}, {"mark": f"breaker{i}"},
             say(N, L(f"You slide a fuse into breaker {i}. It clicks home.", f"Metes un fusible en el interruptor {i}. Encaja con un clic."))],
             "else": [say(N, L("An empty fuse slot. 400 A.", "Un hueco vacío para fusible. 400 A."))]}]}] for i in (1, 2, 3)},
    "c06_console": [
        {"if": "power_on", "then": [say(N, L("MAIN BUS: ONLINE.", "BUS PRINCIPAL: EN LÍNEA."))], "else": [
            {"if": "breaker1,breaker2,breaker3", "then": [
                {"sfx": "breaker", "db": 4}, {"shake": 1.0, "power": 3}, {"mark": "power_on"}, {"call": "relight"},
                {"sfx": "power_up", "db": 2}, {"call": "refresh_doors"},
                say(N, L("The panel roars. Somewhere above and below you, thousands of lights come on at once.",
                         "El panel ruge. Por encima y por debajo de ti, miles de luces se encienden a la vez.")),
                say(R, L("Power is back on -3 to -5. Well done, Vega. The medical wing is open. The HCZ lift needs Level 4.",
                         "La energía ha vuelto de -3 a -5. Bien hecho, Vega. El ala médica está abierta. El ascensor de ZCP necesita nivel 4.")),
                say("ortega", L("Vega, it's Ortega. I heard. The HCZ generator has to be started by hand or the lift won't hold.",
                                "Vega, soy Ortega. Me he enterado. El generador de ZCP hay que arrancarlo a mano o el ascensor no aguantará."),
                    L("I'm going down the service shaft. Don't argue. The kid's safe with the door locked.",
                      "Voy a bajar por el pozo de servicio. No discutas. El chico está a salvo con la puerta cerrada.")),
                choice(V, "",
                       (L("Ortega, wait for me.", "Ortega, espérame."), [say("ortega", L("No time. See you down there.", "No hay tiempo. Nos vemos abajo."))]),
                       (L("Be careful.", "Ten cuidado."), [say("ortega", L("Always am.", "Siempre lo tengo."))])),
                {"mark": "ortega_went_hcz"}, {"quest": ["main_power", -1]},
                {"objective": L("Enter the medical wing (east of the maintenance junction).", "Entra en el ala médica (al este del cruce de mantenimiento).")},
                {"save": True}],
             "else": [say(N, L("MAIN BUS: FAULT. Breakers 1-3 need fuses.", "BUS PRINCIPAL: FALLO. Los interruptores 1-3 necesitan fusibles."))]}]}],
    "item:fuse": [{"if": "!quest:main_power:2", "then": [{"quest": ["main_power", 2]}]}],
    # ------------------------------------------------------------ SCP-087
    "enter:C08": [{"if": "!c08_seen", "then": [{"mark": "c08_seen"}, {"quest": ["side_087", 1]}]}],
    "enter:C09": [{"if": "!c09_seen", "then": [{"mark": "c09_seen"}, {"quest": ["side_087", 2]},
        say(N, L("Your flashlight reaches barely a flight ahead. The dark below swallows the rest.", "La linterna apenas llega a un tramo. La oscuridad de abajo se traga el resto.")),
        {"sfx": "child_cry", "db": -12}]}],
    "c09_depth1": [{"sfx": "child_cry", "db": -8}, say(N, L("A child's voice, far below: 'Help me... please...'", "Una voz de niño, muy abajo: 'Ayúdame... por favor...'"))],
    "c09_depth2": [{"sfx": "child_cry", "db": -6}, say(N, L("You have gone down further than the building is deep. The voice is no closer.",
                                                             "Has bajado más de lo que mide el edificio. La voz no está más cerca.")), {"sanity": -6}],
    "c09_depth3": [{"sfx": "child_cry", "db": -4}, say(N, L("The steps are wet. You don't remember how many flights. You count again. You get a different number.",
                                                             "Los escalones están húmedos. No recuerdas cuántos tramos. Vuelves a contar. Te sale otro número.")), {"sanity": -8}],
    "c09_face": [
        {"if": "!saw_087", "then": [
            {"lights": "off"}, {"music": ""}, {"wait": 1.2}, {"sfx": "static_burst", "db": -4},
            {"flash": 1, "color": "#e8e8f0"},
            say(N, L("On the landing below, a face. Pale. No pupils. No nostrils. No mouth.", "En el rellano de abajo, una cara. Pálida. Sin pupilas. Sin nariz. Sin boca."),
                L("It is not the child. It was never the child.", "No es el niño. Nunca fue el niño.")),
            {"sfx": "heartbeat", "db": 2}, {"shake": 1.5, "power": 2}, {"sanity": -30},
            {"mark": "saw_087"}, {"doc": "doc_087_bottom"}, {"quest": ["side_087", -1]},
            {"objective": L("Get out of the stairwell.", "Sal de la escalera.")}]}],
    "enter:C05": [{"if": "follow_josie,!josie_found", "then": [{"wait": 0.3}, {"run": "tomas_again"}]}],
}

PROPS = {
    "breaker": L("A breaker cabinet. The fuse slot is empty.", "Un armario de interruptores. El hueco del fusible está vacío."),
    "burn_barrel": L("Warm. Tomás burns old files in it. Some of them still have photos.", "Caliente. Tomás quema expedientes viejos. Algunos todavía tienen fotos."),
    "mattress": L("Tomás' bed. A rat is asleep on the pillow.", "La cama de Tomás. Una rata duerme en la almohada."),
    "spider_web": L("Thick, dusty, occupied.", "Espesa, polvorienta, habitada."),
    "boiler": L("It ticks and groans. The gauge is in the red.", "Hace tic-tac y gime. La aguja está en rojo."),
    "pump": L("The pump hums. Water still rises around your boots.", "La bomba zumba. El agua sigue subiendo alrededor de tus botas."),
}

NPC_TALK = {"tomas": [["met_tomas", "tomas_again"], ["", "tomas_first"]]}
