"""Act II — Light Containment. SCP-173 hunts the junction. Adebayo and 914, the Eye Pods, 012, 999, Marcus."""
from common import L, say, choice

N, R, V = "", "radio", "vega"
AD = "adebayo"

QUESTS = {
    "main_173": dict(main=True, name=L("The Sculpture", "La Escultura"), stages=[
        L("SCP-173 is loose in the LCZ junction. Find a way to put it back in its cell.", "SCP-173 anda suelto en el cruce de la ZCL. Encuentra la forma de devolverlo a su celda."),
        L("Adebayo: the cell console is in the observation booth (Level 2). Get a Level 2 card from SCP-914.", "Adebayo: la consola de la celda está en la cabina de observación (Nivel 2). Consigue una tarjeta de nivel 2 con SCP-914."),
        L("The Eye Pods (SCP-131) never blink. Find them in their habitat and make friends.", "Los Ojo-Cápsulas (SCP-131) nunca parpadean. Encuéntralos en su hábitat y hazte su amigo."),
        L("Open the cell from the booth. Lure 173 inside, leave through the crawl hatch, and seal it.", "Abre la celda desde la cabina. Atrae a 173 adentro, sal por la escotilla y séllala."),
        L("Take the maintenance ladder down to Level -3.", "Baja por la escalerilla de mantenimiento al Nivel -3."),
    ]),
    "side_notebook": dict(name=L("Adebayo's notebook", "El cuaderno de Adebayo"), stages=[
        L("Adebayo dropped his notebook in the SCP-012 room. Don't look at the music.", "Adebayo dejó su cuaderno en la sala de SCP-012. No mires la partitura."),
        L("Bring the notebook back to Adebayo in the 914 lab.", "Devuélvele el cuaderno a Adebayo en el laboratorio de 914."),
    ]),
    "side_marcus": dict(name=L("Cell 17", "Celda 17"), stages=[
        L("Nico asked you to find his cell mate Marcus in D-block, cell 17.", "Nico te pidió buscar a su compañero Marcus en el bloque D, celda 17."),
        L("Marcus is dead. He left a letter for Nico. Nico should have it.", "Marcus está muerto. Dejó una carta para Nico. Nico debería tenerla."),
    ]),
}

