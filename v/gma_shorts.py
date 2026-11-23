# v2 Shorts for older women (65+) — English + Spanish, big on-screen text, her voice.
# Each Short points to a related long video already on Community Covenant.
SHORTS = {
 'g1': {
  'link': {'en': ('Walking With Grandma', '9m6-9LMb_-U'), 'es': ('Caminando con la abuela', 'BeCqzWpINZw')},
  'big': {'en': ["3:00 A.M.", "HER LIGHT\nCAME ON", "40 YEARS\nOF NAMES", "MINE WAS\nON EVERY PAGE", "I CAME\nBACK", "WHO PRAYS\nFOR YOU?"],
          'es': ["3:00 A.M.", "SE PRENDÍA\nSU LUZ", "40 AÑOS\nDE NOMBRES", "EL MÍO EN\nCADA PÁGINA", "VOLVÍ", "¿QUIÉN ORA\nPOR TI?"]},
  'lines': {'en': ["Every night at three in the morning, my grandmother's light came on.",
                   "I thought she just couldn't sleep.",
                   "At her funeral, I found her notebook. Forty years of names.",
                   "Mine was on every page. Next to my worst year, she wrote: Lord, keep her alive until she comes back to You.",
                   "I came back. And she lived to see it.",
                   "Grandma, who are you praying for tonight? Watch Walking With Grandma on our channel."],
            'es': ["Cada noche a las tres de la mañana, se prendía la luz de mi abuela.",
                   "Yo pensaba que simplemente no podía dormir.",
                   "En su funeral encontré su cuaderno. Cuarenta años de nombres.",
                   "El mío estaba en cada página. Junto a mi peor año, escribió: Señor, guárdala viva hasta que vuelva a Ti.",
                   "Volví. Y ella alcanzó a verlo.",
                   "Abuela, ¿por quién estás orando esta noche? Mira Caminando con la abuela en nuestro canal."]},
  'shots': ['gA', 'gB', 'gC', 'gC', 'gD', 'gE'],
 },
 'g2': {
  'link': {'en': ('The Sealed Prayers', 'i7AOs43k8sc'), 'es': ('Las oraciones selladas', '-VTRWLW7QmA')},
  'big': {'en': ["NO MONEY.\nNO LAWYERS.", "A KITCHEN\nTABLE", "AND TWO\nKNEES", "EVERY BILL.\nEVERY CHILD.", "ALL 5 OF US\nSTANDING", "TYPE\nAMEN"],
          'es': ["SIN DINERO.\nSIN ABOGADOS.", "UNA MESA\nDE COCINA", "Y DOS\nRODILLAS", "CADA CUENTA.\nCADA HIJO.", "LOS 5\nDE PIE", "ESCRIBE\nAMÉN"]},
  'lines': {'en': ["My mother never had money for lawyers, doctors, or second chances.",
                   "She had a kitchen table.",
                   "And two knees.",
                   "Every bill, every court date, every child who ran off. She laid it on that table, and she prayed.",
                   "Forty years later, all five of us are still standing.",
                   "If your mama prayed you through, type Amen. The full story, The Sealed Prayers, is on our channel."],
            'es': ["Mi madre nunca tuvo dinero para abogados, doctores ni segundas oportunidades.",
                   "Tenía una mesa de cocina.",
                   "Y dos rodillas.",
                   "Cada cuenta, cada citación, cada hijo que se fue. Lo ponía sobre esa mesa, y oraba.",
                   "Cuarenta años después, los cinco seguimos de pie.",
                   "Si tu madre te sostuvo con oración, escribe Amén. La historia completa, Las oraciones selladas, está en nuestro canal."]},
  'shots': ['mA', 'mB', 'mC', 'mD', 'mE', 'mF'],
 },
}
STY = ", vertical portrait composition, cinematic film still, warm soft light, photorealistic, 35mm, emotional, dignified"
G_EN = "elderly African American grandmother in her 70s, silver hair, reading glasses, cardigan"
G_ES = "elderly Mexican grandmother in her 70s, silver hair in a bun, shawl"
SHOTS = {}
for sfx, G in (('', G_EN), ('s', G_ES)):
    SHOTS.update({
     'gA'+sfx: f"Night, small house window glowing at 3 a.m., inside a {G} kneeling in prayer by her bed under a lamp" + STY,
     'gB'+sfx: f"Young woman in her 20s lying awake in bed at night, seeing a sliver of lamplight under her grandmother's door" + STY,
     'gC'+sfx: f"Close-up of hands holding an old worn handwritten prayer notebook full of names, a funeral flower nearby" + STY,
     'gD'+sfx: f"A young woman hugging a frail {G} who smiles with tears, sunlit living room" + STY,
     'gE'+sfx: f"Portrait of a {G} praying with eyes closed, hands folded on a Bible, soft lamp light" + STY,
     'mA'+sfx: f"A tired {G.replace('grandmother in her 70s','mother in her 40s, 1980s')} sitting at a kitchen table covered in unpaid bills at night" + STY,
     'mB'+sfx: f"Simple old kitchen table under a hanging light bulb, a Bible open on it, night" + STY,
     'mC'+sfx: f"A mother kneeling on a linoleum kitchen floor praying with her elbows on a chair, night" + STY,
     'mD'+sfx: f"Overhead view of a kitchen table with a court notice, bills, and a child's school photo, a mother's praying hands on them" + STY,
     'mE'+sfx: f"Five grown adult siblings standing together around their {G} at a family gathering, proud and smiling" + STY,
     'mF'+sfx: f"Portrait of a {G} smiling gently with an open Bible, kitchen background" + STY,
    })
