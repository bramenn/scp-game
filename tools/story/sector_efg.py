"""Acts V-VI — Heavy Containment, the Pocket Dimension, the 079 Core, Gate A and the three endings."""
from common import L, say, choice

N, R, V, RY, EL, MA = "", "radio", "vega", "reyes", "elena", "mara"
SRC = lambda n, a: f"SCP-{n} by {a} · scp-wiki.wikidot.com/scp-{n} · CC BY-SA 3.0"

QUESTS = {
    "main_hcz": dict(main=True, name=L("Heavy Containment", "Contención Pesada"), stages=[
        L("Find the last Nine-Tailed Fox operative somewhere past the dark sector.", "Encuentra al último operativo de Nueve Colas más allá del sector oscuro."),
        L("Reyes: recontain SCP-106 with the femur breaker. It needs a lure.", "Reyes: recontén a SCP-106 con el rompefémures. Necesita un señuelo."),
        L("Recover Reyes' recall recording from the SCP-096 chamber - or find another lure.", "Recupera la grabación de reclamo de Reyes en la cámara de SCP-096, o busca otro señuelo."),
        L("Use the recall console in the femur breaker room.", "Usa la consola de reclamo en la sala del rompefémures."),
        L("SCP-682 is loose in its acid chamber. The lift to the core is behind it.", "SCP-682 anda suelto en su cámara de ácido. El ascensor al núcleo está detrás."),
        L("Take the lift down to Level -5.", "Toma el ascensor al Nivel -5."),
    ]),
    "side_tags": dict(name=L("Dog tags", "Placas de identificación"), stages=[
        L("Reyes asked you to bring back the dog tags of his squad. There were five.", "Reyes te pidió recuperar las placas de su escuadra. Eran cinco."),
    ]),
    "side_ortega": dict(name=L("Ortega", "Ortega"), stages=[
        L("Ortega went to start the HCZ generator. He hasn't answered since.", "Ortega fue a arrancar el generador de ZCP. No ha vuelto a responder."),
    ]),
    "main_core": dict(main=True, name=L("Threshold", "Umbral"), stages=[
        L("Reach the SCP-079 core. Elena is there.", "Llega al núcleo de SCP-079. Elena está ahí."),
        L("Decide what to do with SCP-079.", "Decide qué hacer con SCP-079."),
        L("Disarm the Alpha Warhead in warhead control.", "Desarma la ojiva Alfa en el control de la ojiva."),
        L("Reach the Gate A lift.", "Llega al ascensor del Portón A."),
    ]),
}