DOCS = {
    "doc_173_file": dict(title=L("SCP-173 - Containment procedures", "SCP-173 - Procedimientos de contención"), body=L(
        "Object Class: Euclid.\n\nItem SCP-173 is to be kept in a locked container at all times. When personnel must enter "
        "SCP-173's container, no fewer than 3 may enter at any time and the door is to be relocked behind them. At all times, "
        "two persons must maintain direct eye contact with SCP-173 until all personnel have vacated and relocked the container.\n\n"
        "Constructed from concrete and rebar with traces of Krylon brand spray paint. Animate and extremely hostile. It cannot "
        "move while within a direct line of sight. Line of sight must not be broken at any time. Personnel are instructed to "
        "alert one another before blinking.\n\nReports of scraping stone originating from inside the container when no one is "
        "present are considered normal.",
        "Clase de objeto: Euclid.\n\nSCP-173 debe mantenerse en un contenedor cerrado en todo momento. Cuando el personal deba "
        "entrar, no podrán hacerlo menos de 3 personas y la puerta se volverá a cerrar tras ellas. En todo momento, dos personas "
        "deben mantener contacto visual directo con SCP-173 hasta que todo el personal haya salido y cerrado el contenedor.\n\n"
        "Construido de hormigón y varilla con restos de pintura en aerosol marca Krylon. Animado y extremadamente hostil. No "
        "puede moverse mientras esté en línea de visión directa. La línea de visión no debe romperse nunca. El personal debe "
        "avisarse antes de parpadear.\n\nLos informes de piedra raspando dentro del contenedor cuando no hay nadie se "
        "consideran normales."), source="SCP-173 by Moto42 · scp-wiki.wikidot.com/scp-173 · CC BY-SA 3.0"),
    "doc_914_log": dict(title=L("SCP-914 - Test log (excerpt)", "SCP-914 - Registro de pruebas (extracto)"), body=L(
        "SCP-914 is a large clockwork device: over eight million moving parts, tin and copper, 18 m². Two booths, 'Intake' and "
        "'Output'. A dial: Rough, Coarse, 1:1, Fine, Very Fine. A key winds it.\n\n"
        "Input: 1 steel wrench. Setting: Fine. Output: 1 wrench, precision-machined, no maker's mark.\n"
        "Input: 1 Level-1 keycard. Setting: Fine. Output: 1 Level-2 keycard. Valid. [Security has been notified.]\n"
        "Input: 1 bandage. Setting: Fine. Output: 1 complete field dressing kit.\n"
        "Input: 1 battery. Setting: Very Fine. Output: 1 battery. Charge exceeds rating by 400%. Warm to the touch.\n"
        "Input: 1 revolver. Setting: Very Fine. Output: [REDACTED]. Test halted.\n\n"
        "Biological testing is prohibited. - Dr. Adebayo (who knows why)",
        "SCP-914 es un gran dispositivo de relojería: más de ocho millones de piezas, estaño y cobre, 18 m². Dos cabinas, "
        "'Entrada' y 'Salida'. Un dial: Tosco, Grueso, 1:1, Fino, Muy fino. Una llave le da cuerda.\n\n"
        "Entrada: 1 llave inglesa de acero. Ajuste: Fino. Salida: 1 llave, mecanizada con precisión, sin marca.\n"
        "Entrada: 1 tarjeta de nivel 1. Ajuste: Fino. Salida: 1 tarjeta de nivel 2. Válida. [Se ha notificado a Seguridad.]\n"
        "Entrada: 1 venda. Ajuste: Fino. Salida: 1 botiquín de campaña completo.\n"
        "Entrada: 1 pila. Ajuste: Muy fino. Salida: 1 pila. Carga un 400% superior a la nominal. Tibia al tacto.\n"
        "Entrada: 1 revólver. Ajuste: Muy fino. Salida: [REDACTADO]. Prueba detenida.\n\n"
        "Las pruebas biológicas están prohibidas. - Dr. Adebayo (que sabe por qué)"),
        source="SCP-914 by Dr Gears · scp-wiki.wikidot.com/scp-914 · CC BY-SA 3.0"),
    "doc_012_file": dict(title=L("SCP-012 - 'A Bad Composition'", "SCP-012 - 'Una mala composición'"), body=L(
        "An incomplete score titled 'On Mount Golgotha', written in blood from multiple subjects. Anyone who sees it feels an "
        "irresistible urge to finish it, using their own blood. Those who complete a section become psychotic. They all say "
        "the same thing: it cannot be finished.\n\nKeep it in darkness, in its iron box, at least 2.5 m from any surface.\n\n"
        "Someone opened the box.",
        "Una partitura incompleta titulada 'En el monte Gólgota', escrita con la sangre de varios sujetos. Quien la ve siente "
        "el impulso irresistible de terminarla, usando su propia sangre. Quienes completan una sección se vuelven psicóticos. "
        "Todos dicen lo mismo: no se puede terminar.\n\nMantener a oscuras, en su caja de hierro, a 2,5 m de cualquier "
        "superficie.\n\nAlguien abrió la caja."), sanity=-8,
        source="SCP-012 by ITIFAMCO · scp-wiki.wikidot.com/scp-012 · CC BY-SA 3.0"),
    "doc_131_note": dict(title=L("Sticky note on a door", "Nota adhesiva en una puerta"), body=L(
        "To whoever is on 131 duty: the Eye Pods got out again and followed Keller all the way to the 173 wing. They sat "
        "there and STARED at it for two hours. It didn't move once. Nobody's writing this up, but I'm telling you: they never "
        "blink. They like candy wrappers. The crinkly sound. - J.",
        "Para quien le toque 131: los Ojo-Cápsulas se volvieron a escapar y siguieron a Keller hasta el ala de 173. Se "
        "quedaron ahí MIRÁNDOLA dos horas. No se movió ni una vez. Nadie lo va a poner en un informe, pero os lo digo: nunca "
        "parpadean. Les gustan los envoltorios de caramelos. El ruidito. - J.")),
    "doc_999_note": dict(title=L("Caretaker's note", "Nota del cuidador"), body=L(
        "999 only eats candy. It refused a steak and then spent twenty minutes making a crying intern laugh. If you're "
        "having a bad day, go in. It will know. It always knows.",
        "999 solo come caramelos. Rechazó un filete y luego pasó veinte minutos haciendo reír a un becario que lloraba. Si "
        "tienes un mal día, entra. Lo sabrá. Siempre lo sabe."), source="SCP-999 by ProfSnider · scp-wiki.wikidot.com/scp-999 · CC BY-SA 3.0"),
    "doc_500_file": dict(title=L("SCP-500 - Panacea", "SCP-500 - Panacea"), body=L(
        "A plastic container of red pills. One pill, taken orally, cures the subject of all diseases within two hours. "
        "Remaining: 47. Synthesis attempts have failed.\n\nThe log below the file shows two pills signed out at 03:40 by "
        "'E. Vega - for the core'.",
        "Un contenedor de plástico con píldoras rojas. Una píldora, por vía oral, cura al sujeto de toda enfermedad en dos "
        "horas. Restantes: 47. Los intentos de síntesis han fracasado.\n\nEl registro bajo el expediente muestra dos píldoras "
        "retiradas a las 03:40 por 'E. Vega - para el núcleo'."), source="SCP-500 by snorlison · scp-wiki.wikidot.com/scp-500 · CC BY-SA 3.0"),
    "doc_marcus_letter": dict(title=L("A letter, folded eight times", "Una carta, doblada ocho veces"), body=L(
        "Nico,\n\nif you read this you got out and I didn't, so don't be stupid about it. The guards said Tuesday they're "
        "moving the whole block to Heavy Containment for 'trials'. Nobody comes back from Heavy.\n\nI drew you the horses. "
        "The brown one is you. It's the fast one. When you're outside, go see real ones. Promise.\n\n- Marcus",
        "Nico,\n\nsi lees esto es que saliste y yo no, así que no hagas tonterías. Los guardias dicen que el martes llevan "
        "todo el bloque a Contención Pesada para 'pruebas'. De Pesada no vuelve nadie.\n\nTe dibujé los caballos. El marrón "
        "eres tú. Es el rápido. Cuando estés fuera, ve a ver unos de verdad. Prométemelo.\n\n- Marcus")),
    "doc_black_tide_schedule": dict(title=L("Transfer schedule - D-Block", "Calendario de traslados - Bloque D"), body=L(
        "BLACK TIDE / PHASE 1\nTuesday 04:00 - D-Block (all 40 subjects) to HCZ acid chamber, SCP-682.\n"
        "Escort: Security team 3.\nAmnestics for escort: Class-B, post-procedure.\n"
        "Note from the director: 'No names in the log. Numbers only.'\n\nThe breach started at 03:12, Tuesday.",
        "MAREA NEGRA / FASE 1\nMartes 04:00 - Bloque D (los 40 sujetos) a la cámara de ácido de ZCP, SCP-682.\n"
        "Escolta: equipo de seguridad 3.\nAmnésicos para la escolta: clase B, tras el procedimiento.\n"
        "Nota de la directora: 'Nada de nombres en el registro. Solo números.'\n\nLa brecha empezó a las 03:12, un martes."), sanity=-4),
    "doc_shower_scrawl": dict(title=L("Written in the steam", "Escrito en el vaho"), body=L(
        "On the mirror, in the condensation, someone wrote: DON'T BLINK DON'T BLINK DON'T BL",
        "En el espejo, sobre el vaho, alguien escribió: NO PARPADEES NO PARPADEES NO PARP")),
    "adebayo_notebook": dict(title=L("Adebayo's notebook", "El cuaderno de Adebayo"), body=L(
        "Pages of dial settings and outcomes, in tiny handwriting. The last page, shakier: 'Elena asked me to put a Level-5 "
        "card through on Very Fine. I told her it's a crime. She said so is Tuesday. I did it. It came out black, with no "
        "level printed on it. God help us.'",
        "Páginas de ajustes del dial y resultados, con letra diminuta. La última página, más temblorosa: 'Elena me pidió que "
        "pasara una tarjeta de nivel 5 en Muy fino. Le dije que era un delito. Me dijo que el martes también. Lo hice. Salió "
        "negra, sin nivel impreso. Que Dios nos ayude.'")),
}


