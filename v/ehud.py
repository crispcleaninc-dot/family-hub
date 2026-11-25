# The Left-Handed, Ep. 1 — Ehud (Judges 3:12-30, KJV quotes word for word).
# N = Ciarne's storyteller voice copy (Gideon cadence); characters in period-accented English (edge voices, ASR-checked).
L = [
 ('n01', 'N', 'c01', "Everybody watched his right hand. Nobody watched his left."),
 ('n02', 'N', 'c02', "He came from Benjamin, the tribe whose very name means son of the right hand. And God chose the man who was left-handed."),
 ('t0', 'T', 'TITLE', 2.2),
 ('n03', 'N', 'c03', "The children of Israel did evil again in the sight of the Lord. And for eighteen years, Eglon the king of Moab ruled over them."),
 ('n04', 'N', 'c04', "Every year they carried a heavy tribute to his palace. And Eglon, the Bible says, was a very fat man."),
 ('n05', 'N', 'c03', "And when the children of Israel cried unto the Lord, the Lord raised them up a deliverer."),
 ('n06', 'N', 'c05', "Ehud the son of Gera, a Benjamite, a man lefthanded."),
 ('n07', 'N', 'c06', "Ehud made him a dagger which had two edges, of a cubit length. And he did gird it under his raiment upon his right thigh."),
 ('n08', 'N', 'c07', "The guards searched the left side, where a right-handed man carries his blade. They never checked the right."),
 ('n09', 'N', 'c08', "When the tribute was paid, Ehud sent the people home. Then he turned back. Alone."),
 ('e01', 'E', 'c08', "I have a secret errand unto thee, O king."),
 ('k01', 'K', 'c09', "Keep silence."),
 ('n10', 'N', 'c09', "And all that stood by him went out from him. The king sat alone in his cool summer parlour."),
 ('e02', 'E', 'c08', "I have a message from God unto thee."),
 ('n11', 'N', 'c01', "Eglon rose up out of his seat. And Ehud put forth his left hand. That day, God's judgment fell on the king of Moab."),
 ('n12', 'N', 'c10', "Ehud shut the doors of the parlour upon him, and locked them, and slipped away through the porch."),
 ('s01', 'S', 'c09', "Surely he covereth his feet in his summer chamber."),
 ('n13', 'N', 'c02', "So they waited... till they were ashamed. And by the time they opened those doors, Ehud was long gone."),
 ('n14', 'N', 'c12', "He blew a trumpet in the mountain of Ephraim."),
 ('e03', 'E', 'c12', "Follow after me: for the Lord hath delivered your enemies the Moabites into your hand."),
 ('n15', 'N', 'c13', "So Moab was subdued that day under the hand of Israel. And the land had rest fourscore years."),
 ('n16', 'N', 'c14', "Eighty years of peace. Started by the hand everybody overlooked."),
 ('n17', 'N', 'c14', "What is the thing about you that people called strange, that God might be ready to use? Tell me in the comments. And follow The Left-Handed, a new story every week."),
]
TITLE = {"en": ("EHUD", "THE LEFT-HANDED DELIVERER")}
CAND = {
 'E': ['he-IL-AvriNeural', 'ar-JO-TaimNeural', 'en-US-AndrewMultilingualNeural'],
 'K': ['ar-EG-ShakirNeural', 'ar-SA-HamedNeural', 'fa-IR-FaridNeural'],
 'S': ['fa-IR-FaridNeural', 'ar-SA-HamedNeural', 'ar-JO-TaimNeural'],
}
E = "Ehud, a lean Israelite man about 35, olive-brown skin, short dark beard, plain brown hooded wool robe"
STY = (", ancient Israel and Moab around 1300 BC, epic biblical film still, dark moody cinematic lighting, mist and haze, "
       "desaturated earth tones with warm torchlight, photorealistic, highly detailed, vertical composition, no text")
SHOTS = {
 'c01': f"Extreme close-up of a man's left hand gripping the hilt of a short two-edged bronze dagger in deep shadow, {E} half visible" + STY,
 'c02': f"{E} walking alone toward the camera through a misty valley, a stone palace in the distance behind him, lone figure" + STY,
 'c03': "Weary Israelite men and women carrying heavy baskets of grain and goods as tribute, Moabite soldiers with spears watching" + STY,
 'c04': "Eglon king of Moab, an enormously heavy king on a carved throne, gold rings and crown, torchlit stone palace hall, servants around" + STY,
 'c05': f"Portrait of {E}, calm determined eyes, by firelight at night" + STY,
 'c06': f"{E} fastening a sheathed short dagger to his right thigh under his robe, by an oil lamp" + STY,
 'c07': f"Two Moabite palace guards patting down the left side of {E} at a palace gate, torches" + STY,
 'c08': f"{E} standing before the enormous seated king Eglon in a cool upper summer room, light through wooden lattice windows" + STY,
 'c09': "Palace servants bowing and walking out of a royal chamber, heavy wooden doors closing behind them" + STY,
 'c10': f"{E} quietly locking heavy wooden doors behind him and slipping out through a shadowed porch" + STY,
 'c11': "Moabite servants waiting awkwardly outside locked palace doors, one holding a large iron key, exchanging uneasy looks" + STY,
 'c12': f"{E} blowing a ram's horn shofar on a misty mountaintop at dawn, Israelite men rising from the hills behind him" + STY,
 'c13': "Israelite men charging down a hillside toward the fords of the Jordan river at dawn, dust and mist" + STY,
 'c14': f"Peaceful Israelite village at golden dawn after war, families in the fields, {E} standing among them looking out" + STY,
}
MOTION = {
 'c01': "the hand slowly tightens on the dagger hilt, shadows shift, slow push-in",
 'c02': "the man walks steadily toward camera, robe and mist drifting, slow camera pull back",
 'c03': "people trudge forward under heavy loads, guards turn their heads, dust drifts",
 'c04': "the king shifts on his throne and raises a goblet, torches flicker, servants move",
 'c05': "he breathes and slowly raises his eyes, firelight flickers on his face",
 'c06': "his hands tie the dagger strap and pull the robe over it, lamp flame flickers",
 'c07': "the guards pat his left side and wave him through, torches flicker",
 'c08': "Ehud steps forward and bows slightly, the king leans forward, light rays move through the lattice",
 'c09': "servants walk out and the heavy doors swing shut",
 'c10': "he turns the key, glances back, and slips into the shadows",
 'c11': "servants shift their weight and glance at each other, one raises the key",
 'c12': "he lifts the horn and blows it, mist swirls, men rise from the hills behind him",
 'c13': "men run down the hill, dust and mist swirl, camera tracks with them",
 'c14': "wheat sways in the breeze, families move about, sunrise grows brighter, slow crane up",
}