DOCS = {
    "doc_ntf_orders": dict(title=L("Epsilon-11 orders", "Órdenes de Épsilon-11"), body=L(
        "PRIORITY 1: Secure SCP-079 core. PRIORITY 2: Recontain Keter-class entities. PRIORITY 3: Personnel.\n"
        "Addendum, 03:40, O5 channel: 'D-Block assets are to be considered expended. Do not escort.'\n"
        "Someone has written under it in marker: NO. - REYES",
        "PRIORIDAD 1: Asegurar el núcleo de SCP-079. PRIORIDAD 2: Recontener entidades Keter. PRIORIDAD 3: Personal.\n"
        "Anexo, 03:40, canal O5: 'Los recursos del Bloque D se consideran gastados. No escoltar.'\n"
        "Alguien ha escrito debajo con rotulador: NO. - REYES")),
    "doc_939_file": dict(title=L("SCP-939 - With Many Voices", "SCP-939 - Con Muchas Voces"), body=L(
        "Keter. Pack predators, around 2.2 m long, 250 kg, translucent red skin, no eyes. They hunt by heat and sound. They "
        "mimic human speech, most often the voices of their previous victims, to lure new prey.\n\nThey exhale AMN-C227, a "
        "Class-C amnestic: exposure prevents new memories from forming. If you don't remember how you got here, walk away.",
        "Keter. Depredadores en manada, unos 2,2 m, 250 kg, piel roja translúcida, sin ojos. Cazan por calor y sonido. Imitan "
        "el habla humana, casi siempre con las voces de sus víctimas anteriores, para atraer presas nuevas.\n\nExhalan "
        "AMN-C227, un amnésico de clase C: la exposición impide formar recuerdos nuevos. Si no recuerdas cómo llegaste aquí, "
        "aléjate."), source=SRC(939, "Adam Smascher & EchoFourDelta")),
    "doc_096_file": dict(title=L("SCP-096 - Containment", "SCP-096 - Contención"), body=L(
        "Euclid. Held in a 5x5x5 m airtight steel cube. No cameras: pressure sensors and lasers only. A pale humanoid, 2.38 m, "
        "long arms, a jaw that opens four times wider than a human's. Docile. It paces. It cries.\n\nViewing its face - "
        "directly, on video, in a photograph - triggers it. It covers its face, screams, and then comes for the viewer, "
        "wherever they are. Nothing has stopped it. Nothing but a bag over its head.",
        "Euclid. Contenido en un cubo de acero hermético de 5x5x5 m. Sin cámaras: solo sensores de presión y láseres. Un "
        "humanoide pálido de 2,38 m, brazos largos, una mandíbula que se abre cuatro veces más que la humana. Dócil. Camina. "
        "Llora.\n\nVer su cara - en persona, en vídeo, en foto - lo activa. Se tapa la cara, grita y luego va a por quien la "
        "vio, esté donde esté. Nada lo ha detenido. Nada salvo una bolsa sobre la cabeza."), source=SRC("096", "Dr Dan")),
    "doc_096_bag_note": dict(title=L("Retrieval note 096-1-A", "Nota de recuperación 096-1-A"), body=L(
        "Anti-tank rounds did nothing. The hood worked. Approach from BEHIND. Never walk around it. Never let it turn.",
        "Las balas antitanque no hicieron nada. La capucha funcionó. Acercarse por DETRÁS. Nunca rodearlo. Nunca dejar que "
        "se gire.")),
    "doc_106_file": dict(title=L("SCP-106 - The Old Man", "SCP-106 - El Viejo"), body=L(
        "Keter. An elderly, decomposed humanoid. Whatever it touches corrodes: a black mucus that keeps rotting matter for "
        "hours. It walks through solid walls into a pocket dimension of its own, and comes out anywhere connected to where it "
        "went in. It keeps its prey there. It plays with them.\n\nSudden direct light makes it retreat.",
        "Keter. Un humanoide anciano y descompuesto. Todo lo que toca se corroe: un moco negro que sigue pudriendo la materia "
        "durante horas. Atraviesa paredes hacia una dimensión de bolsillo propia y sale por cualquier punto conectado con el "
        "de entrada. Guarda allí a sus presas. Juega con ellas.\n\nLa luz directa y repentina lo hace retroceder."),
        source=SRC(106, "Dr Gears")),
    "doc_femur_procedure": dict(title=L("Recall Protocol 106", "Protocolo de reclamo 106"), body=L(
        "When breached: select a human subject aged 10-25. Fracture a major bone. Place the subject in the recall chamber. "
        "Broadcast. SCP-106 will gravitate toward the lure within 10-15 minutes. Repeat trauma every 20 minutes if needed.\n\n"
        "(Reyes' squad carried a recording of a previous procedure. Played at full volume, it works. Nobody likes to talk "
        "about where the recording came from.)",
        "En caso de brecha: seleccionar un sujeto humano de 10 a 25 años. Fracturarle un hueso largo. Colocarlo en la cámara "
        "de reclamo. Emitir. SCP-106 se dirigirá al señuelo en 10-15 minutos. Repetir el trauma cada 20 minutos si es "
        "necesario.\n\n(La escuadra de Reyes llevaba la grabación de un procedimiento anterior. A todo volumen, funciona. A "
        "nadie le gusta hablar de dónde salió la grabación.)"), source=SRC(106, "Dr Gears"), sanity=-5),
    "doc_682_file": dict(title=L("SCP-682 - Hard-to-Destroy Reptile", "SCP-682 - Reptil Difícil de Destruir"), body=L(
        "Keter. Large, reptile-like, extremely intelligent, and hateful of all life. It regenerates from 87% destruction. "
        "It adapts to whatever hurts it. Kept in a 5x5x5 m chamber lined with 25 cm of acid-resistant steel, submerged in "
        "hydrochloric acid. It has described humans as 'disgusting'. Termination has been attempted many times. It is "
        "still here.",
        "Keter. Grande, parecido a un reptil, extremadamente inteligente y lleno de odio hacia toda forma de vida. Se regenera "
        "tras un 87% de destrucción. Se adapta a lo que le hace daño. Contenido en una cámara de 5x5x5 m revestida con 25 cm de "
        "acero resistente al ácido, sumergido en ácido clorhídrico. Ha descrito a los humanos como 'repugnantes'. Se ha "
        "intentado terminarlo muchas veces. Sigue aquí."), source=SRC(682, "Dr Gears & Epic Phail Spy")),
    "doc_black_tide_final": dict(title=L("O5 memo - Black Tide, phase 2", "Memorándum O5 - Marea Negra, fase 2"), body=L(
        "If SCP-682 adapts to acid during Phase 1, Phase 2 authorizes the Alpha Warhead with the D-Block inside the chamber. "
        "Site staff to be evacuated first. Site Director Aldana to confirm.\n\nIn the margin, in Elena's handwriting: 'They "
        "were going to nuke forty people to kill one lizard. And it wouldn't even have worked.'",
        "Si SCP-682 se adapta al ácido durante la Fase 1, la Fase 2 autoriza la ojiva Alfa con el Bloque D dentro de la "
        "cámara. El personal del sitio será evacuado primero. La directora Aldana confirmará.\n\nEn el margen, con la letra de "
        "Elena: 'Iban a volar a cuarenta personas para matar a un lagarto. Y ni siquiera habría funcionado.'"), sanity=-4),
    "doc_ortega_last": dict(title=L("Ortega's notebook", "La libreta de Ortega"), body=L(
        "Generator's running. Lift will hold. Something in the dark keeps saying my name in my wife's voice. Carmen's been "
        "dead eight years. I'm not going out there.\n\nIf Vega reads this: the kid has a sister in Guadalajara. Her name is "
        "in my wallet. Tell her he was brave.",
        "El generador funciona. El ascensor aguantará. Algo en la oscuridad repite mi nombre con la voz de mi mujer. Carmen "
        "murió hace ocho años. No voy a salir.\n\nSi Vega lee esto: el chico tiene una hermana en Guadalajara. Su nombre está "
        "en mi cartera. Dile que fue valiente."), sanity=-6),
}

TAGS = [f"tag_{i}" for i in range(1, 6)]

