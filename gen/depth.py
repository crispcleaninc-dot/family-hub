# Depth maps (16-bit PNG, near = bright) for every image in out/ ; SRC=dir of images
import os, glob, numpy as np
from PIL import Image
from transformers import pipeline
pipe = pipeline('depth-estimation', model='depth-anything/Depth-Anything-V2-Small-hf')
src = os.environ.get('SRC', 'out')
for f in sorted(glob.glob(f'{src}/*.webp') + glob.glob(f'{src}/*.jpg')):
    im = Image.open(f).convert('RGB'); d = np.array(pipe(im)['predicted_depth'].squeeze(), dtype=np.float32)
    d = (d - d.min()) / max(1e-6, d.max() - d.min())
    Image.fromarray((d * 65535).astype(np.uint16)).resize(im.size, Image.BICUBIC).save('out/' + os.path.basename(f).rsplit('.', 1)[0] + '_depth.png')
    if src != 'out': im.save('out/' + os.path.basename(f))
    print('depth', f)
