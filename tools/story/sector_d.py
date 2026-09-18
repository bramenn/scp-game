"""Act IV — Medical Wing. SCP-049, the Plague Doctor. Dr. Lin. Lavender."""
from common import L, say, choice

N, R, V, LN, D = "", "radio", "vega", "lin", "scp049"

QUESTS = {
    "main_049": dict(main=True, name=L("The Plague Doctor", "El Doctor de la Peste"), stages=[
        L("Someone is barricaded in the pharmacy. Find out who.", "Alguien se ha atrincherado en la farmacia. Averigua quién."),
        L("Dr. Lin: lavender calms SCP-049. Get some from the greenhouse.", "Dra. Lin: la lavanda calma a SCP-049. Consigue un poco en el invernadero."),
        L("Find SCP-049 in the wards. Carry the lavender. Talk to it.", "Encuentra a SCP-049 en las salas. Lleva la lavanda. Habla con él."),
        L("SCP-049 is following you. Lead it to its cell, south of the wards.", "SCP-049 te sigue. Llévalo a su celda, al sur de las salas."),
        L("Return to Dr. Lin in the pharmacy.", "Vuelve con la Dra. Lin en la farmacia."),
    ]),
}

DOCS = {
    "doc_049_notice": dict(title=L("Staff notice - SCP-049", "Aviso al personal - SCP-049"), body=L(
        "SCP-049 is a humanoid, 1.9 m, resembling a medieval plague doctor. Its robes and mask appear to grow from its body. "
        "Direct skin contact is lethal. It believes it is curing a disease it calls 'the Pestilence', and becomes hostile "
        "to anyone it thinks is infected.\n\nLavender has proven effective at calming its outbursts. Keep sprigs at every "
        "post. Do NOT argue with it about medicine.",
        "SCP-049 es un humanoide de 1,9 m que se parece a un médico de la peste medieval. Su túnica y su máscara parecen "
        "crecerle del cuerpo. El contacto directo con la piel es letal. Cree estar curando una enfermedad que llama 'la "
        "Pestilencia' y se vuelve hostil con quien cree infectado.\n\nLa lavanda ha resultado eficaz para calmar sus "
        "arrebatos. Tengan ramitas en cada puesto. NO discutan de medicina con él."),
        source="SCP-049 by Gabriel Jade & djkaktus · scp-wiki.wikidot.com/scp-049 · CC BY-SA 3.0"),
    "doc_049_interview": dict(title=L("Interview 049-B (excerpt)", "Entrevista 049-B (extracto)"), body=L(
        "Dr. Hamm: What do you call yourself?\nSCP-049: A medical man, such as myself. Wonders abound!\n"
        "Dr. Hamm: The subjects you operate on die.\nSCP-049: They are cured. I am the only one who can do this. My work "
        "must continue.\n\n[Note: SCP-049 speaks English and medieval French fluently. It remains cordial throughout.]",
        "Dr. Hamm: ¿Cómo se llama a sí mismo?\nSCP-049: Un hombre de medicina, como yo. ¡Abundan las maravillas!\n"
        "Dr. Hamm: Los sujetos que opera mueren.\nSCP-049: Están curados. Soy el único que puede hacer esto. Mi trabajo "
        "debe continuar.\n\n[Nota: SCP-049 habla inglés y francés medieval con fluidez. Se mantiene cordial en todo momento.]"),
        source="SCP-049 by Gabriel Jade & djkaktus · scp-wiki.wikidot.com/scp-049 · CC BY-SA 3.0"),
    "doc_ward_chart": dict(title=L("Patient chart, ward 3", "Historia clínica, sala 3"), body=L(
        "Patient: D-3312. Admitted 02:50 for 'pre-transfer health check' (HCZ, Tuesday).\nNote in a different hand, 04:10: "
        "'Cured.' The handwriting is beautiful, old-fashioned, with long loops.",
        "Paciente: D-3312. Ingresa a las 02:50 para 'revisión previa al traslado' (ZCP, martes).\nNota con otra letra, 04:10: "
        "'Curado.' La letra es preciosa, anticuada, con largos bucles.")),
    "doc_morgue_tag": dict(title=L("Toe tag", "Etiqueta de pie"), body=L(
        "NAME: [blank]. NUMBER: D-4417-B. CAUSE: [blank]. RELEASE TO: Black Tide / HCZ.\n\n4417. That's Nico's number, "
        "with a B. Someone was already filling in the paperwork for his body.",
        "NOMBRE: [en blanco]. NÚMERO: D-4417-B. CAUSA: [en blanco]. ENTREGAR A: Marea Negra / ZCP.\n\n4417. Es el número de "
        "Nico, con una B. Alguien ya estaba rellenando los papeles de su cadáver."), sanity=-4),
    "doc_cold_storage": dict(title=L("Inventory, cold storage", "Inventario, cámara frigorífica"), body=L(
        "Bodies from 682 trial #29 to #33: returned 'incomplete'. Stored pending amnestic sign-off. Do not show to D-class.",
        "Cadáveres de la prueba 682 n.º 29 a n.º 33: devueltos 'incompletos'. Almacenados hasta la firma de amnésicos. No "
        "mostrar a los Clase-D.")),
    "doc_049_journal": dict(title=L("A journal in French", "Un diario en francés"), body=L(
        "Pages of elegant handwriting in old French. You understand one line, underlined twice: 'La Pestilence est dans les "
        "murs de ce lieu, et ceux qui le gouvernent en sont la source.'\n(The Pestilence is in the walls of this place, and "
        "those who govern it are its source.)",
        "Páginas de letra elegante en francés antiguo. Entiendes una línea, subrayada dos veces: 'La Pestilence est dans les "
        "murs de ce lieu, et ceux qui le gouvernent en sont la source.'\n(La Pestilencia está en los muros de este lugar, y "
        "quienes lo gobiernan son su origen.)")),
}

