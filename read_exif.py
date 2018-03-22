from PIL import Image

image = Image.open("test.jpg")
exif_data = image._getexif()

if exif_data:
    print("Da")
    print(exif_data[306])

