# The Table — segments for EN / FR / ES. Roles: N narrator (her voice copy), A Andre, D Dad, P pause (seconds).
# Each entry: (id, role, shot, {lang: caption text}) ; pause entries: (id, 'P', None, seconds)
# Optional 5th element: dict of flags, e.g. {'slow': True}

S = [
 ('p01', 'N', 's01', {
  'en': "There's a kind of quiet that isn't peace. It's the quiet of a body that has decided, all by itself, to stop moving.",
  'fr': "Il existe un silence qui n'est pas la paix. C'est le silence d'un corps qui a décidé, tout seul, de ne plus bouger.",
  'es': "Hay un tipo de silencio que no es paz. Es el silencio de un cuerpo que decidió, solito, dejar de moverse."}),
 ('p02', 'N', 's02', {
  'en': "I learned about that quiet on a massage table.",
  'fr': "J'ai découvert ce silence sur une table de massage.",
  'es': "Conocí ese silencio en una camilla de masajes."}),
 ('p03', 'N', 's03', {
  'en': "I'm a mother. I work with my hands, and I carry everything in my back. The kids, the bills, the school calls, the job. By the end of that winter I couldn't turn my head to check my blind spot.",
  'fr': "Je suis mère. Je travaille de mes mains, et je porte tout dans mon dos. Les enfants, les factures, les appels de l'école, le travail. À la fin de cet hiver-là, je ne pouvais même plus tourner la tête.",
  'es': "Soy madre. Trabajo con las manos y cargo todo en la espalda. Los hijos, las cuentas, las llamadas de la escuela, el trabajo. Al final de ese invierno ya ni podía voltear la cabeza."}),
 ('p04', 'N', 's04', {
  'en': "So I did the thing everybody says you should do. I took care of myself. I booked a massage.",
  'fr': "Alors j'ai fait ce que tout le monde conseille. J'ai pris soin de moi. J'ai réservé un massage.",
  'es': "Así que hice lo que todos dicen que hay que hacer. Me cuidé. Hice una cita para un masaje."}),
 ('p05', 'N', 's05', {
  'en': "I'd been to him before. He was licensed. His certificate hung by the door. He knew my name, asked about my children, played soft music. Nothing about that room said danger.",
  'fr': "Je le connaissais déjà. Il avait son diplôme. Son certificat était accroché près de la porte. Il connaissait mon nom, il demandait des nouvelles de mes enfants, il mettait une musique douce. Rien dans cette pièce ne disait danger.",
  'es': "Ya había ido con él antes. Tenía licencia. Su certificado colgaba junto a la puerta. Sabía mi nombre, me preguntaba por mis hijos, ponía música suave. Nada en ese cuarto decía peligro."}),
 ('p06', 'N', 's06', {
  'en': "That's the part people don't understand. It doesn't always look like danger. Sometimes it looks like a warm towel and a man who remembers your kids' names.",
  'fr': "C'est ce que les gens ne comprennent pas. Le danger n'a pas toujours l'air du danger. Parfois, il ressemble à une serviette chaude et à un homme qui se souvient du prénom de vos enfants.",
  'es': "Eso es lo que la gente no entiende. El peligro no siempre parece peligro. A veces parece una toalla tibia y un hombre que se acuerda de los nombres de tus hijos."}),
 ('p07', 'N', 's07', {
  'en': "He told me what every therapist says. \"Get comfortable. Under the sheet. I'll knock.\"",
  'fr': "Il m'a dit ce que disent tous les thérapeutes : « Installez-vous. Sous le drap. Je frapperai avant d'entrer. »",
  'es': "Me dijo lo que dicen todos los terapeutas: \"Póngase cómoda. Debajo de la sábana. Toco antes de entrar.\""}),
 ('p08', 'N', 's08', {
  'en': "I lay face down. I breathed out. For the first time in months, I let my guard all the way down.",
  'fr': "Je me suis allongée sur le ventre. J'ai respiré. Pour la première fois depuis des mois, j'ai baissé complètement ma garde.",
  'es': "Me acosté boca abajo. Solté el aire. Por primera vez en meses, bajé la guardia por completo."}),
 ('x1', 'P', 's08', 2.0, {'music': 'drop'}),
 ('p09', 'N', 's09', {
  'en': "It started the way a massage starts. Shoulders. Back. Pressure that hurt in the good way.",
  'fr': "Ça a commencé comme commence un massage. Les épaules. Le dos. Une pression qui fait du bien.",
  'es': "Empezó como empieza un masaje. Los hombros. La espalda. Una presión que dolía de la manera buena."}),
 ('p10', 'N', 's10', {
  'en': "Then his hands went somewhere a therapist's hands have no reason to go.",
  'fr': "Puis ses mains sont allées là où les mains d'un thérapeute n'ont aucune raison d'aller.",
  'es': "Luego sus manos fueron a donde las manos de un terapeuta no tienen ninguna razón de ir."}),
 ('p11', 'N', 's10', {
  'en': "The first second, I told myself I was wrong. He slipped. You're imagining it. Don't make it weird.",
  'fr': "La première seconde, je me suis dit que je me trompais. Il a glissé. Tu imagines des choses. Ne crée pas de malaise.",
  'es': "El primer segundo, me dije que me estaba equivocando. Se le resbaló la mano. Te lo estás imaginando. No hagas las cosas incómodas."}),
 ('p12', 'N', 's11', {
  'en': "The second time, there was no mistake left to believe in.",
  'fr': "La deuxième fois, il n'y avait plus d'erreur à laquelle croire.",
  'es': "La segunda vez, ya no quedaba ningún error en el cual creer."}),
 ('x2', 'P', 's11', 2.0),
 ('p13', 'N', 's11', {
  'en': "And I didn't move.",
  'fr': "Et je n'ai pas bougé.",
  'es': "Y no me moví."}, {'slow': True}),
 ('p14', 'N', 's12', {
  'en': "I didn't scream. I didn't sit up. I didn't say his name or stop. I'm a grown woman. I've stood up to principals, landlords, police officers, judges. I have never been afraid to open my mouth.",
  'fr': "Je n'ai pas crié. Je ne me suis pas relevée. Je n'ai pas dit son nom, ni arrêtez. Je suis une femme adulte. J'ai tenu tête à des directeurs d'école, à des propriétaires, à des policiers, à des juges. Je n'ai jamais eu peur d'ouvrir la bouche.",
  'es': "No grité. No me levanté. No dije su nombre, ni pare. Soy una mujer adulta. Me he enfrentado a directores de escuela, a caseros, a policías, a jueces. Nunca he tenido miedo de abrir la boca."}),
 ('p15', 'N', 's12', {
  'en': "But on that table, my mouth wouldn't open. My arms were heavy like wet sand. My heart was pounding so hard I could hear it in the pillow, and my body just… stayed.",
  'fr': "Mais sur cette table, ma bouche ne s'ouvrait pas. Mes bras étaient lourds comme du sable mouillé. Mon cœur battait si fort que je l'entendais dans le coussin, et mon corps… est resté là.",
  'es': "Pero en esa camilla, la boca no se me abría. Los brazos me pesaban como arena mojada. El corazón me latía tan fuerte que lo oía en la almohada, y mi cuerpo… se quedó ahí."}),
 ('p16', 'N', 's13', {
  'en': "I counted the holes in the face cradle. I listened to the music. I watched one strip of light under the door. I went somewhere far away and waited for it to be over.",
  'fr': "J'ai compté les trous de l'appui-tête. J'ai écouté la musique. J'ai regardé un mince filet de lumière sous la porte. Je suis partie très loin, et j'ai attendu que ce soit fini.",
  'es': "Conté los agujeros del apoyacabezas. Escuché la música. Miré una rayita de luz debajo de la puerta. Me fui muy lejos y esperé a que se terminara."}),
 ('p17', 'N', 's14', {
  'en': "That's when it happened. Not with a fight. With a freeze.",
  'fr': "C'est comme ça que c'est arrivé. Pas avec un combat. Avec un corps figé.",
  'es': "Así pasó. No con una pelea. Con un cuerpo paralizado."}, {'slow': True}),
 ('p18', 'N', 's15', {
  'en': "When it was done, he said, \"Take your time getting up.\" Like nothing. Like every other Tuesday.",
  'fr': "Quand ce fut terminé, il a dit : « Prenez votre temps pour vous relever. » Comme si de rien n'était. Comme un mardi ordinaire.",
  'es': "Cuando terminó, dijo: \"Tómese su tiempo para levantarse.\" Como si nada. Como cualquier martes."}),
 ('p19', 'N', 's16', {
  'en': "I got dressed. I paid. I tipped him.",
  'fr': "Je me suis habillée. J'ai payé. Je lui ai laissé un pourboire.",
  'es': "Me vestí. Le pagué. Le dejé propina."}),
 ('x3', 'P', 's16', 1.2),
 ('p20', 'N', 's16', {
  'en': "I tipped him. I've replayed that more than anything else.",
  'fr': "Je lui ai laissé un pourboire. C'est ce que j'ai repassé dans ma tête plus que tout le reste.",
  'es': "Le dejé propina. Eso es lo que más he repasado en mi mente."}),
 ('p21', 'N', 's17', {
  'en': "I walked to my car, locked the doors, and sat there with my keys in my lap for forty minutes. I didn't cry. I didn't call anyone. I just sat.",
  'fr': "Je suis allée jusqu'à ma voiture, j'ai verrouillé les portes, et je suis restée assise quarante minutes, les clés sur les genoux. Je n'ai pas pleuré. Je n'ai appelé personne. Je suis restée assise.",
  'es': "Caminé a mi carro, cerré los seguros y me quedé sentada cuarenta minutos con las llaves en las piernas. No lloré. No llamé a nadie. Nada más me quedé sentada."}),
 ('p22', 'N', 's18', {
  'en': "And a voice in my head asked the question I would hear a lot more after that day: Why didn't you do anything?",
  'fr': "Et une voix dans ma tête a posé la question que j'allais entendre souvent après ce jour-là : Pourquoi tu n'as rien fait ?",
  'es': "Y una voz en mi cabeza hizo la pregunta que iba a escuchar mucho después de ese día: ¿Por qué no hiciste nada?"}),
 ('x4', 'P', 's18', 1.5),
 ('p23', 'N', 's19', {
  'en': "For weeks, I didn't do anything.",
  'fr': "Pendant des semaines, je n'ai rien fait.",
  'es': "Durante semanas, no hice nada."}),
 ('p24', 'N', 's19', {
  'en': "I went to work. I signed permission slips. I cooked. From the outside I looked fine. Inside, my thoughts ran like cars on a freeway with no exits.",
  'fr': "J'allais au travail. Je signais les autorisations de l'école. Je cuisinais. De l'extérieur, j'avais l'air bien. À l'intérieur, mes pensées tournaient comme des voitures sur une autoroute sans sortie.",
  'es': "Iba al trabajo. Firmaba los permisos de la escuela. Cocinaba. Por fuera me veía bien. Por dentro, mis pensamientos corrían como carros en una autopista sin salidas."}),
 ('p25', 'N', 's20', {
  'en': "Was it real? Did I lead him on? Who would believe me? He has a license. I have a temper, and everybody knows it.",
  'fr': "Est-ce que c'était réel ? Est-ce que je l'ai encouragé ? Qui va me croire ? Lui, il a un diplôme. Moi, j'ai du caractère, et tout le monde le sait.",
  'es': "¿Fue real? ¿Yo le di pie? ¿Quién me va a creer? Él tiene licencia. Yo tengo carácter, y todo el mundo lo sabe."}),
 ('p26', 'N', 's21', {
  'en': "I'd sit on the edge of my bed for an hour and not remember sitting down.",
  'fr': "Je m'asseyais au bord du lit pendant une heure sans me souvenir de m'être assise.",
  'es': "Me sentaba en la orilla de la cama una hora entera sin acordarme de haberme sentado."}),
 ('p27', 'N', 's22', {
  'en': "Finally, I told my boyfriend, Andre. I chose the words carefully, like setting down glass.",
  'fr': "Finalement, je l'ai dit à mon compagnon, André. J'ai choisi mes mots avec soin, comme on pose du verre.",
  'es': "Por fin se lo conté a mi novio, Andre. Escogí las palabras con cuidado, como quien pone un vaso en la mesa."}),
 ('p28', 'N', 's22', {
  'en': "He was quiet. Then he asked, not mean, just tired:",
  'fr': "Il est resté silencieux. Puis il a demandé, pas méchamment, juste fatigué :",
  'es': "Se quedó callado. Luego preguntó, no con maldad, solo cansado:"}),
 ('a1', 'A', 's23', {
  'en': "What did you have on?",
  'fr': "Qu'est-ce que tu portais ?",
  'es': "¿Qué llevabas puesto?"}),
 ('x5', 'P', 's23', 2.0),
 ('p30', 'N', 's24', {
  'en': "A sheet. I had on a sheet. That's what you wear at a massage. That's what everybody wears.",
  'fr': "Un drap. Je portais un drap. C'est ce qu'on porte pour un massage. C'est ce que tout le monde porte.",
  'es': "Una sábana. Llevaba una sábana. Eso es lo que uno lleva en un masaje. Eso es lo que lleva todo el mundo."}),
 ('p31', 'N', 's24', {
  'en': "I know he didn't mean to put it on me. But that question landed right where the freeze already lived. Because underneath what did you have on is what did you do to cause it.",
  'fr': "Je sais qu'il ne voulait pas me rendre responsable. Mais cette question est tombée exactement là où vivait déjà le silence. Parce que sous qu'est-ce que tu portais, il y a qu'est-ce que tu as fait pour que ça arrive.",
  'es': "Sé que no quiso echarme la culpa. Pero esa pregunta cayó justo donde ya vivía el silencio. Porque debajo de ¿qué llevabas puesto? está ¿qué hiciste para que pasara?"}),
 ('p32', 'N', 's25', {
  'en': "Then I told my dad. My dad loves me loud. He wanted to drive over there that night. When I said no, he said,",
  'fr': "Ensuite, je l'ai dit à mon père. Mon père m'aime fort et bruyamment. Il voulait y aller le soir même. Quand j'ai dit non, il a dit :",
  'es': "Después se lo conté a mi papá. Mi papá me quiere en voz alta. Quería ir esa misma noche. Cuando le dije que no, me dijo:"}),
 ('d1', 'D', 's25', {
  'en': "Then let it go, baby girl. You know how you get. Don't make it bigger than it is.",
  'fr': "Alors laisse tomber, ma fille. Tu sais comment tu es. N'en fais pas une montagne.",
  'es': "Entonces déjalo así, mija. Tú sabes cómo te pones. No lo hagas más grande de lo que es."}),
 ('p34', 'N', 's26', {
  'en': "Between the two of them, I heard the same message: Either you caused it, or you're overreacting to it.",
  'fr': "Entre les deux, j'ai entendu le même message : Soit c'est ta faute, soit tu exagères.",
  'es': "Entre los dos, escuché el mismo mensaje: O tú lo provocaste, o estás exagerando."}),
 ('p35', 'N', 's26', {
  'en': "So I went quiet again. And the quiet got heavier every day.",
  'fr': "Alors je me suis tue à nouveau. Et ce silence devenait plus lourd chaque jour.",
  'es': "Así que me volví a quedar callada. Y ese silencio pesaba más cada día."}),
 ('x6', 'P', 's26', 1.5),
 ('p36', 'N', 's27', {
  'en': "One night, I read about something called the freeze response.",
  'fr': "Un soir, j'ai lu quelque chose sur la réaction de sidération.",
  'es': "Una noche leí sobre algo que se llama la respuesta de congelamiento."}),
 ('p37', 'N', 's27', {
  'en': "When the brain decides a threat can't be fought or outrun, it can shut the body down. Muscles go heavy. The voice locks. It isn't agreement. It isn't weakness. It's survival, happening faster than thought.",
  'fr': "Quand le cerveau décide qu'on ne peut ni se battre ni fuir, il peut mettre le corps à l'arrêt. Les muscles deviennent lourds. La voix se bloque. Ce n'est pas un consentement. Ce n'est pas de la faiblesse. C'est de la survie, plus rapide que la pensée.",
  'es': "Cuando el cerebro decide que no se puede pelear ni huir, puede apagar el cuerpo. Los músculos se ponen pesados. La voz se traba. No es consentimiento. No es debilidad. Es supervivencia, más rápida que el pensamiento."}),
 ('p38', 'N', 's28', {
  'en': "I sat on my kitchen floor and cried for the first time since the table. Not because I was broken. Because I finally understood I wasn't.",
  'fr': "Je me suis assise par terre dans la cuisine, et j'ai pleuré pour la première fois depuis la table. Pas parce que j'étais brisée. Parce que j'ai enfin compris que je ne l'étais pas.",
  'es': "Me senté en el piso de la cocina y lloré por primera vez desde la camilla. No porque estuviera rota. Porque por fin entendí que no lo estaba."}),
 ('p39', 'N', 's28', {
  'en': "I didn't do nothing. My body was protecting me the only way it knew how.",
  'fr': "Je n'ai pas « rien fait ». Mon corps me protégeait de la seule manière qu'il connaissait.",
  'es': "No es que no hice nada. Mi cuerpo me estaba protegiendo de la única manera que sabía."}),
 ('p40', 'N', 's29', {
  'en': "The next morning I called the state licensing board. I filed a complaint. I made a police report. I wrote it all down, every date, every detail I could remember.",
  'fr': "Le lendemain matin, j'ai appelé l'ordre professionnel. J'ai porté plainte. J'ai fait une déposition à la police. J'ai tout écrit, chaque date, chaque détail dont je me souvenais.",
  'es': "A la mañana siguiente llamé a la junta de licencias del estado. Puse una queja. Hice una denuncia en la policía. Lo escribí todo, cada fecha, cada detalle que recordaba."}),
 ('p41', 'N', 's30', {
  'en': "And the people around me said what they always say. \"You're doing too much.\" \"Why now?\" \"You waited all that time, and now you want to blow it up?\"",
  'fr': "Et autour de moi, les gens ont dit ce qu'ils disent toujours. « Tu en fais trop. » « Pourquoi maintenant ? » « Tu as attendu tout ce temps, et maintenant tu veux tout faire exploser ? »",
  'es': "Y la gente a mi alrededor dijo lo que siempre dice. \"Estás exagerando.\" \"¿Por qué ahora?\" \"Esperaste todo ese tiempo, ¿y ahora quieres armar un escándalo?\""}),
 ('p42', 'N', 's30', {
  'en': "I didn't rush. I carried it by myself until it got too heavy to carry. That's not too much. That's the exact right amount.",
  'fr': "Je ne me suis pas précipitée. J'ai porté ce poids seule jusqu'à ce qu'il soit trop lourd. Ce n'est pas trop. C'est exactement ce qu'il fallait.",
  'es': "No me apresuré. Lo cargué sola hasta que pesó demasiado. Eso no es exagerar. Eso es exactamente lo justo."}),
 ('p43', 'N', 's31', {
  'en': "Andre came around. Weeks later he sat next to me and said,",
  'fr': "André a fini par comprendre. Des semaines plus tard, il s'est assis près de moi et m'a dit :",
  'es': "Andre al final entendió. Semanas después se sentó a mi lado y me dijo:"}),
 ('a2', 'A', 's31', {
  'en': "I asked you the wrong question. I'm sorry.",
  'fr': "Je t'ai posé la mauvaise question. Pardonne-moi.",
  'es': "Te hice la pregunta equivocada. Perdóname."}),
 ('p45', 'N', 's32', {
  'en': "My dad still doesn't fully get it. But he drove me to the hearing. Love doesn't always understand. Sometimes love just shows up.",
  'fr': "Mon père ne comprend toujours pas tout. Mais il m'a conduite à l'audience. L'amour ne comprend pas toujours. Parfois, l'amour est simplement là.",
  'es': "Mi papá todavía no lo entiende del todo. Pero me llevó a la audiencia. El amor no siempre entiende. A veces el amor simplemente llega."}),
 ('x7', 'P', 's33', 1.2, {'music': 'rise'}),
 ('p46', 'N', 's33', {
  'en': "The Bible says, \"The Lord is nigh unto them that are of a broken heart; and saveth such as be of a contrite spirit.\" Psalm 34:18.",
  'fr': "La Bible dit : « L'Éternel est près de ceux qui ont le cœur brisé, et il sauve ceux qui ont l'esprit dans l'abattement. » Psaume 34:19.",
  'es': "La Biblia dice: \"Cercano está Jehová a los quebrantados de corazón; y salva a los contritos de espíritu.\" Salmo 34:18."}),
 ('p47', 'N', 's33', {
  'en': "And I hold on to this one: \"For there is nothing covered, that shall not be revealed; neither hid, that shall not be known.\" Luke 12:2.",
  'fr': "Et je m'accroche à celui-ci : « Il n'y a rien de caché qui ne doive être découvert, ni de secret qui ne doive être connu. » Luc 12:2.",
  'es': "Y me agarro de este: \"Porque nada hay encubierto, que no haya de descubrirse; ni oculto, que no haya de saberse.\" Lucas 12:2."}),
 ('p48', 'N', 's34', {
  'en': "If you froze, you did not consent. If you waited, you were not lying. If you finally spoke, you were not doing too much.",
  'fr': "Si votre corps s'est figé, vous n'avez pas consenti. Si vous avez attendu, vous ne mentiez pas. Si vous avez enfin parlé, vous n'en faisiez pas trop.",
  'es': "Si te quedaste paralizada, no diste tu consentimiento. Si esperaste, no estabas mintiendo. Si por fin hablaste, no estabas exagerando."}),
 ('p49', 'N', 's34', {
  'en': "Have you ever been asked the wrong question after something happened to you? Tell me in the comments. Somebody reading needs to know they're not the only one.",
  'fr': "Bien-aimés, vous a-t-on déjà posé la mauvaise question après ce qui vous est arrivé ? Écrivez-le en commentaire. Quelqu'un qui lit a besoin de savoir qu'il n'est pas seul.",
  'es': "¿Alguna vez te hicieron la pregunta equivocada después de lo que te pasó? Cuéntamelo en los comentarios. Y etiqueta a alguien que necesite escuchar esto. Alguien que está leyendo necesita saber que no es la única."}),
 ('x8', 'P', 'END', 1.0),
 ('p50', 'N', 'END', {
  'en': "If this happened to you, you don't have to carry it alone. Open the Community Covenant app. The link is in the description. If you're in the U.S. and want to talk to a lawyer, the free legal referral form is in the description too. It's free to ask and free to be matched. We are not attorneys, and this is not legal advice. It's a referral to someone who is.",
  'fr': "Si cela vous est arrivé, vous n'avez pas à porter ce poids seule. Ouvrez l'application Community Covenant. Le lien est dans la description. Si vous êtes en danger maintenant, appelez le numéro d'urgence de votre pays. Que Dieu vous bénisse et vous garde.",
  'es': "Si esto te pasó a ti, no tienes que cargarlo sola. Abre la aplicación Community Covenant. El enlace está en la descripción. Si estás en Estados Unidos y quieres hablar con un abogado, el formulario gratuito de referencia legal también está en la descripción. No somos abogados y esto no es asesoría legal."}),
 ('p51', 'N', 'END', {
  'en': "If you're in danger right now, call 911. In the U.S., you can call the National Sexual Assault Hotline at 1-800-656-4673, any time, day or night. If you're thinking about hurting yourself, call or text 988.",
  'es': "Si estás en peligro ahora mismo, llama al 911. En Estados Unidos puedes llamar a la línea nacional de agresión sexual al 1-800-656-4673, a cualquier hora. Si estás pensando en hacerte daño, llama o envía un texto al 988 y marca 2 para español. Fuera de Estados Unidos, llama al número de emergencia de tu país. Que Dios te bendiga a ti y a tu familia."}),
]

