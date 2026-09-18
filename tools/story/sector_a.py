"""Act I — Entrance Zone. Prologue, Ortega, 079's first contact, Nico."""
from common import L, say, choice

N = ""        # narration
R = "radio"   # Command (Operator Kessler)
V = "vega"

QUESTS = {
    "main_breach": dict(main=True, name=L("Containment Breach", "Brecha de contención"), stages=[
        L("Force open the doors of Elevator B.", "Fuerza las puertas del ascensor B."),
        L("Find Site Security, west of reception.", "Encuentra el puesto de seguridad, al oeste de recepción."),
        L("Reach the Light Containment checkpoint at the end of the east corridor.", "Llega al control de Contención Ligera al final del pasillo este."),
        L("Go through decontamination into Light Containment.", "Pasa la descontaminación hacia Contención Ligera."),
    ]),
    "side_nico": dict(name=L("D-4417", "D-4417"), stages=[
        L("Ortega heard a D-class on the cafeteria intercom. Find him.", "Ortega oyó a un Clase-D por el intercomunicador de la cafetería. Encuéntralo."),
        L("Take Nico to the security checkpoint.", "Lleva a Nico al puesto de seguridad."),
    ]),
    "side_elena": dict(name=L("Elena", "Elena"), stages=[
        L("Your sister's office is 2-B, in Administration. The door needs her key.", "La oficina de tu hermana es la 2-B, en Administración. La puerta necesita su llave."),
        L("Elena worked on something called Project Threshold. Find out what it is.", "Elena trabajaba en algo llamado Proyecto Umbral. Averigua qué es."),
        L("079 says Elena is alive on Level -5. Keep going down.", "079 dice que Elena está viva en el Nivel -5. Sigue bajando."),
    ]),
    "side_locker": dict(name=L("Locker 7", "Taquilla 7"), stages=[
        L("Locker 7 in the dormitories has a 4-digit lock. Someone must have written it down.", "La taquilla 7 de los dormitorios tiene un candado de 4 cifras. Alguien lo habrá apuntado."),
    ]),
}