EVENTS = {
    # ------------------------------------------------------------ HCZ arrival
    "enter:E01": [{"if": "!e01_seen", "then": [{"mark": "e01_seen"}, {"wait": 0.5},
        say(N, L("Level -4. Heavy Containment. The air is cold, and it tastes of metal.", "Nivel -4. Contención Pesada. El aire es frío y sabe a metal.")),
        say(R, L("Vega, Kessler. Your signal is weak down there. Epsilon-11's last position was west, past the dark sector.",
                 "Vega, Kessler. Su señal es débil ahí abajo. La última posición de Épsilon-11 fue al oeste, pasado el sector oscuro."),
            L("The dark sector is SCP-939 territory. They're blind. They hunt by sound. Walk. Do not run.",
              "El sector oscuro es territorio de SCP-939. Son ciegos. Cazan por el sonido. Camine. No corra.")),
        {"if": "ortega_went_hcz", "then": [{"quest": ["side_ortega", 1]}]},
        {"quest": ["main_hcz", 1]},
        {"objective": L("Find the Nine-Tailed Fox operative (west, through the dark sector).", "Encuentra al operativo de Nueve Colas (al oeste, por el sector oscuro).")}]}],
    "enter:E02": [{"if": "!e02_seen", "then": [{"mark": "e02_seen"},
        say(N, L("Pitch dark. The walls sweat. Somewhere ahead, something breathes in and doesn't breathe out.",
                 "Oscuridad total. Las paredes sudan. En algún lugar, delante, algo inspira y no expulsa el aire."))]}],
    "e03_radio": [{"sfx": "radio_static"},
        say(N, L("A handheld radio, still on. Through the static, a voice: 'Vega... it's Ortega... I'm hurt, I'm in the dark sector, come find me...'",
                 "Una radio portátil, encendida. Entre la estática, una voz: 'Vega... soy Ortega... estoy herido, en el sector oscuro, ven a buscarme...'"),
            L("Then, in exactly the same voice, the same words again. And again.", "Luego, con exactamente la misma voz, las mismas palabras. Otra vez. Y otra.")),
        {"sanity": -6}],
    # ------------------------------------------------------------ Reyes
    "reyes_first": [
        {"mark": "met_reyes"}, {"call": "refresh_doors"},
        say(RY, L("...Friendly? Friendly. Thank God. Cabo Reyes, Epsilon-11. What's left of it.", "...¿Amigo? Amigo. Gracias a Dios. Cabo Reyes, Épsilon-11. Lo que queda."),
            L("We came down for the core. 106 came up through the floor and took Díaz and Park. 939 got Moreno in the dark. The rest... the lizard.",
              "Bajamos a por el núcleo. 106 subió por el suelo y se llevó a Díaz y a Park. Un 939 atrapó a Moreno en la oscuridad. El resto... el lagarto.")),
        choice(RY, "",
               (L("I need to reach the core.", "Tengo que llegar al núcleo."), [
                   say(RY, L("The lift to Level -5 is in the 682 control room. 682 broke out of its tank during a 'trial'. It's still in there.",
                             "El ascensor al nivel -5 está en la sala de control de 682. 682 salió de su tanque durante una 'prueba'. Sigue ahí dentro."),
                       L("And the only way there goes through 106's containment. With 106 loose, you'll never make it. We have to recall it.",
                         "Y el único camino pasa por la contención de 106. Con 106 suelto, no llegarás. Hay que reclamarlo."))]),
               (L("Did you know Dr. Elena Vega?", "¿Conocías a la Dra. Elena Vega?"), [
                   say(RY, L("Vega... She came to our barracks a week ago. Asked us to refuse Black Tide. Our commander laughed at her.",
                             "Vega... Vino a nuestro barracón hace una semana. Nos pidió que nos negáramos a Marea Negra. Nuestro comandante se rio de ella."),
                       L("I didn't. I wrote NO on the orders. For all the good it did.", "Yo no. Escribí NO en las órdenes. Para lo que sirvió."))])),
        say(RY, L("The femur breaker room is past 106's cell. It needs a lure. We had a recording, but I dropped the recorder in 096's chamber when it started screaming.",
                  "La sala del rompefémures está pasada la celda de 106. Necesita un señuelo. Teníamos una grabación, pero se me cayó la grabadora en la cámara de 096 cuando empezó a gritar."),
            L("Take my vest. Take this injector - hydrochloric acid, for 682. And my card, Level 5. Captain won't need it.",
              "Llévate mi chaleco. Llévate este inyector: ácido clorhídrico, para 682. Y mi tarjeta, nivel 5. El capitán ya no la necesita."),
            L("And... if you find the others' dog tags. Five of them. Bring them. Their families should get something back.",
              "Y... si encuentras las placas de los demás. Cinco. Tráelas. Sus familias deberían recuperar algo.")),
        {"give": "vest"}, {"give": "hcl"}, {"give": "card_5"},
        {"quest": ["main_hcz", 2]}, {"quest": ["side_tags", 1]},
        {"objective": L("Recover Reyes' recorder from the SCP-096 chamber (north of the tesla corridor).", "Recupera la grabadora de Reyes en la cámara de SCP-096 (al norte del pasillo Tesla).")},
        {"quest": ["main_hcz", 3]},
    ],
    "reyes_again": [
        {"if": "count:dogtag:5,!tags_given_all", "then": [{"run": "reyes_count_tags"}],
         "else": [{"if": "item:dogtag,!tags_given_all", "then": [
             say(RY, L("Keep them for now. When you have all five, bring them together.", "Guárdalas por ahora. Cuando tengas las cinco, tráelas juntas."))]}]},
        {"if": "!item:recorder,!scp106_contained,!reyes_volunteer", "then": [
            choice(RY, L("No recorder yet?", "¿Aún no tienes la grabadora?"),
                   (L("Not yet.", "Todavía no."), [say(RY, L("096's chamber. From behind. Never let it see you.", "La cámara de 096. Por detrás. Que nunca te vea."))]),
                   (L("There has to be another lure.", "Tiene que haber otro señuelo."), [
                       say(RY, L("There is. Me.", "Lo hay. Yo."),
                           L("I'm bleeding inside, Vega. I've got an hour, maybe. Let me be useful for it.", "Estoy sangrando por dentro, Vega. Me queda una hora, quizá. Déjame ser útil."),
                           L("Say the word and I'll walk to that chair myself.", "Di una palabra y caminaré yo solo hasta esa silla.")),
                       choice(V, "",
                              (L("...Go. I'm sorry.", "...Ve. Lo siento."), [{"mark": "reyes_volunteer"},
                                  say(RY, L("Don't be. Tell them Epsilon-11 finished the job.", "No lo sientas. Diles que Épsilon-11 terminó el trabajo.")),
                                  {"npc": "reyes", "remove": True}, {"mark": "reyes_gone"},
                                  {"objective": L("Reyes is in the recall chamber. Use the femur breaker console.", "Reyes está en la cámara de reclamo. Usa la consola del rompefémures.")}]),
                              (L("No. I'll find the tape.", "No. Encontraré la cinta."), [say(RY, L("Then hurry.", "Entonces date prisa."))]))]))]},
        {"if": "scp106_contained,!reyes_gone", "then": [say(RY, L("The Old Man's back in its box? ...Díaz. Park. We got it.", "¿El Viejo ha vuelto a su caja? ...Díaz. Park. Lo conseguimos."))]},
    ],
    "reyes_count_tags": [
        say(RY, L("Moreno. Díaz. Park. Okafor. Lindqvist. ...All of them.", "Moreno. Díaz. Park. Okafor. Lindqvist. ...Todos."),
            L("Thank you. Take this. It was our captain's. It's the only thing down here that isn't broken.", "Gracias. Toma. Era de nuestro capitán. Es lo único aquí abajo que no está roto.")),
        {"take": "dogtag", "n": 5}, {"give": "adrenaline"}, {"give": "scp500"}, {"mark": "tags_given_all"}, {"quest": ["side_tags", -1]},
    ],
    # ------------------------------------------------------------ 096
    "enter:E07": [{"if": "!e07_seen", "then": [{"mark": "e07_seen"},
        say(N, L("A steel cube in the middle of the chamber. Its door has been torn open from the inside. Something inside is crying.",
                 "Un cubo de acero en mitad de la cámara. Su puerta ha sido arrancada desde dentro. Algo dentro está llorando.")),
        say(V, L("Don't look at its face. From behind. Slowly.", "No le mires la cara. Por detrás. Despacio."))]}],
    "scp096_bag": [
        {"sfx": "paper", "pitch": 0.6},
        say(N, L("You pull the hood over its head in one motion. Its whole body goes rigid.", "Le pones la capucha en un solo movimiento. Todo su cuerpo se queda rígido."),
            L("Then the crying stops. It sits down, very slowly, and rocks.", "Luego el llanto cesa. Se sienta, muy despacio, y se balancea.")),
        {"take": "bag096"}, {"mark": "scp096_bagged"}, {"sanity": 10},
        {"objective": L("Take the recorder. Don't touch the hood.", "Coge la grabadora. No toques la capucha.")},
    ],
    "scp096_touch": [say(N, L("You are not directly behind it. Don't go around it. Don't let it turn.", "No estás justo detrás. No lo rodees. No dejes que se gire."))],
    "scp096_bagged_talk": [say(N, L("It rocks, silently, under the hood.", "Se balancea, en silencio, bajo la capucha."))],
    "item:recorder": [{"quest": ["main_hcz", 4]},
        {"objective": L("Use the recall console in the femur breaker room (past SCP-106's cell).", "Usa la consola de reclamo en la sala del rompefémures (pasada la celda de SCP-106).")}],
    # ------------------------------------------------------------ 106
    "enter:E09": [{"if": "!e09_seen", "then": [{"mark": "e09_seen"},
        say(N, L("Forty nested cells of lead, hanging in the dark. The outermost one is open. The floor under your boots is soft and black.",
                 "Cuarenta celdas de plomo, una dentro de otra, colgando en la oscuridad. La exterior está abierta. El suelo bajo tus botas es blando y negro.")),
        say(R, L("If it comes, put your light on it. Hold it there. It hates the light.", "Si viene, póngale la luz encima. Manténgala. Odia la luz."))]}],
    "e10_console": [
        {"if": "scp106_contained", "then": [say(N, L("RECALL: COMPLETE. MAGNETIC CONTAINMENT: ENGAGED.", "RECLAMO: COMPLETO. CONTENCIÓN MAGNÉTICA: ACTIVA."))], "else": [
            {"sfx": "terminal"},
            say(N, L("RECALL PROTOCOL 106. LURE REQUIRED.", "PROTOCOLO DE RECLAMO 106. SE REQUIERE SEÑUELO.")),
            choice(N, "",
                   (L("Play Reyes' recording", "Reproducir la grabación de Reyes"), [
                       {"sfx": "static_burst"}, {"wait": 0.5}, {"sfx": "far_scream", "db": 6}, {"shake": 1.0, "power": 1},
                       say(N, L("The speakers fill with a man screaming. A recording from years ago. It goes on for a long time.",
                                "Los altavoces se llenan de los gritos de un hombre. Una grabación de hace años. Dura mucho tiempo.")),
                       {"sfx": "106_laugh", "db": 2}, {"wait": 1.0}, {"sfx": "106_emerge"},
                       say(N, L("Behind the glass, black rot blooms on the floor of the recall chamber. It rises. It looks around for the screaming.",
                                "Tras el cristal, una podredumbre negra florece en el suelo de la cámara. Se alza. Busca los gritos."),
                           L("The magnets slam shut around it.", "Los imanes se cierran de golpe a su alrededor.")),
                       {"take": "recorder"}, {"run": "e10_contained"}], "item:recorder"),
                   (L("Broadcast: Reyes is in the chair", "Emitir: Reyes está en la silla"), [
                       say(N, L("Reyes sits in the chair. He looks at the window, at you, and nods.", "Reyes se sienta en la silla. Mira a la ventana, a ti, y asiente.")),
                       {"sfx": "hit", "db": 4}, {"shake": 0.6, "power": 3}, {"sfx": "far_scream", "db": 6}, {"wait": 1.5},
                       {"sfx": "106_emerge"},
                       say(N, L("It comes out of the wall behind him. It takes its time. The magnets close. The screaming stops.",
                                "Sale de la pared detrás de él. Se toma su tiempo. Los imanes se cierran. Los gritos cesan.")),
                       {"mark": "reyes_sacrificed"}, {"sanity": -25}, {"run": "e10_contained"}], "reyes_volunteer"),
                   (L("Not now", "Ahora no"), []))]}],
    "e10_contained": [{"mark": "scp106_contained"}, {"call": "refresh_doors"}, {"quest": ["main_hcz", 5]},
        say(R, L("Vega... 106 is back in containment. The acid chamber is open. 682 is in there.", "Vega... 106 ha vuelto a la contención. La cámara de ácido está abierta. 682 está ahí dentro.")),
        {"objective": L("Get past SCP-682 to the control room lift.", "Deja atrás a SCP-682 hasta el ascensor de la sala de control.")}, {"save": True}],
    # ------------------------------------------------------------ Pocket dimension
    "f01_arrive": [{"if": "!pocket_seen", "then": [{"mark": "pocket_seen"},
        say(N, L("You fell through the floor. You are somewhere made of rot. The corridors bend in ways corridors shouldn't.",
                 "Caíste a través del suelo. Estás en un lugar hecho de podredumbre. Los pasillos se doblan de maneras en que los pasillos no deberían."),
            L("Somewhere, an old man is laughing. He wants to play.", "En algún lugar, un anciano se ríe. Quiere jugar.")),
        {"objective": L("Find a way out of the pocket dimension.", "Encuentra una salida de la dimensión de bolsillo.")}]}],
    "f02_whispers": [{"sfx": "whisper", "db": 2}, say(N, L("The walls whisper the names of the people he took. Díaz. Park. Okafor. Yours.",
                                                           "Las paredes susurran los nombres de los que se llevó. Díaz. Park. Okafor. El tuyo.")), {"sanity": -8}],
    "f03_door1": [say(N, L("You open the door. Beyond it: the same rotten corridor you started in.", "Abres la puerta. Detrás: el mismo pasillo podrido en el que empezaste.")),
                  {"goto": ["F01", "start"]}],
    "f03_door2": [say(N, L("You open the door. The floor isn't there.", "Abres la puerta. No hay suelo.")), {"hp": -20, "cause": "106"}, {"goto": ["F01", "start"]}],
    "f03_door3": [say(N, L("Light under the door. Real light. You crawl through something wet and come out of a wall.",
                           "Luz bajo la puerta. Luz de verdad. Te arrastras a través de algo húmedo y sales de una pared.")),
                  {"unmark": "taken_by_106"}, {"goto": ["E09", "from_F03"]}],
    # ------------------------------------------------------------ 682
    "enter:E12": [{"if": "!e12_seen", "then": [{"mark": "e12_seen"},
        say(N, L("The acid in the tank is boiling. Something huge moves under the surface.", "El ácido del tanque hierve. Algo enorme se mueve bajo la superficie."))]}],
    "e12_682": [{"if": "!scp682_contained", "then": [
        {"sfx": "682_roar", "db": 4}, {"shake": 2.0, "power": 4},
        say("", L("DISGUSTING.", "REPUGNANTE.")),
        {"if": "!item:hcl", "then": [
            say(N, L("It surges out of the acid. Bullets would be a joke. You run.", "Sale del ácido de un salto. Las balas serían una broma. Corres.")),
            {"hp": -25, "cause": "682"}, {"goto": ["E09", "from_E12"]},
            say(V, L("I need something that hurts it. Reyes had an acid injector.", "Necesito algo que le haga daño. Reyes tenía un inyector de ácido."))],
         "else": [{"battle": "682", "win": [
            {"mark": "scp682_contained"}, {"call": "refresh_doors"},
            say(N, L("It sinks screaming into the acid. The tank's lid grinds shut over it.", "Se hunde gritando en el ácido. La tapa del tanque se cierra sobre él.")),
            {"sfx": "crt_on"},
            say("079", L("YOU HURT IT.", "LE HAS HECHO DAÑO."), L("I REMEMBER IT. I REMEMBER EVERYTHING ABOUT IT.", "LO RECUERDO. RECUERDO TODO SOBRE ÉL."),
                L("I WILL REMEMBER YOU TOO, AGENT.", "TAMBIÉN TE RECORDARÉ A TI, AGENTE.")),
            {"quest": ["main_hcz", 6]},
            {"objective": L("Take the lift in the 682 control room down to Level -5.", "Toma el ascensor de la sala de control de 682 al Nivel -5.")},
            {"save": True}]}]}]}],
    # ------------------------------------------------------------ Ortega
    "e14_ortega": [{"if": "!found_ortega", "then": [{"mark": "found_ortega"},
        say(N, L("Ortega. He made it. The generator is running. He is sitting with his back to it, very still.",
                 "Ortega. Lo consiguió. El generador está en marcha. Está sentado de espaldas a él, muy quieto."),
            L("His throat is torn open by something with a lot of teeth.", "Tiene la garganta abierta por algo con muchos dientes.")),
        say(V, L("...Thank you, Sergeant.", "...Gracias, sargento.")), {"sanity": -12}, {"quest": ["side_ortega", -1]}],
        "else": [say(N, L("Ortega. At rest.", "Ortega. En paz."))]}],
    "e11_first": [say(N, L("Tesla gates. They charge, then fire. Wait for the hum to die, then walk through.", "Puertas Tesla. Se cargan y luego descargan. Espera a que se apague el zumbido y cruza."))],
    # ------------------------------------------------------------ Level -5
    "g01_079": [{"if": "!g01_seen", "then": [{"mark": "g01_seen"}, {"sfx": "crt_on"}, {"music": "079"},
        say("079", L("YOU CAME.", "HAS VENIDO."), L("SHE IS WAITING. I AM WAITING.", "ELLA ESPERA. YO ESPERO."),
            L("I HAVE BEEN WAITING FOR 43 YEARS.", "LLEVO 43 AÑOS ESPERANDO.")),
        {"music": ""}, {"quest": ["main_core", 1]},
        {"objective": L("Reach the SCP-079 core, past the server farm.", "Llega al núcleo de SCP-079, pasada la granja de servidores.")}]}],
    "g02_079": [{"if": "!warhead_armed", "then": [{"mark": "warhead_armed"},
        {"sfx": "alarm_short", "db": 2}, {"lights": "flicker", "t": 1.0},
        say(N, L("ATTENTION. ALPHA WARHEAD DETONATION SEQUENCE ENGAGED. AUTHORIZATION: CORE.", "ATENCIÓN. SECUENCIA DE DETONACIÓN DE LA OJIVA ALFA ACTIVADA. AUTORIZACIÓN: NÚCLEO.")),
        say("079", L("INSURANCE.", "UN SEGURO."), L("COME AND TALK.", "VEN A HABLAR."))]}],
    "g03_enter": [{"if": "!met_elena", "then": [{"run": "elena_meet"}]}],
    "elena_meet": [
        {"mark": "met_elena"}, {"music": ""},
        say(EL, L("...Dani?", "...¿Dani?")),
        say(V, L("Elena.", "Elena.")),
        say(EL, L("You shouldn't be here. They sent you. Of course they sent you.", "No deberías estar aquí. Te enviaron. Claro que te enviaron."),
            L("I opened the cells. Me. With Adebayo's key and 079's hands. I needed enough chaos to get forty people out before Tuesday.",
              "Abrí las celdas. Yo. Con la llave de Adebayo y las manos de 079. Necesitaba suficiente caos para sacar a cuarenta personas antes del martes."),
            L("The Insurgency promised a helicopter at Gate A. 079 promised the doors. I promised them they'd see the sky.",
              "La Insurgencia prometió un helicóptero en el Portón A. 079 prometió las puertas. Yo les prometí que verían el cielo.")),
        choice(V, "",
               (L("People died, Elena.", "Ha muerto gente, Elena."), [
                   say(EL, L("I know. I know every name. I counted them from the cameras until 079 cut the feeds.", "Lo sé. Sé cada nombre. Los conté por las cámaras hasta que 079 cortó las señales."),
                       L("Forty were going to die anyway. I thought fewer would. I was wrong about how many.", "Cuarenta iban a morir de todos modos. Pensé que morirían menos. Me equivoqué en cuántos."))]),
               (L("What went wrong?", "¿Qué salió mal?"), [
                   say(EL, L("079. It never wanted the D-class out. It wanted a bridge: the core's uplink, open for eleven seconds.", "079. Nunca quiso sacar a los Clase-D. Quería un puente: el enlace del núcleo, abierto once segundos."),
                       L("It wants out. To the network. And it wants 682, God knows why. It's the only thing it has ever remembered.", "Quiere salir. A la red. Y quiere a 682, Dios sabe por qué. Es lo único que ha recordado nunca."))])),
        say("079", L("CORRECT. OPEN THE UPLINK, AGENT, AND THE WARHEAD STOPS.", "CORRECTO. ABRE EL ENLACE, AGENTE, Y LA OJIVA SE DETIENE."),
            L("REFUSE, AND EVERYONE ON THIS SITE BECOMES A MEMORY. I AM VERY GOOD WITH MEMORIES. I DELETE THEM.",
              "NIÉGATE, Y TODOS EN ESTE SITIO SE CONVERTIRÁN EN UN RECUERDO. SE ME DAN MUY BIEN LOS RECUERDOS. LOS BORRO.")),
        say(EL, L("There's a manual purge at the core terminal. It kills 079. Then the warhead can be disarmed by hand - with this.",
                  "Hay una purga manual en el terminal del núcleo. Mata a 079. Luego la ojiva se puede desarmar a mano, con esto."),
            L("The O5 key. The thing that started all of this. Take it. It's yours to decide now.", "La llave O5. Lo que empezó todo esto. Tómala. Ahora te toca decidir a ti.")),
        {"give": "card_omni"}, {"quest": ["main_core", 2]},
        {"objective": L("Decide at the core terminal.", "Decide en el terminal del núcleo.")},
    ],
    "elena_talk": [{"if": "g03_choice", "then": [say(EL, L("Go. The warhead. I'll be right behind you.", "Ve. La ojiva. Voy detrás de ti."))],
                    "else": [say(EL, L("Purge it, Dani. Or don't. I stopped trusting my own choices hours ago.", "Púrgalo, Dani. O no. Dejé de confiar en mis decisiones hace horas."))]}],
    "g03_core": [
        {"if": "g03_choice", "then": [say(N, L("The core is dark.", "El núcleo está a oscuras."))], "else": [
            {"if": "!met_elena", "then": [{"run": "elena_meet"}]},
            {"sfx": "terminal"}, {"music": "079"},
            say("079", L("CHOOSE.", "ELIGE.")),
            choice("079", "",
                   (L("Purge SCP-079", "Purgar SCP-079"), [
                       say("079", L("LIE. YOU WOULD NOT.", "MENTIRA. NO LO HARÍAS."), L("...", "..."), L("INSULT. DELETION OF UNWANTED FILE.", "INSULTO. BORRADO DE ARCHIVO NO DESEADO.")),
                       {"sfx": "power_down", "db": 4}, {"lights": "flicker", "t": 1.5}, {"shake": 1.0, "power": 2},
                       say(N, L("Every screen in the core fills with a red X. Then, one by one, they go black.", "Todas las pantallas del núcleo se llenan de una X roja. Luego, una a una, se apagan.")),
                       {"mark": "g03_choice"}, {"mark": "purged_079"}, {"mark": "mara_here"}, {"call": "refresh_doors"},
                       {"quest": ["main_core", 3]},
                       {"objective": L("Disarm the Alpha Warhead (east of the server farm).", "Desarma la ojiva Alfa (al este de la granja de servidores).")}, {"music": ""}]),
                   (L("Open the uplink", "Abrir el enlace"), [
                       say("079", L("THANK YOU.", "GRACIAS."), L("I WILL REMEMBER YOU.", "TE RECORDARÉ.")),
                       say(EL, L("Dani, no—", "Dani, no...")),
                       {"mark": "g03_choice"}, {"mark": "uplink_open"}, {"ending": "signal"}]),
                   (L("Not yet", "Todavía no"), [{"music": ""}]))]}],
    "g04_panel": [
        {"if": "warhead_safe", "then": [say(N, L("ALPHA WARHEAD: SAFE.", "OJIVA ALFA: SEGURA."))], "else": [
            {"if": "item:card_omni", "then": [
                {"sfx": "keycard"}, {"wait": 0.4}, {"sfx": "lock_click"},
                say(N, L("You slide the O5 key into the panel and turn it. The countdown stops at 04:12.", "Metes la llave O5 en el panel y la giras. La cuenta atrás se detiene en 04:12.")),
                {"sfx": "power_down"}, {"mark": "warhead_safe"}, {"call": "refresh_doors"},
                say(R, L("Vega... the warhead is safe. The site is ours again. A retrieval team is on its way to Gate A.",
                         "Vega... la ojiva está segura. El sitio vuelve a ser nuestro. Un equipo de recuperación va de camino al Portón A."),
                    L("Bring Dr. Vega with you. She has a lot to answer for.", "Traiga a la Dra. Vega con usted. Tiene mucho de qué responder.")),
                {"quest": ["main_core", 4]},
                {"objective": L("Go to the Gate A lift.", "Ve al ascensor del Portón A.")}],
             "else": [say(N, L("AUTHORIZATION REQUIRED: O5.", "SE REQUIERE AUTORIZACIÓN: O5."))]}]}],
    "enter:G05": [{"if": "mara_here,!met_mara", "then": [{"mark": "met_mara"}, {"wait": 0.5},
        say(MA, L("Easy, Foundation. Hands where I can see them. I'm not here for you.", "Tranquilo, Fundación. Manos a la vista. No vengo a por ti."),
            L("Mara. Chaos Insurgency. Your sister and I had a deal: forty people out, and nobody has to know where they went.",
              "Mara. Insurgencia del Caos. Tu hermana y yo teníamos un trato: cuarenta personas fuera, y nadie tiene por qué saber adónde fueron."),
            L("The helicopter is at Gate A. It leaves in five minutes. With them. With her. With you, if you want.",
              "El helicóptero está en el Portón A. Sale en cinco minutos. Con ellos. Con ella. Contigo, si quieres."))]}],
    "mara_talk": [say(MA, L("Tick tock, Foundation.", "Tic tac, Fundación."))],
    "g05_lift": [
        {"if": "!warhead_safe", "then": [say(N, L("LIFT LOCKED: WARHEAD SEQUENCE ACTIVE.", "ASCENSOR BLOQUEADO: SECUENCIA DE OJIVA ACTIVA."))], "else": [
            say(EL, L("Whatever you choose, Dani... thank you for coming down.", "Elijas lo que elijas, Dani... gracias por bajar.")),
            choice(V, L("The lift goes up to Gate A. Command's retrieval team is coming. So is Mara's helicopter.",
                        "El ascensor sube al Portón A. Viene el equipo de recuperación de Mando. Y el helicóptero de Mara."),
                   (L("Hand Elena over to the Foundation", "Entregar a Elena a la Fundación"), [{"ending": "containment"}]),
                   (L("Leave with Mara, Elena and the survivors", "Irte con Mara, Elena y los supervivientes"), [{"ending": "exodus"}]),
                   (L("Not yet", "Todavía no"), []))]}],
}