# spoken forms (what the voice reads) where captions use digits/abbreviations
SAY = {
 'en': [("Psalm 34:18", "Psalm thirty-four, verse eighteen"), ("Luke 12:2", "Luke twelve, verse two"),
        ("1-800-656-4673", "one, eight hundred, six five six, four six seven three"), ("911", "nine one one"),
        ("988", "nine eight eight"), ("the U.S.", "the U S"), ("U.S.", "U S"), ("…", ",")],
 'fr': [("Psaume 34:19", "Psaume trente-quatre, verset dix-neuf"), ("Luc 12:2", "Luc douze, verset deux"),
        ("« ", ""), (" »", ""), ("…", ",")],
 'es': [("Salmo 34:18", "Salmo treinta y cuatro, versículo dieciocho"), ("Lucas 12:2", "Lucas doce, versículo dos"),
        ("1-800-656-4673", "uno, ochocientos, seis cinco seis, cuatro seis siete tres"), ("911", "nueve uno uno"),
        ("988", "nueve ocho ocho"), ("marca 2", "marca dos"), ("…", ",")],
}

def say(lang, t):
    for a, b in SAY[lang]: t = t.replace(a, b)
    return t.replace('"', '')

TITLE = {'en': "I Froze On The Table. Then They Asked What I Had On.",
         'fr': "Je me suis figée sur la table. Puis on m'a demandé ce que je portais.",
         'es': "Me quedé paralizada en la camilla. Luego me preguntaron qué llevaba puesto."}
THUMB = {'en': "I FROZE", 'fr': "JE ME SUIS FIGÉE", 'es': "ME QUEDÉ PARALIZADA"}
WARN = {'en': "Content note: this story discusses sexual assault. No graphic details.",
        'fr': "Avertissement : cette histoire parle d'agression sexuelle. Aucun détail explicite.",
        'es': "Aviso: esta historia habla de agresión sexual. Sin detalles explícitos."}
NAMES = {'A': {'en': 'ANDRE', 'fr': 'ANDRÉ', 'es': 'ANDRE'}, 'D': {'en': 'DAD', 'fr': 'PAPA', 'es': 'PAPÁ'}}