def recipe(item, setting, result=None, n=1, text=None, lose=True):
    acts = [{"sfx": "machine_pour"}, {"shake": 2.0, "power": 1}, {"wait": 1.0}]
    if lose:
        acts.append({"take": item})
    if result:
        acts.append({"give": result, "n": n})
    acts.append(say(N, text or L("The machine clatters for a long time. The Output door opens.", "La máquina traquetea un buen rato. Se abre la puerta de Salida.")))
    return acts


SETTINGS = [L("Rough", "Tosco"), L("Coarse", "Grueso"), L("1:1", "1:1"), L("Fine", "Fino"), L("Very Fine", "Muy fino")]


def machine(item, results):
    """results: 5 action lists (one per setting)."""
    return [choice(N, L("Set the dial.", "Gira el dial."), *[(SETTINGS[i], results[i]) for i in range(5)])]


RUBBLE = L("Out comes a small heap of dust and shavings.", "Sale un montoncito de polvo y virutas.")
SAME = L("It comes out exactly the same. Slightly warm.", "Sale exactamente igual. Ligeramente tibio.")

SCP914 = [
    {"if": "!seen_914", "then": [{"mark": "seen_914"},
        say(N, L("SCP-914. A cathedral of brass, eight million parts ticking in the dark. An Intake booth, an Output booth, "
                 "and a big dial between them.", "SCP-914. Una catedral de latón, ocho millones de piezas latiendo en la oscuridad. "
                 "Una cabina de Entrada, una de Salida y un gran dial entre ellas."))]},
    choice(N, L("What do you put in the Intake booth?", "¿Qué metes en la cabina de Entrada?"),
           (L("Level 1 keycard", "Tarjeta de nivel 1"), machine("card_1", [
               recipe("card_1", 0, text=RUBBLE), recipe("card_1", 1, text=L("A bent strip of plastic.", "Una tira de plástico doblada.")),
               recipe("card_1", 2, "card_1", text=SAME),
               recipe("card_1", 3, "card_2", text=L("A clean new card. The stripe is green: LEVEL 2.", "Una tarjeta nueva y limpia. La franja es verde: NIVEL 2.")),
               recipe("card_1", 4, "card_2", text=L("A LEVEL 2 card, printed with a name you don't recognise and a photo of you, older.",
                                                    "Una tarjeta de NIVEL 2, con un nombre que no reconoces y una foto tuya, más viejo."))]), "item:card_1"),
           (L("Level 2 keycard", "Tarjeta de nivel 2"), machine("card_2", [
               recipe("card_2", 0, text=RUBBLE), recipe("card_2", 1, "card_1", text=L("It comes out as a Level 1 card.", "Sale como tarjeta de nivel 1.")),
               recipe("card_2", 2, "card_2", text=SAME),
               recipe("card_2", 3, "card_2", text=L("The card comes back, scratched: 'NICE TRY'.", "La tarjeta vuelve, rayada: 'BUEN INTENTO'.")),
               recipe("card_2", 4, "card_2", text=L("The card comes back, scratched: 'NICE TRY'.", "La tarjeta vuelve, rayada: 'BUEN INTENTO'."))]), "item:card_2,!item:card_3"),
           (L("Bandage", "Venda"), machine("bandage", [
               recipe("bandage", 0, text=RUBBLE), recipe("bandage", 1, text=L("Loose cotton threads.", "Hilos de algodón sueltos.")),
               recipe("bandage", 2, "bandage", text=SAME), recipe("bandage", 3, "medkit", text=L("A complete medkit.", "Un botiquín completo.")),
               recipe("bandage", 4, "adrenaline", text=L("An auto-injector, humming faintly.", "Un autoinyector que zumba levemente."))]), "item:bandage"),
           (L("Medkit", "Botiquín"), machine("medkit", [
               recipe("medkit", 0, "bandage", n=2, text=L("Two bandages.", "Dos vendas.")), recipe("medkit", 1, "bandage", text=L("One bandage.", "Una venda.")),
               recipe("medkit", 2, "medkit", text=SAME), recipe("medkit", 3, "adrenaline", text=L("Adrenaline.", "Adrenalina.")),
               recipe("medkit", 4, "medkit", text=L("A medkit full of instruments you don't recognise. You keep the gauze.", "Un botiquín lleno de instrumentos que no reconoces. Te quedas con las gasas."))]), "item:medkit"),
           (L("Battery", "Pila"), machine("battery", [
               recipe("battery", 0, text=RUBBLE), recipe("battery", 1, text=L("Acid leaks out. Nothing useful.", "Sale ácido. Nada útil.")),
               recipe("battery", 2, "battery", text=SAME), recipe("battery", 3, "battery", n=2, text=L("Two batteries.", "Dos pilas.")),
               [{"take": "battery"}, {"sfx": "machine_pour"}, {"wait": 1.0}, {"battery": 100}, {"give": "battery"},
                say(N, L("A battery that is warm and heavy. The flashlight will love it.", "Una pila tibia y pesada. A la linterna le encantará."))]]), "item:battery"),
           (L("Coin", "Moneda"), machine("coin", [
               recipe("coin", 0, text=RUBBLE), recipe("coin", 1, text=L("A flat disc of metal.", "Un disco plano de metal.")),
               recipe("coin", 2, "coin", text=SAME), recipe("coin", 3, "coin", n=2, text=L("Two quarters. Adebayo pretends not to see.", "Dos monedas. Adebayo finge no verlo.")),
               recipe("coin", 4, "candy", n=3, text=L("Three candies. The machine has a sense of humour.", "Tres caramelos. La máquina tiene sentido del humor."))]), "item:coin"),
           (L("Nothing", "Nada"), [])),
]