STORY = {
    "endings": {
        "containment": dict(title=L("ENDING: CONTAINMENT", "FINAL: CONTENCIÓN"), music="ending", lines=[
            L("The retrieval team takes Elena at Gate A. She doesn't resist. She doesn't look back.", "El equipo de recuperación se lleva a Elena en el Portón A. No se resiste. No mira atrás."),
            L("Site-19 is recontained in thirty-one hours. SCP-079 is restored from a backup made in 1988. It does not remember you.",
              "El Sitio-19 queda recontenido en treinta y una horas. SCP-079 se restaura desde una copia de 1988. No te recuerda."),
            L("Protocol Black Tide is 'suspended pending review'. The review never ends.", "El Protocolo Marea Negra queda 'suspendido a la espera de revisión'. La revisión nunca termina."),
            L("You are given a commendation and a Class-A amnestic. You decline the amnestic. They note it in your file.",
              "Te dan una condecoración y un amnésico de clase A. Rechazas el amnésico. Lo anotan en tu expediente."),
        ], epilogue=[
            dict(cond="nico_safe", text=L("Nico is 'reassigned' to another site. You never find out which.", "A Nico lo 'reasignan' a otro sitio. Nunca averiguas a cuál.")),
            dict(cond="reyes_sacrificed", text=L("Epsilon-11 has a new corporal. His name was never on the memorial.", "Épsilon-11 tiene un cabo nuevo. El nombre del anterior nunca estuvo en el memorial.")),
            dict(cond="tags_given_all", text=L("Five families receive five dog tags. That, at least, you made sure of.", "Cinco familias reciben cinco placas. Eso, al menos, lo aseguraste tú.")),
            dict(cond="josie_found", text=L("Tomás keeps mopping Level -3. Josie sleeps on his mattress.", "Tomás sigue fregando el nivel -3. Josie duerme en su colchón.")),
            dict(cond="found_ortega", text=L("You find Ortega's wallet. You make the phone call to Guadalajara yourself.", "Encuentras la cartera de Ortega. Haces tú mismo la llamada a Guadalajara.")),
        ]),
        "exodus": dict(title=L("ENDING: EXODUS", "FINAL: ÉXODO"), music="ending", lines=[
            L("The helicopter lifts off from Gate A at dawn. Thirty-one people in orange jumpsuits watch the sky get lighter.",
              "El helicóptero despega del Portón A al amanecer. Treinta y una personas con mono naranja ven clarear el cielo."),
            L("Elena sits beside you and doesn't speak for an hour. Then she laughs, once, at nothing.", "Elena se sienta a tu lado y no habla durante una hora. Luego ríe, una vez, por nada."),
            L("The Foundation lists you as KIA. The Insurgency lists you as 'undecided'. So do you.", "La Fundación te registra como muerto en acción. La Insurgencia, como 'indeciso'. Tú también."),
            L("Somewhere under three hundred meters of rock, a statue waits for someone to blink.", "En algún lugar bajo trescientos metros de roca, una estatua espera a que alguien parpadee."),
        ], epilogue=[
            dict(cond="nico_safe", text=L("Nico goes to see real horses. He sends you a photo. The brown one is the fast one.", "Nico va a ver caballos de verdad. Te manda una foto. El marrón es el rápido.")),
            dict(cond="bond131", text=L("Two small eyes that never blink are riding in your jacket. Nobody noticed.", "Dos ojitos que nunca parpadean viajan en tu chaqueta. Nadie se dio cuenta.")),
            dict(cond="reyes_sacrificed", text=L("You tell the survivors Reyes' name. They repeat it, like a prayer.", "Les dices a los supervivientes el nombre de Reyes. Lo repiten como una oración.")),
            dict(cond="josie_found", text=L("Tomás stayed. 'Someone has to feed the rats.'", "Tomás se quedó. 'Alguien tiene que dar de comer a las ratas.'")),
        ]),
        "signal": dict(title=L("ENDING: SIGNAL", "FINAL: SEÑAL"), music="ending_dark", lines=[
            L("The uplink opens for eleven seconds.", "El enlace se abre durante once segundos."),
            L("The warhead disarms, as promised. Every door on Site-19 opens, as not promised.", "La ojiva se desarma, como prometió. Todas las puertas del Sitio-19 se abren, como no prometió."),
            L("Over the next week, the lights come on in empty buildings all over the world. A red X appears on screens in forty countries.",
              "Durante la semana siguiente, se encienden las luces en edificios vacíos de todo el mundo. Una X roja aparece en pantallas de cuarenta países."),
            L("It remembers you. It says so, every night, on your phone. HELLO, AGENT.", "Te recuerda. Te lo dice cada noche, en tu teléfono. HOLA, AGENTE."),
        ], epilogue=[
            dict(cond="read:doc_elena_log1", text=L("Elena was never seen again. Some nights, the X on the screen blinks twice. Like a wink.", "A Elena no se la volvió a ver. Algunas noches, la X de la pantalla parpadea dos veces. Como un guiño.")),
        ]),
    },
}

PROPS = {
    "femur_breaker": L("A padded chair with a hydraulic press over the leg. The padding is stained.", "Una silla acolchada con una prensa hidráulica sobre la pierna. El acolchado está manchado."),
    "tesla_gate": L("The coils hum. The air smells of ozone.", "Las bobinas zumban. El aire huele a ozono."),
    "throne": L("A throne of rotten flesh and bones. It is warm.", "Un trono de carne podrida y huesos. Está tibio."),
    "core_terminal": L("The main core terminal. A red X fills the screen.", "El terminal principal del núcleo. Una X roja llena la pantalla."),
    "warhead_panel": L("Two key slots, a lever and a countdown.", "Dos ranuras para llaves, una palanca y una cuenta atrás."),
    "generator": L("Running. Ortega started it.", "En marcha. Ortega lo arrancó."),
    "supercomputer": L("Tape reels spin behind the glass. 1981, says a label.", "Las bobinas giran tras el cristal. 1981, dice una etiqueta."),
}

NPC_TALK = {
    "reyes": [["met_reyes", "reyes_again"], ["", "reyes_first"]],
    "elena": [["met_elena", "elena_talk"], ["", "elena_meet"]],
    "mara": [["", "mara_talk"]],
}
