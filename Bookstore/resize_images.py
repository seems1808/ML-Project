from PIL import Image
from pathlib import Path

# Path to your assets folder
assets = Path("frontend/assets")

WIDTH = 300
HEIGHT = 450

for img_path in assets.glob("*.*"):
    try:
        img = Image.open(img_path)
        img = img.resize((WIDTH, HEIGHT))
        img.save(img_path)
        print(f"Resized: {img_path.name}")
    except Exception as e:
        print(f"Skipped {img_path.name}: {e}")

print("Done!")