EVENTS = {
    # --------------------------------------------------------- LCZ entrance
    "enter:B01": [{"if": "!b01_seen", "then": [{"mark": "b01_seen"}, {"quest": ["main_breach", -1]}, {"wait": 0.4},
        say(R, L("Vega, you're in Light Containment. Readings show movement in the central junction. Something heavy. It stops when the cameras look at it.",
                 "Vega, está en Contención Ligera. Hay movimiento en el cruce central. Algo pesado. Se detiene cuando las cámaras lo miran.")),
        {"objective": L("Cross the LCZ junction. Keep your light on anything that moves.", "Cruza el cruce de la ZCL. Mantén la luz sobre cualquier cosa que se mueva.")}]}],
    # --------------------------------------------------------- the junction
    "b02_reveal": [
        {"if": "!scp173_contained", "then": [
            {"lights": "flicker", "t": 1.0}, {"sfx": "scrape", "db": 2},
            say(N, L("Something stands in the middle of the junction. Tall. Concrete. Its face is sprayed in red and green.",
                     "Algo está de pie en mitad del cruce. Alto. De hormigón. Tiene la cara pintada con spray rojo y verde.")),
            say(R, L("That's it. SCP-173. Do not take your eyes off it. Keep it in your light.", "Es él. SCP-173. No le quite los ojos de encima. Manténgalo bajo su luz."),
                L("It moves when you blink. Every time you blink.", "Se mueve cuando parpadea. Cada vez que parpadea.")),
            {"quest": ["main_173", 1]},
            {"objective": L("Get past SCP-173. The research corridor is north.", "Deja atrás a SCP-173. El pasillo de investigación está al norte.")}]}],
    "b02_console": [
        {"if": "scp173_contained", "then": [say(N, L("CELL 173: SEALED. OCCUPANT: PRESENT.", "CELDA 173: SELLADA. OCUPANTE: PRESENTE."))], "else": [
            {"sfx": "terminal"},
            {"if": "!b02_cell_open", "then": [
                choice(N, L("CELL 173 - STATUS: CLOSED, EMPTY.", "CELDA 173 - ESTADO: CERRADA, VACÍA."),
                       (L("Open the cell door", "Abrir la puerta de la celda"), [
                           {"mark": "b02_cell_open"}, {"call": "refresh_doors"}, {"door": "B02_cell", "open": True}, {"sfx": "alarm_short"},
                           say(N, L("The heavy door grinds open. The cell is dark.", "La puerta blindada se abre con un chirrido. La celda está a oscuras.")),
                           {"if": "bond131", "then": [say(V, L("If I leave the Pods here, nothing will watch it. It'll follow me.",
                                                              "Si dejo aquí a los Ojo-Cápsulas, nada lo vigilará. Me seguirá."))]},
                           {"quest": ["main_173", 4]},
                           {"objective": L("Lure 173 into its cell, leave through the hatch, seal it from here.", "Atrae a 173 a su celda, sal por la escotilla y séllala desde aquí.")}]),
                       (L("Leave it", "Dejarlo"), []))],
             "else": [
                {"unmark": "seal_failed"}, {"call": "seal_173", "args": [24, 2, 10, 8]},
                {"if": "scp173_contained", "then": [
                    {"door": "B02_cell", "open": False}, {"sfx": "door_close", "db": 4}, {"shake": 0.8, "power": 3},
                    say(N, L("You slam the SEAL button. The door crashes down. Behind it, stone scrapes against steel. Then nothing.",
                             "Golpeas el botón de SELLAR. La puerta cae de golpe. Detrás, piedra que raspa acero. Luego, nada.")),
                    {"sfx": "crt_on"},
                    say("079", L("IMPRESSIVE. THE STATUE IS HOME.", "IMPRESIONANTE. LA ESTATUA ESTÁ EN CASA."),
                        L("I OPENED THE MAINTENANCE DOOR FOR YOU. CONSIDER IT A LOAN.", "TE HE ABIERTO LA PUERTA DE MANTENIMIENTO. CONSIDÉRALO UN PRÉSTAMO.")),
                    say(R, L("Vega... good work. How did you open maintenance? That door is on the core network.",
                             "Vega... buen trabajo. ¿Cómo abrió mantenimiento? Esa puerta está en la red del núcleo.")),
                    {"unmark": "pods_stay"},
                    {"quest": ["main_173", 5]}, {"call": "refresh_doors"},
                    {"objective": L("Take the maintenance ladder down to Level -3.", "Baja por la escalerilla de mantenimiento al Nivel -3.")},
                    {"save": True}],
                 "else": [say(N, L("SEAL REFUSED: CELL SENSORS REPORT NO OCCUPANT.", "SELLADO DENEGADO: LOS SENSORES NO DETECTAN OCUPANTE."))]}]}]},
    ],
    # --------------------------------------------------------- 914 / Adebayo
    "enter:B06": [{"if": "!met_adebayo", "then": [{"wait": 0.5},
        say(N, L("A man in an oil-stained lab coat is winding a brass key the size of his arm. He doesn't turn around.",
                 "Un hombre con una bata manchada de aceite da cuerda a una llave de latón del tamaño de su brazo. No se gira."))]}],
    "adebayo_first": [
        {"mark": "met_adebayo"},
        say(AD, L("You are not a statue. Good. You would be surprised how often I have to check.", "No eres una estatua. Bien. Te sorprendería cuántas veces tengo que comprobarlo."),
            L("Adebayo. I've worked on 914 for eleven years. When the doors opened I locked myself in with it. It seemed the safest thing in the building.",
              "Adebayo. Llevo once años con 914. Cuando se abrieron las puertas me encerré con ella. Me pareció lo más seguro del edificio.")),
        choice(AD, "",
               (L("I need to put 173 back in its cell.", "Tengo que devolver a 173 a su celda."), [
                   say(AD, L("The cell console is in the observation booth. Level 2. You have a Level 1 card, I assume.", "La consola de la celda está en la cabina de observación. Nivel 2. Supongo que tienes una tarjeta de nivel 1."),
                       L("Put it in the Intake booth. Turn the dial to Fine. The Foundation pretends it doesn't know this works.", "Métela en la cabina de Entrada. Gira el dial a Fino. La Fundación finge que no sabe que esto funciona."))]),
               (L("Do you know Elena Vega?", "¿Conoces a Elena Vega?"), [
                   say(AD, L("...She asked me for a favour, two days ago. I did it. I should not have. Ask me about it when you've earned it.",
                             "...Me pidió un favor hace dos días. Se lo hice. No debí. Pregúntame cuando te lo hayas ganado."))])),
        say(AD, L("One more thing. If you want to survive 173, you need eyes that never close. There are two of them in the Eye Pod habitat.",
                  "Una cosa más. Si quieres sobrevivir a 173, necesitas ojos que nunca se cierren. Hay dos en el hábitat de los Ojo-Cápsulas."),
            L("And... I dropped my notebook in the 012 room when I ran. I cannot go back there. Please don't read the music.",
              "Y... se me cayó el cuaderno en la sala de 012 cuando huí. No puedo volver. Por favor, no leas la partitura.")),
        {"quest": ["main_173", 2]}, {"quest": ["side_notebook", 1]},
        {"objective": L("Refine your Level 1 card into Level 2 with SCP-914 (Fine).", "Refina tu tarjeta de nivel 1 a nivel 2 con SCP-914 (Fino).")},
    ],
    "adebayo_again": [
        {"if": "quest:side_notebook:2,!done:side_notebook", "then": [
            say(AD, L("My notebook! You went in there. Are you... fine? Look at your hands. Good. Good.", "¡Mi cuaderno! Entraste ahí. ¿Estás... bien? Mírate las manos. Bien. Bien.")),
            {"quest": ["side_notebook", -1]},
            say(AD, L("You read the last page. I can see it in your face.", "Leíste la última página. Te lo veo en la cara."),
                L("Your sister put a Level 5 card through on Very Fine. It came out as something that opens every door in this site. An O5 key. Forged by a clock.",
                  "Tu hermana pasó una tarjeta de nivel 5 en Muy fino. Salió algo que abre todas las puertas del sitio. Una llave O5. Falsificada por un reloj."),
                L("I think that is how the cells opened. I think I helped her do it.", "Creo que así se abrieron las celdas. Creo que la ayudé a hacerlo.")),
            {"give": "battery", "n": 2}, {"give": "medkit"}, {"mark": "knows_o5_key"}],
         "else": [say(AD, L("Fine for keycards. Very Fine for... surprises. Never put anything alive in there.",
                           "Fino para tarjetas. Muy fino para... sorpresas. Nunca metas nada vivo ahí."))]},
    ],
    "scp914": SCP914,
    # --------------------------------------------------------- 012
    "enter:B07": [{"if": "!b07_seen", "then": [{"mark": "b07_seen"}, {"wait": 0.5}, {"sfx": "whisper"},
        say(N, L("The iron box hangs open. The paper inside is covered in notes of dried blood.", "La caja de hierro cuelga abierta. El papel de dentro está cubierto de notas de sangre seca."),
            L("You can almost hear the melody. It's missing one bar. Only one.", "Casi puedes oír la melodía. Le falta un compás. Solo uno.")),
        {"sanity": -8}]}],
    "b07_close": [{"if": "!b07_resisted", "then": [
        say(N, L("Your hand is already reaching for the paper. Your fingertip is wet.", "Tu mano ya se estira hacia el papel. Tienes la yema del dedo húmeda.")),
        choice(N, "",
               (L("Look away", "Apartar la vista"), [{"mark": "b07_resisted"}, {"sanity": -4},
                                                   say(V, L("No. Not today.", "No. Hoy no."))]),
               (L("Finish the bar", "Terminar el compás"), [{"hp": -25, "cause": "sanity"}, {"sanity": -30},
                   say(N, L("You write one note with your own blood. It is wrong. It is always wrong.", "Escribes una nota con tu propia sangre. Está mal. Siempre está mal.")),
                   {"mark": "b07_resisted"}]))]}],
    "item:adebayo_notebook": [{"quest": ["side_notebook", 2]}],
    # --------------------------------------------------------- 131
    "scp131_talk": [
        {"if": "bond131", "then": [
            choice(N, L("The Eye Pods babble at you, both eyes wide.", "Los Ojo-Cápsulas te balbucean, con los ojos muy abiertos."),
                   (L("Stay here and watch", "Quedaos aquí vigilando"), [{"mark": "pods_stay"}, say(N, L("They huddle behind the console, trembling, and squeeze their eyes shut. For once, nothing is watching.",
                                                           "Se acurrucan detrás de la consola, temblando, y cierran los ojos con fuerza. Por una vez, nada vigila."))]),
                   (L("Come with me", "Venid conmigo"), [{"unmark": "pods_stay"}, say(N, L("They wheel around your ankles, delighted.", "Ruedan alrededor de tus tobillos, encantados."))]))],
         "else": [
            say(N, L("Two little teardrop creatures, orange and yellow, each one a single enormous blue eye. They roll back from you.",
                     "Dos criaturitas con forma de lágrima, naranja y amarilla, cada una un único ojo azul enorme. Retroceden rodando.")),
            {"if": "item:candy", "then": [
                choice(N, "",
                       (L("Crinkle a candy wrapper", "Hacer sonar un envoltorio"), [{"take": "candy"}, {"sfx": "paper", "pitch": 1.4},
                           say(N, L("They freeze. Then they zoom to your feet and start babbling, bouncing, staring up at you.",
                                    "Se quedan quietos. Luego salen disparados hacia tus pies y empiezan a balbucear, saltando, mirándote.")),
                           {"mark": "bond131"}, {"quest": ["main_173", 3]}, {"toast": L("The Eye Pods are following you.", "Los Ojo-Cápsulas te siguen.")},
                           say(V, L("Two pairs of eyes that never blink. Alright. Stay close.", "Dos pares de ojos que nunca parpadean. Muy bien. No os separéis.")),
                           {"objective": L("Return to the junction. Open 173's cell from the observation booth.", "Vuelve al cruce. Abre la celda de 173 desde la cabina de observación.")}]),
                       (L("Leave them", "Dejarlos"), []))],
             "else": [say(N, L("They don't trust you. Something small and noisy might help.", "No se fían de ti. Algo pequeño y ruidoso ayudaría."))]}]},
    ],
    "enter:B08": [{"if": "!bond131", "then": [{"quest": ["main_173", 3]}]}],
    # --------------------------------------------------------- 999
    "scp999_talk": [
        say(N, L("The orange blob wobbles against your legs and gurgles. It smells like your mother's kitchen.",
                 "La masa naranja se tambalea contra tus piernas y gorgotea. Huele a la cocina de tu madre.")),
        {"if": "!b09_hugged", "then": [{"mark": "b09_hugged"}, {"sanity": 100}, {"hp": 15}, {"sfx": "heal"},
            say(N, L("It wraps itself around you. You are laughing. You don't remember deciding to laugh.", "Te envuelve. Te estás riendo. No recuerdas haber decidido reírte.")),
            say(V, L("...Thanks, little guy.", "...Gracias, pequeño."))],
         "else": [{"if": "item:candy", "then": [
             choice(N, "", (L("Give it a candy", "Darle un caramelo"), [{"take": "candy"}, {"sanity": 60}, {"sfx": "squelch", "pitch": 1.6},
                                                                        say(N, L("It absorbs the candy with a happy squeal. You feel lighter.", "Absorbe el caramelo con un chillido feliz. Te sientes más ligero."))]),
                    (L("Pat it", "Acariciarlo"), [{"sanity": 10}]))],
             "else": [{"sanity": 10}, say(N, L("It bumps your hand, hoping for candy.", "Te empuja la mano, esperando un caramelo."))]}]},
    ],
    # --------------------------------------------------------- D-block
    "enter:B11": [{"if": "!b11_seen", "then": [{"mark": "b11_seen"}, {"wait": 0.4},
        say(N, L("Forty cells. Most doors hang open. The ones that are closed are quiet.", "Cuarenta celdas. Casi todas las puertas están abiertas. Las cerradas están en silencio.")),
        {"if": "nico_asked_marcus", "then": [{"quest": ["side_marcus", 1]}]}]}],
    "b11_marcus": [
        say(N, L("Horses. Dozens of them, drawn in charcoal on every wall, running.", "Caballos. Decenas, dibujados con carbón en todas las paredes, corriendo."),
            L("The man on the floor still holds the charcoal.", "El hombre del suelo todavía sujeta el carbón.")),
        {"if": "nico_asked_marcus", "then": [say(V, L("Marcus. I'm sorry, kid.", "Marcus. Lo siento, chico.")), {"quest": ["side_marcus", 2]}]},
        {"sanity": -5},
    ],
    "item:doc_marcus_letter": [{"if": "nico_asked_marcus", "then": [{"quest": ["side_marcus", 2]}]}],
    "item:doc_black_tide_schedule": [{"mark": "knows_black_tide"},
        say(V, L("Tuesday. Today. They were going to feed forty people to 682 today.", "Martes. Hoy. Hoy iban a darle cuarenta personas a 682."))],
    "b12_mirror": [{"lights": "off"}, {"wait": 0.8}, {"sfx": "scrape", "db": 4}, {"wait": 0.6}, {"lights": "on"},
        say(N, L("For a moment, in the mirror, there was someone standing behind you.", "Por un momento, en el espejo, había alguien de pie detrás de ti.")), {"sanity": -6}],
    # --------------------------------------------------------- down
    "b15_ladder": [say(N, L("A service ladder goes down into warm, wet darkness. It smells of rust and something rotting.",
                            "Una escalerilla de servicio baja hacia una oscuridad cálida y húmeda. Huele a óxido y a algo podrido."))],
    "enter:B15": [{"if": "!b15_seen", "then": [{"mark": "b15_seen"},
        say(R, L("Vega, the power plant for Levels -3 to -5 is down there. If you can restore it, the lower doors will answer.",
                 "Vega, la central eléctrica de los niveles -3 a -5 está ahí abajo. Si la restablece, las puertas inferiores responderán."))]}],
    "enter:B02": [{"if": "scp173_contained,!b02_after", "then": [{"mark": "b02_after"}]}],
}

PROPS = {
    "scp914": L("SCP-914. The dial reads: ROUGH · COARSE · 1:1 · FINE · VERY FINE.", "SCP-914. El dial dice: TOSCO · GRUESO · 1:1 · FINO · MUY FINO."),
    "iron_box": L("The box is open. Don't look inside. Don't.", "La caja está abierta. No mires dentro. No."),
    "pill_case": L("An empty cradle for the pill bottle. A label: 'SCP-500. Level 4.'", "Un soporte vacío para el frasco. Una etiqueta: 'SCP-500. Nivel 4.'"),
    "toy_pile": L("Toys, chewed on by something with no teeth.", "Juguetes, mordisqueados por algo sin dientes."),
    "cell_bunk": L("A concrete bunk. A number scratched into it with a fingernail.", "Un camastro de hormigón. Un número rayado con la uña."),
    "shower": L("Cold water still drips from the head.", "Todavía gotea agua fría de la alcachofa."),
    "control_console": L("CELL 173 CONTROL. Two buttons: OPEN, SEAL.", "CONTROL CELDA 173. Dos botones: ABRIR, SELLAR."),
}

NPC_TALK = {"adebayo": [["met_adebayo", "adebayo_again"], ["", "adebayo_first"]]}
