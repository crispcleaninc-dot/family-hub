# Mommy Is Human Too — commercial pipeline
Re-run after every app update so the commercial shows the current app:
1. Build the app test copy (Index with add-ons) and run `python3 capture.py <Index.html>` → refreshes `shots/*.png` from the real app.
2. Edit `lines4.txt` lines 10-13 if features changed (then `python3 vo5.py` for new voice lines).
3. `cp lines4.txt lines.txt; PAGE=ad4.html VO=vo5 OUT=scenes4 python3 render.py video 9 10 11 12`
4. Concat scenes4 + mix (see session notes) → upload to family-hub/mommy/art/commercial.mp4 and bump ?v= in studio-addon.
