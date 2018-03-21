import fileinput
from PIL import Image, ImageDraw, ImageFont
import numpy
#from PIL.ĒKifTags import TAGS

def add_caption(input_file, caption, output_file="result.jpg"):
# open original
    image = Image.open(input_file)
# rotate 90 deg counterclockwise
    image = image.rotate(90, expand=True)
# get size of picture
    size_image = numpy.array(image.size)

    path_fonts = "/usr/share/fonts/TTF/"
    size_font = int(size_image[1]*0.01)
    font = ImageFont.truetype(path_fonts+"DejaVuSans.ttf", size_font)
# get size of text
    size_text = numpy.array(font.getsize(caption))

#----------
    margin = int(size_text[1]*0.3)
#gnügend Platz für den text
    size_blank_image = (size_image[0], size_image[1] + size_text[1] + margin*2)
# new blank image
    blank_image = Image.new('RGB', size_blank_image, color="#000000")

    canvas = ImageDraw.Draw(blank_image)
# text einfügen
    canvas.text((0 + margin*5, 0 + margin), caption, font=font, fill="#ffffff")
#original bild einfügen
    blank_image.paste(image, (0, 0 + size_text[1] + margin*2))
# zurück rotieren
    blank_image = blank_image.rotate(-90, expand=True)
    blank_image.save(output_file)

if __name__ ==  "__main__":
#input_file = "test, png"
    output = "_result"
    counter = 0
    with fileinput.input() as f_input:
        for line in f_input:
            outname = line.split('.')[0] + output + ".jpg"
            add_caption(line.rstrip(), caption="Hallo", output_file=outname)
            counter =+ 1

# TODO: EXIF auslesen und Datum Uhrzeit einfagen, Dateinaine einfügen
