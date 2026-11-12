"""
Prepare the portrait photo for clean ASCII conversion:
  1. Cut out the subject / use existing transparency mask
  2. Crop square around subject and composite onto white
  3. Tone stretch and enhance contrast for ASCII resolution

Output: source-prepped.png, consumed by make_ascii_svg.py.

    python scripts/prep_photo.py [input.png] [output.png]
"""
import os
import sys
import numpy as np
from PIL import Image, ImageEnhance

HERE = os.path.dirname(os.path.abspath(__file__))
INP = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "source-photo.png")
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, "..", "source-prepped.png")

img = Image.open(INP)
if img.mode == "RGBA":
    alpha = np.array(img.split()[-1])
    if (alpha < 250).any():
        ys, xs = np.where(alpha > 10)
        cx = (xs.min() + xs.max()) // 2
        head_top = ys.min()
        side = max(xs.max() - xs.min(), ys.max() - ys.min()) + 80
        cy = head_top + side // 2 - 40
        x0 = cx - side // 2
        y0 = cy - side // 2
        cropped = img.crop((x0, y0, x0 + side, y0 + side))
        bg = Image.new("RGB", (side, side), (255, 255, 255))
        bg.paste(cropped, mask=cropped.split()[-1])
        bg.save(OUT)
        print("wrote", OUT, bg.size)
        sys.exit(0)

# If already RGB or composite
gray = img.convert("L")
enhanced = ImageEnhance.Contrast(gray).enhance(1.15)
enhanced.save(OUT)
print("wrote", OUT, enhanced.size)