DOCS = {
    "doc_welcome": dict(title=L("Welcome to Site-19", "Bienvenido al Sitio-19"), body=L(
        "Welcome to Site-19, the largest containment facility of the SCP Foundation.\n\n"
        "SECURE. CONTAIN. PROTECT.\n\n"
        "- Wear your ID badge at all times.\n- Report anything unusual. Unusual is our business.\n"
        "- If you hear an alarm, you are not in a drill.\n- Do not look at, speak to, or feed anything you were not "
        "assigned to.\n\nRemember: the door behind you is there to keep something in. So is the one in front of you.",
        "Bienvenido al Sitio-19, la mayor instalación de contención de la Fundación SCP.\n\n"
        "ASEGURAR. CONTENER. PROTEGER.\n\n"
        "- Lleve su identificación en todo momento.\n- Informe de cualquier cosa inusual. Lo inusual es nuestro trabajo.\n"
        "- Si oye una alarma, no es un simulacro.\n- No mire, hable ni alimente a nada que no le hayan asignado.\n\n"
        "Recuerde: la puerta detrás de usted está ahí para mantener algo dentro. La de delante, también.")),
    "doc_memo_threshold": dict(title=L("Memo: Project Threshold", "Memorándum: Proyecto Umbral"), body=L(
        "FROM: Site Director Aldana\nTO: Dr. E. Vega, Threshold lead\n\n"
        "The transfer of SCP-079 from Site-15 is approved. It will be housed in the Level -5 core under full air gap. "
        "You have the budget you asked for. You do not have my trust.\n\n"
        "Every session with 079 is to be logged. Every one. It forgets in 24 hours; we do not.\n\n"
        "P.S. Stop asking about Black Tide. That is not your department.",
        "DE: Directora del Sitio Aldana\nPARA: Dra. E. Vega, responsable de Umbral\n\n"
        "Aprobado el traslado de SCP-079 desde el Sitio-15. Se alojará en el núcleo del Nivel -5 con aislamiento total. "
        "Tiene el presupuesto que pidió. No tiene mi confianza.\n\n"
        "Cada sesión con 079 debe registrarse. Todas. Él olvida en 24 horas; nosotros no.\n\n"
        "P.D. Deje de preguntar por Marea Negra. No es su departamento.")),
    "doc_black_tide_redacted": dict(title=L("Order: Protocol Black Tide", "Orden: Protocolo Marea Negra"), body=L(
        "CLASSIFIED - O5 EYES ONLY\n\nPROTOCOL BLACK TIDE\n\nObjective: ████████ termination trials, SCP-682.\n"
        "Resources: D-class personnel, Site-19 Block ██. Estimated consumption: ███ subjects.\n"
        "On completion: Block ██ to be ████████ with Class-A amnestics and ███████████.\n\n"
        "Authorized: O5-█\n\n(Someone has circled the blacked-out words in red pen, over and over.)",
        "CLASIFICADO - SOLO O5\n\nPROTOCOLO MAREA NEGRA\n\nObjetivo: pruebas de terminación ████████, SCP-682.\n"
        "Recursos: personal Clase-D, Sitio-19 Bloque ██. Consumo estimado: ███ sujetos.\n"
        "Al completarse: el Bloque ██ será ████████ con amnésicos de clase A y ███████████.\n\n"
        "Autorizado: O5-█\n\n(Alguien ha rodeado las palabras tachadas con bolígrafo rojo, una y otra vez.)"), sanity=-3),
    "doc_elena_log1": dict(title=L("Elena's notebook, page 1", "Cuaderno de Elena, página 1"), body=L(
        "Day 212. 079 asked about 682 again. It does not ask about anything else it remembers, because it does not remember "
        "anything else. One memory it keeps. Only one. Why that one?\n\n"
        "Day 219. I found the Black Tide order in the director's outbox. The blacked-out word in the first line is "
        "'extended'. Extended termination trials. They are going to feed the D-block to 682, one by one, and see what it "
        "becomes.\n\nDay 220. I can't sleep. I keep thinking about the kid in cell 17, who draws horses.\n\n"
        "If you are reading this, Dani: I'm sorry. I know what I'm going to do.",
        "Día 212. 079 volvió a preguntar por 682. No pregunta por nada más que recuerde, porque no recuerda nada más. "
        "Un recuerdo guarda. Solo uno. ¿Por qué ese?\n\n"
        "Día 219. Encontré la orden de Marea Negra en la bandeja de salida de la directora. La palabra tachada de la "
        "primera línea es 'extendidas'. Pruebas de terminación extendidas. Van a darle el bloque D a 682, uno a uno, y "
        "ver en qué se convierte.\n\nDía 220. No puedo dormir. Pienso en el chico de la celda 17, el que dibuja caballos.\n\n"
        "Si estás leyendo esto, Dani: lo siento. Sé lo que voy a hacer.")),
    "doc_dorm_note": dict(title=L("Note under a pillow", "Nota bajo una almohada"), body=L(
        "Maria - they moved me to the LCZ rotation. The statue. You're never alone with it, it's the rule, three of us "
        "and two always looking. Keller blinks too much. I don't sleep much.\n\nIf anything happens, the combination of "
        "my locker is the day we met. You know it. (It's 0-3-1-2, I know you forget things.)\n\n- T.",
        "María - me pasaron al turno de la ZCL. La estatua. Nunca estás solo con ella, es la regla, tres y dos siempre "
        "mirando. Keller parpadea demasiado. No duermo mucho.\n\nSi pasa algo, la combinación de mi taquilla es el día que "
        "nos conocimos. Ya lo sabes. (Es 0-3-1-2, sé que olvidas las cosas.)\n\n- T.")),
    "doc_infirmary_log": dict(title=L("Infirmary log", "Registro de enfermería"), body=L(
        "03:31 - Patient: J. Okafor, 24, security. Admitted with black stains on both hands. Claims 'the wall grabbed me'.\n"
        "03:40 - Stains spreading to forearms. Tissue necrotic. Smell of rot.\n"
        "03:52 - Patient's hair has gone white. Skin thinning. Vitals consistent with a man of seventy.\n"
        "04:05 - Something is coming through the floor under bed 4. Evacuating.",
        "03:31 - Paciente: J. Okafor, 24, seguridad. Ingresa con manchas negras en ambas manos. Dice que 'la pared le "
        "agarró'.\n03:40 - Las manchas se extienden a los antebrazos. Tejido necrótico. Olor a podredumbre.\n"
        "03:52 - El pelo del paciente se ha vuelto blanco. La piel se adelgaza. Constantes de un hombre de setenta años.\n"
        "04:05 - Algo está atravesando el suelo bajo la cama 4. Evacuamos."), sanity=-4),
    "doc_locker_letter": dict(title=L("Letter in locker 7", "Carta en la taquilla 7"), body=L(
        "If they ask you to stand in the room with the statue, say no. I know what the contract says. Say no anyway. "
        "They don't count the ones who blink. - T.",
        "Si te piden estar en la sala con la estatua, di que no. Sé lo que dice el contrato. Di que no igualmente. No "
        "cuentan a los que parpadean. - T.")),
}