EVENTS = {
    "enter:D01": [{"if": "!d01_seen", "then": [{"mark": "d01_seen"}, {"wait": 0.5},
        say(N, L("The medical wing. Two patients sit upright on the waiting bench, perfectly still. Their chests are stitched shut.",
                 "El ala médica. Dos pacientes están sentados en el banco de espera, completamente quietos. Tienen el pecho cosido.")),
        {"sfx": "049_hum", "db": -10},
        {"quest": ["main_049", 1]},
        {"objective": L("Someone is in the pharmacy (south door).", "Hay alguien en la farmacia (puerta sur).")}]}],
    "d01_pharmacy_door": [
        {"if": "lin_opened", "then": [say(N, L("The door is open.", "La puerta está abierta."))], "else": [
            {"sfx": "hit", "db": -6},
            say(LN, L("Go away! Go away, I'm not sick, I'm not—", "¡Vete! ¡Vete, no estoy enferma, no estoy...!"),
                L("...You knocked. They don't knock. Prove you're not one of his. What does 049 call the disease?",
                  "...Has llamado. Ellos no llaman. Demuestra que no eres uno de los suyos. ¿Cómo llama 049 a la enfermedad?")),
            choice(LN, "",
                   (L("The Plague", "La Plaga"), [say(LN, L("No. Go away.", "No. Vete."))]),
                   (L("The Pestilence", "La Pestilencia"), [
                       {"sfx": "lock_click"}, {"mark": "lin_opened"}, {"call": "refresh_doors"}, {"door": "D01_pharmacy", "open": True},
                       say(LN, L("...Come in. Quickly.", "...Pasa. Rápido."))]),
                   (L("The Rot", "La Podredumbre"), [say(LN, L("No. You'd know if you'd read the notice. Go away.", "No. Lo sabrías si hubieras leído el aviso. Vete."))]))]}],
    "lin_first": [
        {"mark": "met_lin"},
        say(LN, L("Lin. Medical director of this wing. Former. Everyone I directed is on those benches now.", "Lin. Directora médica de esta ala. Antigua. Todos a los que dirigía están ahora en esos bancos."),
            L("049 walked out of its cell at 03:12 and started 'treating' the night shift. It's very polite about it.",
              "049 salió de su celda a las 03:12 y empezó a 'tratar' al turno de noche. Es muy educado.")),
        choice(LN, "",
               (L("How do we get it back in its cell?", "¿Cómo lo devolvemos a su celda?"), [
                   say(LN, L("You ask it. Nicely. It isn't an animal, it's a doctor. A doctor with a patient list.", "Se lo pides. Con educación. No es un animal, es un médico. Un médico con una lista de pacientes."),
                       L("Lavender calms it. There's a greenhouse past the wards. Carry some, and it will listen.", "La lavanda lo calma. Hay un invernadero más allá de las salas. Lleva un poco y te escuchará."))]),
               (L("You knew Elena Vega?", "¿Conocías a Elena Vega?"), [
                   say(LN, L("She took two SCP-500 pills from the vault at 03:40. 'For the core', she said. Someone down there is sick. Or will be.",
                             "Se llevó dos píldoras SCP-500 de la bóveda a las 03:40. 'Para el núcleo', dijo. Alguien ahí abajo está enfermo. O lo estará."))])),
        say(LN, L("And... Vega. Before you judge me for hiding: I signed the health checks for Black Tide. Forty of them. I told myself it was paperwork.",
                  "Y... Vega. Antes de que me juzgues por esconderme: firmé las revisiones médicas de Marea Negra. Cuarenta. Me dije que era papeleo."),
            L("049 says the Pestilence is in the people who run this place. Some nights I think it's right.",
              "049 dice que la Pestilencia está en quienes gobiernan este lugar. Algunas noches creo que tiene razón.")),
        {"quest": ["main_049", 2]},
        {"objective": L("Get lavender from the greenhouse (east of the wards).", "Consigue lavanda en el invernadero (al este de las salas).")},
    ],
    "lin_again": [
        {"if": "scp049_contained,!lin_reward", "then": [
            say(LN, L("It's back in its room. You actually did it. It walked in by itself?", "Ha vuelto a su habitación. Lo has conseguido. ¿Entró solo?"),
                L("Take my card. Level 4. Heavy Containment. And this - the hood. From the 096 retrieval. If you ever see that thing, never, ever look at its face.",
                  "Toma mi tarjeta. Nivel 4. Contención Pesada. Y esto: la capucha. De la recuperación de 096. Si alguna vez ves esa cosa, nunca, jamás, le mires la cara."),
                L("Reyes, the last Nine-Tailed Fox, radioed from HCZ an hour ago. Find him. He'll know what's left down there.",
                  "Reyes, el último de Nueve Colas, llamó por radio desde ZCP hace una hora. Encuéntralo. Sabrá qué queda ahí abajo.")),
            {"give": "card_4"}, {"give": "bag096"}, {"mark": "lin_reward"}, {"quest": ["main_049", -1]},
            {"objective": L("Take the Heavy Containment lift (maintenance junction, south-east door, Level 4).",
                            "Toma el ascensor de Contención Pesada (cruce de mantenimiento, puerta sureste, nivel 4).")},
            {"save": True}],
         "else": [{"if": "scp049_contained", "then": [say(LN, L("Go. And come back alive, please. I'm tired of signing things.", "Vete. Y vuelve vivo, por favor. Estoy cansada de firmar cosas."))],
                   "else": [say(LN, L("Lavender. Then talk to it. Don't let it touch you. Don't argue about medicine.", "Lavanda. Luego habla con él. No dejes que te toque. No discutas de medicina."))]}]},
    ],
    "item:lavender": [{"if": "met_lin", "then": [{"quest": ["main_049", 3]},
        {"objective": L("Find SCP-049 in the wards. Talk to it with the lavender.", "Encuentra a SCP-049 en las salas. Háblale con la lavanda.")}]}],
    "d02_enter": [{"if": "!d02_seen", "then": [{"mark": "d02_seen"},
        say(N, L("Somewhere among the beds, a low humming. An old tune. Someone is working.", "En algún lugar entre las camas, un zumbido grave. Una melodía antigua. Alguien está trabajando."))]}],
    "d03_enter": [{"if": "!d03_seen", "then": [{"mark": "d03_seen"},
        say(N, L("The operating table is still warm. The instruments are laid out in perfect order, cleaned, ready.",
                 "La mesa de operaciones sigue tibia. Los instrumentos están colocados en orden perfecto, limpios, listos.")), {"sanity": -5}]}],
    "d04_drawer": [{"sfx": "hit", "db": 2}, {"shake": 0.4, "power": 2}, {"wait": 0.6}, {"sfx": "hit", "db": 0}, {"wait": 0.9}, {"sfx": "hit", "db": -2},
        say(N, L("Something knocks from inside one of the drawers. Three times. Then it stops.", "Algo golpea desde dentro de uno de los cajones. Tres veces. Luego para.")), {"sanity": -7}],
    # ---------------------------------------------------------------- 049
    "scp049_meet": [
        {"if": "follow049", "then": [say(D, L("Lead on, doctor. I will follow.", "Guíe usted, doctor. Le sigo."))], "else": [
            {"music": "079"},
            {"if": "item:lavender", "then": [
                say(D, L("Ah. Lavender. How civilized.", "Ah. Lavanda. Qué civilizado."),
                    L("You are not one of the sick ones. Not yet. Tell me, colleague: why have you come to my ward?",
                      "Usted no es de los enfermos. Todavía no. Dígame, colega: ¿por qué ha venido a mi sala?")),
                choice(D, "",
                       (L("The Pestilence is spreading here. Your study is safer.", "La Pestilencia se extiende aquí. Su estudio es más seguro."), [
                           say(D, L("You understand. The Pestilence is everywhere tonight. It walked out of the cells with the others.",
                                    "Lo entiende. La Pestilencia está por todas partes esta noche. Salió de las celdas con los demás."),
                               L("Very well. Take me to my study. I have notes to write.", "Muy bien. Lléveme a mi estudio. Tengo notas que escribir.")),
                           {"mark": "follow049"}, {"quest": ["main_049", 4]},
                           {"objective": L("Lead SCP-049 to its cell (south of the wards).", "Lleva a SCP-049 a su celda (al sur de las salas).")}]),
                       (L("You're killing people.", "Está matando gente."), [
                           say(D, L("I am curing them. You would understand if you were a physician. Are you questioning my methods?",
                                    "Los estoy curando. Lo entendería si fuera médico. ¿Cuestiona mis métodos?")),
                           choice(D, "",
                                  (L("No, doctor. Forgive me.", "No, doctor. Perdóneme."), [say(D, L("Forgiven. Now, if you'll excuse me.", "Perdonado. Ahora, si me disculpa."))]),
                                  (L("Yes.", "Sí."), [say(D, L("Then you are sick too. Hold still.", "Entonces usted también está enfermo. Quieto.")),
                                                    {"sfx": "049_hum", "db": 4}, {"flash": 2, "color": "#000000"}, {"hp": -200, "cause": "049"}]))]),
                       (L("Nothing. Excuse me.", "Nada. Disculpe."), [say(D, L("Of course.", "Por supuesto."))]))],
             "else": [
                say(D, L("Ah. Another one. I sense it in you... faint. Early. The Pestilence.", "Ah. Otro más. Lo percibo en usted... tenue. Temprano. La Pestilencia."),
                    L("Hold still, please. This will not take long.", "Quieto, por favor. No tardaré.")),
                choice(D, "",
                       (L("Back away slowly.", "Retroceder despacio."), [say(D, L("You cannot outrun a disease, my friend. But go. I have other patients.", "No se puede huir de una enfermedad, amigo mío. Pero váyase. Tengo otros pacientes.")), {"sanity": -8}]),
                       (L("Hold still.", "Quedarse quieto."), [say(D, L("...Hm. Not yet. Come back to me when it has progressed.", "...Hm. Todavía no. Vuelva cuando haya avanzado.")), {"sanity": -12}]),
                       (L("Don't touch me!", "¡No me toque!"), [say(D, L("Panic is a symptom.", "El pánico es un síntoma.")),
                                                             {"flash": 2, "color": "#000000"}, {"hp": -200, "cause": "049"}]))]},
            {"music": ""}]}],
    "d08_contain": [
        say(D, L("My study. My books. Someone has moved my candles.", "Mi estudio. Mis libros. Alguien ha movido mis velas."),
            L("Thank you, colleague. Close the door when you leave. The Pestilence is out there. Not in here.",
              "Gracias, colega. Cierre la puerta al salir. La Pestilencia está ahí fuera. No aquí dentro.")),
        {"call": "contain049"},
        say(D, L("And... your sister. She visited me once. She had the Pestilence very badly, the guilt kind. I told her she would find her cure. I hope she did.",
                 "Y... su hermana. Me visitó una vez. Tenía muy avanzada la Pestilencia, la de la culpa. Le dije que encontraría su cura. Espero que la encontrara.")),
        {"quest": ["main_049", 5]},
        {"objective": L("Return to Dr. Lin in the pharmacy.", "Vuelve con la Dra. Lin en la farmacia.")},
        {"save": True},
    ],
}

PROPS = {
    "operating_lamp": L("The lamp is still on. Someone was operating a few minutes ago.", "La lámpara sigue encendida. Alguien estaba operando hace unos minutos."),
    "morgue_drawers": L("Steel drawers. One of them is warm.", "Cajones de acero. Uno de ellos está tibio."),
    "cryo_tank": L("Frost on the glass. Something inside, curled up.", "Escarcha en el cristal. Algo dentro, encogido."),
    "lavender_bed": L("Lavender. The smell cuts through the rot.", "Lavanda. El olor atraviesa la podredumbre."),
    "grow_rack": L("Hydroponic racks under purple lights.", "Estanterías hidropónicas bajo luces moradas."),
    "med_bed": L("The sheets are folded back neatly. The patient was 'cured'.", "Las sábanas están dobladas con esmero. El paciente fue 'curado'."),
    "body_cured": L("A long, neat Y-incision, stitched with care. The eyes are open.", "Una larga incisión en Y, cosida con cuidado. Los ojos están abiertos."),
}

NPC_TALK = {"lin": [["met_lin", "lin_again"], ["", "lin_first"]]}
