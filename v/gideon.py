# Cinematic Bible Short (vertical) — Gideon, Judges 6–7 (KJV quotes word for word).
# N = Ciarne's storyteller voice copy; character lines in period-accented English (edge voices tested by ASR).
L = [
 ('n01', 'N', 'b01', "Three hundred men. Against an army so big, the Bible says their camels were without number."),
 ('n02', 'N', 'b02', "And God looked at Gideon's army... and said it was still too many."),
 ('t0', 'T', 'TITLE', 2.2),
 ('n03', 'N', 'b03', "For seven years, Midian stripped Israel bare. They came like locusts, ate every harvest, and left God's people hiding in caves."),
 ('n04', 'N', 'b04', "One young man was threshing wheat down in a winepress, hiding it from the enemy. His name was Gideon."),
 ('a01', 'A', 'b05', "The Lord is with thee, thou mighty man of valour."),
 ('g01', 'G', 'b05', "If the Lord be with us, why then is all this befallen us?"),
 ('n05', 'N', 'b06', "Gideon was the least in his father's house, from the poorest family in Manasseh. But God doesn't call the ready. He readies the called."),
 ('n06', 'N', 'b07', "Thirty-two thousand men answered the trumpet. And the Lord said: the people that are with thee are too many."),
 ('n07', 'N', 'b08', "Twenty-two thousand went home afraid. Ten thousand remained. Still... too many."),
 ('n08', 'N', 'b08', "At the water, God watched how they drank. Three hundred lapped from their hands, eyes on the horizon. Those were the ones."),
 ('n09', 'N', 'b09', "That night, Gideon crept to the edge of the enemy camp. And he heard a soldier telling his dream."),
 ('s01', 'S', 'b10', "I dreamed a cake of barley bread tumbled into the host of Midian. It struck the tent, and the tent lay flat."),
 ('s02', 'R', 'b10', "This is nothing else save the sword of Gideon. Into his hand hath God delivered Midian."),
 ('n10', 'N', 'b11', "Gideon bowed down and worshipped. Then he ran back, and gave every man a trumpet, an empty jar, and a torch hidden inside."),
 ('n11', 'N', 'b12', "In the middle of the night, three hundred jars shattered at once. Three hundred torches blazed in the dark."),
 ('g02', 'G', 'b12', "The sword of the Lord, and of Gideon!"),
 ('n12', 'N', 'b13', "The enemy woke in terror, turned their swords on each other, and fled into the night."),
 ('n13', 'N', 'b14', "Three hundred men. No plan anyone would choose. Just obedience."),
 ('n14', 'N', 'b14', "So what is God asking you to let go of, so that when the victory comes, everyone knows it was Him? Tell me in the comments. And follow for more stories from the Book."),
]
TITLE = {"en": ("GIDEON", "300 AGAINST AN ARMY")}
# candidate accented voices to test (English text read by these voices)
CAND = {
 'G': ['he-IL-AvriNeural', 'ar-SA-HamedNeural', 'en-US-AndrewMultilingualNeural'],
 'A': ['ar-EG-ShakirNeural', 'he-IL-AvriNeural', 'en-US-BrianMultilingualNeural'],
 'S': ['ar-EG-ShakirNeural', 'fa-IR-FaridNeural', 'ar-SA-HamedNeural'],
 'R': ['ar-SA-HamedNeural', 'ar-JO-TaimNeural', 'fa-IR-FaridNeural'],
}
G = "young Israelite man Gideon, about 25, olive-brown skin, dark curly hair and short beard, rough wool tunic"
STY = ", ancient Israel around 1200 BC, epic biblical film still, cinematic golden-hour light, dust in the air, photorealistic, highly detailed, vertical composition, no text"
SHOTS = {
 'b01': "A vast ancient Midianite army camp filling an entire valley at dusk, thousands of tents and countless camels, campfires" + STY,
 'b02': f"Small group of Israelite warriors on a hilltop looking down at a huge enemy valley camp, {G} in front" + STY,
 'b03': "Midianite raiders on camels trampling Israelite wheat fields, frightened villagers fleeing to cliff caves" + STY,
 'b04': f"{G} secretly threshing wheat inside a stone winepress, looking over his shoulder in fear" + STY,
 'b05': f"A radiant angelic figure in white robes sitting under an oak tree, {G} startled in the winepress, soft holy light" + STY,
 'b06': f"Close portrait of {G}, humble and doubtful, poor family home behind him" + STY,
 'b07': "Thousands of Israelite men gathering on a hillside as a ram's horn shofar is blown at sunrise" + STY,
 'b08': "Israelite soldiers at a stream, a few kneeling and lapping water from cupped hands while watching the horizon" + STY,
 'b09': f"Night, {G} and his servant crouching in darkness at the edge of a huge enemy camp, moonlight and campfires" + STY,
 'b10': "Night, two Midianite soldiers in robes and head wraps by a campfire inside a tent, one telling a dream with fearful eyes" + STY,
 'b11': f"{G} handing out ram's horn trumpets, clay jars and torches to his men at night, determined faces" + STY,
 'b12': f"Night, three hundred Israelite men on a ridge breaking clay jars, torches blazing, shofars raised, {G} shouting" + STY,
 'b13': "Night chaos in the Midianite camp, soldiers fleeing in panic, tents and torches, dust" + STY,
 'b14': f"Dawn, {G} standing on a hill with a small band of men, sunrise behind them, peaceful and victorious" + STY,
}