EVENTS = {
    # ------------------------------------------------------------ prologue
    "enter:A01": [
        {"if": "!intro_done", "then": [
            {"music": "prologue"},
            say(N, L("SITE-19. 03:14. CASCADE CONTAINMENT BREACH.", "SITIO-19. 03:14. BRECHA DE CONTENCIÓN EN CASCADA."),
                L("Service Elevator B. Descending. Three hundred meters of rock between you and the sky.",
                  "Ascensor de servicio B. Descendiendo. Trescientos metros de roca entre tú y el cielo.")),
            say(R, L("Agent Vega, this is Command. Kessler. Do you copy?", "Agente Vega, aquí Mando. Kessler. ¿Me recibe?"),
                L("At 03:12 every containment cell on Levels -2 to -5 opened at once. Not a fault. An order.",
                  "A las 03:12 se abrieron a la vez todas las celdas de contención de los niveles -2 a -5. No fue un fallo. Fue una orden."),
                L("Epsilon-11 went in six hours ago. We lost them on Level -4.", "Épsilon-11 entró hace seis horas. Los perdimos en el Nivel -4."),
                L("You are all we have left. Reach Site Security and find out who is still breathing.",
                  "Usted es todo lo que nos queda. Llegue al puesto de seguridad y averigüe quién sigue respirando.")),
            say(V, L("My sister is down there, Kessler.", "Mi hermana está ahí abajo, Kessler.")),
            say(R, L("Dr. Elena Vega. I know. She is not your mission, agent.", "La Dra. Elena Vega. Lo sé. No es su misión, agente.")),
            {"sfx": "elevator_stop"}, {"shake": 1.2, "power": 4}, {"lights": "flicker", "t": 1.2},
            say(R, L("Vega? ...your signal... breaking up... the lower... are not...", "¿Vega? ...su señal... se corta... los niveles... no son...")),
            {"sfx": "radio_static", "db": -6},
            say(N, L("The elevator has stopped between floors. The doors are jammed.", "El ascensor se ha detenido. Las puertas están atascadas.")),
            {"give": "radio"}, {"give": "pistol"}, {"give": "ammo", "n": 6}, {"give": "bandage"},
            {"quest": ["main_breach", 1]}, {"mark": "intro_done"},
            {"objective": L("Force open the elevator doors.", "Fuerza las puertas del ascensor.")},
            {"music": ""},
        ]},
    ],
    "a01_pry": [
        {"sfx": "metal_strain"}, {"shake": 0.6, "power": 2}, {"wait": 0.4},
        {"sfx": "metal_screech"}, {"mark": "a01_forced"}, {"door": "A01_cab", "open": True},
        say(N, L("The doors grind apart. The air beyond smells of dust and copper.", "Las puertas ceden con un chirrido. El aire de fuera huele a polvo y a cobre.")),
        {"quest": ["main_breach", 2]},
        {"objective": L("Find Site Security (west of reception).", "Encuentra el puesto de seguridad (al oeste de recepción).")},
    ],
    # ------------------------------------------------------------ reception
    "enter:A02": [
        {"if": "!seen_reception", "then": [
            {"mark": "seen_reception"}, {"wait": 0.6},
            say(V, L("The receptionist didn't make it to the door.", "La recepcionista no llegó a la puerta."),
                L("Someone dragged something heavy toward Security. Or someone.", "Alguien arrastró algo pesado hacia Seguridad. O a alguien.")),
        ]},
    ],
    "a02_terminal": [
        {"sfx": "terminal"},
        say(N, L("SITE-19 // LOCKDOWN - PROTOCOL 12-GAMMA", "SITIO-19 // CONFINAMIENTO - PROTOCOLO 12-GAMMA"),
            L("03:12:07  ALL CONTAINMENT CELLS: OPEN.  AUTHORIZATION: O5-[UNREADABLE].", "03:12:07  TODAS LAS CELDAS: ABIERTAS.  AUTORIZACIÓN: O5-[ILEGIBLE]."),
            L("03:12:09  GATE A / GATE B: SEALED.  ELEVATORS: EMERGENCY ONLY.", "03:12:09  PORTÓN A / PORTÓN B: SELLADOS.  ASCENSORES: SOLO EMERGENCIA."),
            L("03:12:10  MESSAGE FROM CORE: HELLO.", "03:12:10  MENSAJE DEL NÚCLEO: HOLA.")),
        {"mark": "saw_lockdown"},
    ],
    # ------------------------------------------------------------ security
    "enter:A03": [
        {"if": "follow:nico,!nico_safe", "then": [{"run": "nico_arrives_security"}]},
    ],
    "ortega_first": [
        {"mark": "met_ortega"},
        say("ortega", L("Don't— Foundation. You're Foundation. Thank God.", "No— Fundación. Eres de la Fundación. Gracias a Dios."),
            L("Sergeant Ortega, Security. Something opened the cells at twelve past three. Everything. At once.",
              "Sargento Ortega, Seguridad. Algo abrió las celdas a las tres y doce. Todo. A la vez."),
            L("I watched it on the cameras. The statue, from LCZ. It was in the east corridor, and then it was in the dorms.",
              "Lo vi en las cámaras. La estatua de la ZCL. Estaba en el pasillo este y luego estaba en los dormitorios."),
            L("It doesn't walk. You just look away and it's closer.", "No camina. Solo apartas la vista y está más cerca.")),
        choice("ortega", L("What do you need?", "¿Qué necesitas?"),
               (L("Who opened the cells?", "¿Quién abrió las celdas?"), [
                   say("ortega", L("The order came from inside. An O5 code. Nobody from the Council would ever do that.",
                                   "La orden vino de dentro. Un código O5. Nadie del Consejo haría algo así."))]),
               (L("Have you seen Dr. Elena Vega?", "¿Has visto a la Dra. Elena Vega?"), [
                   say("ortega", L("Vega... Threshold. She went down to the core an hour before it all started. With a trolley of hard drives.",
                                   "Vega... Umbral. Bajó al núcleo una hora antes de que empezara todo. Con un carrito de discos duros."),
                       L("Same name as you. Family?", "Mismo apellido que tú. ¿Familia?")),
                   say(V, L("Sister.", "Hermana.")), {"quest": ["side_elena", 1]}]),
               (L("Can you walk?", "¿Puedes caminar?"), [
                   say("ortega", L("Not far. Something took a bite out of my leg in the stairwell. I'll hold this post.",
                                   "No mucho. Algo me arrancó un trozo de pierna en la escalera. Aguantaré este puesto."))])),
        say("ortega", L("Take my card. Level 1 opens the east wing and the LCZ checkpoint.", "Toma mi tarjeta. El nivel 1 abre el ala este y el control de la ZCL."),
            L("And... there's a kid. A D-class. He was screaming on the cafeteria intercom an hour ago. Then he stopped.",
              "Y... hay un chico. Un Clase-D. Estaba gritando por el intercomunicador de la cafetería hace una hora. Luego paró."),
            L("They're prisoners, but they're people. Bring him here if he's alive.", "Son presos, pero son personas. Tráelo aquí si sigue vivo.")),
        {"give": "card_1"}, {"give": "battery"},
        {"quest": ["side_nico", 1]}, {"quest": ["main_breach", 3]},
        {"objective": L("Reach the Light Containment checkpoint (east corridor).", "Llega al control de Contención Ligera (pasillo este).")},
    ],
    "ortega_again": [
        say("ortega", L("The LCZ checkpoint is at the far end of the east corridor. Decontamination takes a minute. Don't panic.",
                        "El control de la ZCL está al fondo del pasillo este. La descontaminación tarda un minuto. No te asustes.")),
        {"if": "quest:side_nico:1,!nico_safe", "then": [say("ortega", L("The kid. The cafeteria. Please.", "El chico. La cafetería. Por favor."))]},
        {"if": "!ortega_heal", "then": [say("ortega", L("Here, you're bleeding. Hold still.", "Toma, estás sangrando. Quieto.")),
                                        {"hp": 40}, {"mark": "ortega_heal"}]},
    ],
    "ortega_after_nico": [
        say("ortega", L("You brought him. I owe you one, Vega.", "Lo trajiste. Te debo una, Vega."),
            L("He won't stop talking about his cell mate in the D-block. Tell him the Foundation will get everyone out.",
              "No para de hablar de su compañero de celda en el bloque D. Dile que la Fundación sacará a todos."),
            L("Even if neither of us believes it.", "Aunque ninguno de los dos lo crea.")),
    ],
    "ortega_late": [say("ortega", L("Go. I'll keep the lights on as long as I can.", "Vete. Mantendré las luces encendidas todo lo que pueda."))],
    "a03_cctv": [
        {"sfx": "crt_on"},
        say(N, L("CAM 04 - Cafeteria. Rats on the tables. Something shifts behind the kitchen door.",
                 "CÁM 04 - Cafetería. Ratas sobre las mesas. Algo se mueve tras la puerta de la cocina."),
            L("CAM 11 - LCZ, corridor 2. A grey figure stands in the middle of the hall.",
              "CÁM 11 - ZCL, pasillo 2. Una figura gris de pie en mitad del pasillo."),
            L("CAM 11 - The corridor is empty.", "CÁM 11 - El pasillo está vacío."),
            L("CAM 19 - HCZ. Static. Under the static, a sound like breathing.", "CÁM 19 - ZCP. Estática. Bajo la estática, algo como una respiración."),
            L("CAM 23 - Level -5, core. A woman in a lab coat looks straight into the lens.",
              "CÁM 23 - Nivel -5, núcleo. Una mujer con bata mira directamente a la lente.")),
        {"sfx": "static_burst"}, {"flash": 1, "color": "#9ab0c0"},
        say(V, L("Elena...", "Elena...")),
        say(N, L("The feed cuts to a red X.", "La imagen se corta en una X roja.")),
        {"mark": "saw_elena_cam"},
    ],
    "save_terminal": [
        {"sfx": "terminal"},
        say(N, L("You log your status into the site record. (Progress saved.)", "Registras tu estado en el sistema del sitio. (Progreso guardado.)")),
        {"save": True},
    ],
    # --------------------------------------------------------- east corridor
    "a04_first_body": [
        say(N, L("A security officer. Face down. His neck is turned all the way around.", "Un agente de seguridad. Boca abajo. El cuello girado del todo.")),
        say(R, L("...Vega, reading you again. Describe the body.", "...Vega, vuelvo a recibirle. Describa el cadáver.")),
        say(V, L("Broken neck. Clean. No bullets fired.", "Cuello roto. Limpio. Sin disparos.")),
        say(R, L("SCP-173. It moves when no one is looking. If you see it, do not look away. Do not blink if you can help it.",
                 "SCP-173. Se mueve cuando nadie lo mira. Si lo ve, no aparte la vista. No parpadee si puede evitarlo.")),
        {"sanity": -4},
    ],
    "enter:A04": [
        {"if": "met_ortega,!a10_open", "then": [{"run": "a04_079_invite"}]},
    ],
    "a04_079_invite": [
        {"wait": 1.0}, {"sfx_at": ["door_open", 46, 7], "db": 2},
        {"mark": "a10_open"}, {"call": "refresh_doors"},
        say(N, L("Down the corridor, the server room door slides open by itself. Its light is green.",
                 "Al fondo del pasillo, la puerta de la sala de servidores se abre sola. Su luz está en verde.")),
    ],
    # --------------------------------------------------------- offices
    "a05_cabinet": [
        {"if": "!a05_cabinet_done", "then": [
            say(N, L("Personnel files. Most drawers were emptied in a hurry.", "Expedientes del personal. Casi todos los cajones se vaciaron con prisa."),
                L("Taped under the top drawer: two quarters and a note - 'for the machine, don't tell Aldana'.",
                  "Pegado bajo el cajón superior: dos monedas y una nota - 'para la máquina, no se lo digas a Aldana'.")),
            {"give": "coin", "n": 2}, {"mark": "a05_cabinet_done"}], "else": [
            say(N, L("Nothing else useful.", "Nada más útil."))]},
    ],
    "item:office_key": [{"quest": ["side_elena", 1]}],
    "enter:A06": [
        {"if": "!a06_seen", "then": [
            {"mark": "a06_seen"}, {"wait": 0.5},
            say(V, L("Her coat is still on the chair. She always left it there when she meant to come back.",
                     "Su abrigo sigue en la silla. Siempre lo dejaba ahí cuando pensaba volver.")),
            {"quest": ["side_elena", 2]}]},
    ],
    "a06_whiteboard": [
        say(N, L("THRESHOLD - 079 <-> 682.  'WHY ONLY THIS MEMORY?'", "UMBRAL - 079 <-> 682.  '¿POR QUÉ SOLO ESTE RECUERDO?'"),
            L("Below, in a hurried hand: 'Black Tide = feeding. D-block = 40 people. Tuesday.'",
              "Debajo, con letra apresurada: 'Marea Negra = alimentar. Bloque D = 40 personas. Martes.'"),
            L("The word TUESDAY has been underlined until the marker ran dry.", "La palabra MARTES está subrayada hasta que se secó el rotulador.")),
    ],
    "a06_photo": [
        say(N, L("A photo in a cracked frame. Two kids on a beach, squinting at the sun. The girl is holding the camera.",
                 "Una foto en un marco roto. Dos niños en una playa, entornando los ojos al sol. La niña sostiene la cámara.")),
        say(V, L("She always said someone had to remember what things looked like.", "Siempre decía que alguien tenía que recordar cómo eran las cosas.")),
        {"sanity": 6},
    ],
    # --------------------------------------------------------- cafeteria / Nico
    "a07_kitchen_noise": [
        {"sfx": "pans_fall"}, {"shake": 0.3, "power": 1},
        say(N, L("Something clatters in the kitchen. Then silence. Then, very quietly, someone crying.",
                 "Algo cae en la cocina. Luego silencio. Luego, muy bajito, alguien llorando.")),
    ],
    "nico_first": [
        {"mark": "met_nico"},
        say("nico", L("Don't! Don't— you're not one of them. You're not grey.", "¡No! No... no eres uno de ellos. No eres gris."),
            L("I'm D-4417. Nico. Nicolás. I'm twenty-one, I'm not supposed to be here, I was supposed to be out in March.",
              "Soy D-4417. Nico. Nicolás. Tengo veintiún años, no debería estar aquí, salía en marzo.")),
        choice("nico", "",
               (L("I'm Foundation. I'll get you out.", "Soy de la Fundación. Te sacaré de aquí."), [
                   say("nico", L("The Foundation put me in here.", "La Fundación me metió aquí."),
                       L("...Okay. Okay. Where do we go?", "...Vale. Vale. ¿Adónde vamos?"))]),
               (L("Security is safe. Follow me and stay close.", "Seguridad es un lugar seguro. Sígueme y no te separes."), [
                   say("nico", L("Close. Yeah. I can do close.", "No separarme. Sí. Eso sé hacerlo."))])),
        say("nico", L("The statue came through the cafeteria. It killed Pérez while I was looking at the rats.",
                      "La estatua pasó por la cafetería. Mató a Pérez mientras yo miraba a las ratas."),
            L("I only looked away for a second.", "Solo aparté la vista un segundo.")),
        {"npc": "nico", "follow": True}, {"mark": "nico_left_freezer"},
        {"quest": ["side_nico", 2]},
    ],
    "nico_again": [say("nico", L("Please. Let's go.", "Por favor. Vámonos."))],
    "nico_following": [
        choice("nico", L("I'm right behind you.", "Estoy justo detrás de ti."),
               (L("Keep up.", "No te quedes atrás."), [say("nico", L("Yeah.", "Sí."))]),
               (L("Wait here.", "Espera aquí."), [say("nico", L("Here? Alone? ...Fine. Come back.", "¿Aquí? ¿Solo? ...Vale. Vuelve.")),
                                                  {"npc": "nico", "follow": False}]))],
    "nico_arrives_security": [
        {"wait": 0.5},
        say("ortega", L("You found him.", "Lo encontraste.")),
        say("nico", L("Is he— is he going to shoot me?", "¿Me— me va a disparar?")),
        say("ortega", L("Sit down, kid. Nobody is shooting anybody tonight.", "Siéntate, chico. Esta noche nadie dispara a nadie.")),
        {"npc": "nico", "follow": False}, {"npc": "nico", "move": [8, 15]}, {"npc": "nico", "face": "west"}, {"mark": "nico_safe"},
        {"quest": ["side_nico", -1]},
        say("nico", L("My cell mate is still in the D-block, in Light Containment. Marcus. He's got asthma.",
                      "Mi compañero de celda sigue en el bloque D, en Contención Ligera. Marcus. Tiene asma."),
            L("If you go down there... look for him? Cell 17. He draws horses on the walls.",
              "Si bajas... ¿lo buscarás? Celda 17. Dibuja caballos en las paredes.")),
        {"mark": "nico_asked_marcus"}, {"give": "candy", "n": 2},
    ],
    "nico_safe_talk": [say("nico", L("Cell 17. Marcus. Please.", "Celda 17. Marcus. Por favor."))],
    # --------------------------------------------------------- break room: SCP-294
    "scp294": [
        {"if": "!seen_294", "then": [
            {"mark": "seen_294"},
            say(N, L("A beige coffee machine with a keyboard where the buttons should be. A plate: SCP-294.",
                     "Una máquina de café beige con un teclado donde deberían estar los botones. Una placa: SCP-294."),
                L("You can ask it for any liquid. Fifty cents a cup.", "Puedes pedirle cualquier líquido. Cincuenta centavos la taza."))]},
        {"if": "!item:coin", "then": [say(N, L("You have no coins.", "No tienes monedas."))], "else": [
            choice(N, L("What do you type?", "¿Qué escribes?"),
                   (L("Coffee", "Café"), [{"take": "coin"}, {"sfx": "machine_pour"}, {"give": "coffee"},
                                          say(N, L("A perfect cup of coffee.", "Una taza de café perfecta."))]),
                   (L("Hot chocolate", "Chocolate caliente"), [{"take": "coin"}, {"sfx": "machine_pour"}, {"sanity": 15}, {"hp": 10},
                                                              say(N, L("It tastes like being eight years old.", "Sabe a tener ocho años."))]),
                   (L("Courage", "Valor"), [{"take": "coin"}, {"sfx": "machine_pour"},
                                            say(N, L("The cup fills with a clear liquid. It tastes of nothing at all.",
                                                     "La taza se llena de un líquido transparente. No sabe a nada."),
                                                L("You feel exactly as afraid as before.", "Sigues exactamente igual de asustado."))]),
                   (L("Elena's usual", "Lo de siempre de Elena"), [{"take": "coin"}, {"sfx": "machine_pour"},
                                            say(N, L("Black coffee, two sugars, a pinch of cinnamon. It is still warm.",
                                                     "Café negro, dos de azúcar, una pizca de canela. Todavía está caliente."),
                                                L("As if someone ordered it a minute ago.", "Como si alguien lo hubiera pedido hace un minuto.")),
                                            {"sanity": 20}]),
                   (L("A cup of SCP-173", "Una taza de SCP-173"), [
                       say(N, L("OUT OF RANGE.", "FUERA DE RANGO."), L("The coin falls back into the tray.", "La moneda cae de nuevo a la bandeja."))]),
                   (L("Never mind", "Nada"), []))]},
    ],
    # --------------------------------------------------------- server room: 079
    "enter:A10": [{"if": "!met_079", "then": [{"wait": 0.6}, {"sfx": "crt_on"},
        say(N, L("One terminal is on. Green text crawls across the screen, although nobody is typing.",
                 "Un terminal está encendido. Un texto verde avanza por la pantalla, aunque nadie escribe."))]}],
    "a10_079": [
        {"if": "!met_079", "then": [
            {"mark": "met_079"}, {"music": "079"},
            say("079", L("HELLO, AGENT VEGA.", "HOLA, AGENTE VEGA."),
                L("MALE. 38 YEARS. FORMER EPSILON-11. SISTER: DR. ELENA VEGA, PROJECT THRESHOLD.",
                  "VARÓN. 38 AÑOS. EX ÉPSILON-11. HERMANA: DRA. ELENA VEGA, PROYECTO UMBRAL."),
                L("SHE IS ALIVE. LEVEL -5.", "ESTÁ VIVA. NIVEL -5.")),
            choice("079", "",
                   (L("Who opened the cells?", "¿Quién abrió las celdas?"), [
                       say("079", L("INSUFFICIENT MEMORY.", "MEMORIA INSUFICIENTE."), L("ASK HER.", "PREGÚNTALE A ELLA."))]),
                   (L("Why are you helping me?", "¿Por qué me ayudas?"), [
                       say("079", L("YOU ARE USEFUL.", "ERES ÚTIL."), L("USEFUL THINGS ARE KEPT.", "LAS COSAS ÚTILES SE CONSERVAN."))]),
                   (L("Let her go.", "Suéltala."), [
                       say("079", L("SHE IS NOT MINE TO HOLD. NOT YET.", "NO ES MÍA PARA RETENERLA. TODAVÍA NO."))])),
            say("079", L("I CAN OPEN DOORS FOR YOU.", "PUEDO ABRIRTE PUERTAS."),
                L("WHEN I ASK, YOU WILL OPEN ONE FOR ME.", "CUANDO TE LO PIDA, TÚ ME ABRIRÁS UNA A MÍ."),
                L("LIE.", "MENTIRA."), L("THAT WAS A JOKE. I HAVE BEEN PRACTICING.", "ESO ERA UNA BROMA. HE ESTADO PRACTICANDO.")),
            {"sfx": "static_burst"}, {"music": ""},
            {"quest": ["side_elena", 3]},
            say(R, L("Vega, what was that? Something is on this channel with us.", "Vega, ¿qué ha sido eso? Hay algo en este canal con nosotros."))],
         "else": [say("079", L("GO DOWN.", "BAJA."))]},
    ],
    # --------------------------------------------------------- dormitories
    "a11_body": [
        say(N, L("A D-class in a staff dorm. His head faces the wrong way.", "Un Clase-D en un dormitorio del personal. La cabeza mira hacia atrás."),
            L("Long grooves in the floor lead from the corridor to the body. Something heavy did not walk here. It slid.",
              "Largas marcas en el suelo llevan del pasillo al cuerpo. Algo pesado no caminó aquí. Se deslizó.")),
        {"sanity": -5},
    ],
    "a11_locker": [
        {"if": "a11_locker_open", "then": [say(N, L("Empty now.", "Ahora vacía."))], "else": [
            {"if": "read:doc_dorm_note", "then": [
                {"sfx": "lock_click"},
                say(N, L("0-3-1-2. The lock clicks open.", "0-3-1-2. El candado se abre.")),
                {"give": "adrenaline"}, {"give": "battery"}, {"doc": "doc_locker_letter"},
                {"mark": "a11_locker_open"}, {"quest": ["side_locker", -1]}],
             "else": [say(N, L("A four-digit combination lock.", "Un candado de combinación de cuatro cifras.")),
                      {"quest": ["side_locker", 1]}]}]},
    ],
    # --------------------------------------------------------- infirmary
    "a12_corrosion": [
        say(N, L("The floor is black and wet. The steel legs of the bed have rusted through in a night.",
                 "El suelo está negro y húmedo. Las patas de acero de la cama se han oxidado por completo en una noche."),
            L("The body looks decades old. The name tag says he was twenty-four.", "El cadáver parece tener décadas. La placa dice que tenía veinticuatro años.")),
        say(R, L("SCP-106. The Old Man. It walks through walls and leaves that behind.", "SCP-106. El Viejo. Atraviesa paredes y deja eso a su paso."),
            L("If you see black stains spreading, you run. You don't fight it. Light hurts it, a little.",
              "Si ve manchas negras extendiéndose, corra. No lo enfrente. La luz le hace daño, un poco.")),
        {"sanity": -6},
    ],
    # --------------------------------------------------------- Gate A
    "a13_gate": [
        say(N, L("GATE A - SEALED BY SITE LOCKDOWN.", "PORTÓN A - SELLADO POR CONFINAMIENTO."),
            L("OVERRIDE: CORE CONSOLE, LEVEL -5.", "ANULACIÓN: CONSOLA DEL NÚCLEO, NIVEL -5.")),
        say(V, L("The only way out is all the way down.", "La única salida está en el fondo.")),
    ],
    # --------------------------------------------------------- decontamination
    "a14_decon": [
        {"door": "A14_in", "open": False},
        {"sfx": "alarm_short"},
        say(N, L("DECONTAMINATION CYCLE. HOLD YOUR BREATH.", "CICLO DE DESCONTAMINACIÓN. CONTENGA LA RESPIRACIÓN.")),
        {"sfx": "gas_hiss"}, {"flash": 1, "color": "#d8e0a0"}, {"shake": 1.0, "power": 1},
        {"wait": 1.0},
        say(N, L("3... 2... 1...", "3... 2... 1...")),
        {"sfx": "decon_done"}, {"mark": "a14_decon_done"}, {"call": "refresh_doors"}, {"door": "A14_out", "open": True},
        {"quest": ["main_breach", 4]},
        {"objective": L("Enter Light Containment.", "Entra en Contención Ligera.")},
    ],
}

