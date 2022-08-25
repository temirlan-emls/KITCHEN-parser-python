from PIL import Image, ImageOps

img = Image.open(f"./Тепловые витрины/ZH-1200.R.png")
img = ImageOps.expand(img, border=(10, 70, 7, 10), fill='black')
img.save(f"a.png")