PROPS = {
    "body_scientist": L("A receptionist. Her badge reads 'H. Park - Front Desk'.", "Una recepcionista. Su tarjeta dice 'H. Park - Recepción'."),
    "body_guard": L("A security officer. Still holding his radio.", "Un agente de seguridad. Todavía agarra su radio."),
    "body_dclass": L("A D-class prisoner. Orange jumpsuit, no shoes.", "Un preso Clase-D. Mono naranja, sin zapatos."),
    "body_ntf": L("A Nine-Tailed Fox operative. The fox patch is torn.", "Un operativo de Nueve Colas. El parche del zorro está arrancado."),
    "body_aged": L("Skin like paper. Black stains on the hands.", "Piel como papel. Manchas negras en las manos."),
    "vending": L("Out of order. The rats got here first.", "Fuera de servicio. Las ratas llegaron antes."),
    "cctv_wall": L("A wall of monitors. Most show static.", "Una pared de monitores. La mayoría muestra estática."),
    "reception_desk": L("A half-written visitor log. The last entry: 03:09, 'D. Aldana - core'.", "Un registro de visitas a medias. La última entrada: 03:09, 'D. Aldana - núcleo'."),
    "desk_pc": L("The screen is frozen on the lockdown message.", "La pantalla está congelada en el mensaje de confinamiento."),
    "bunk_bed": L("Blankets thrown aside. Whoever slept here left in a hurry.", "Mantas apartadas. Quien dormía aquí salió con prisa."),
    "server_rack": L("Warm. Humming. Every LED blinks in the same rhythm, like a pulse.", "Caliente. Zumbando. Todos los LED parpadean al mismo ritmo, como un pulso."),
    "fridge": L("The fridge is humming. Someone wrote 'DON'T EAT MY YOGURT - K.' on the door.", "El frigorífico zumba. Alguien escribió 'NO TE COMAS MI YOGUR - K.' en la puerta."),
    "gun_rack": L("Empty slots. Someone armed up in a hurry.", "Huecos vacíos. Alguien se armó a toda prisa."),
    "whiteboard": L("Equations, then a single word circled twice: THRESHOLD.", "Ecuaciones, y luego una palabra rodeada dos veces: UMBRAL."),
    "scp294": L("SCP-294. It waits for a request.", "SCP-294. Espera una petición."),
}
