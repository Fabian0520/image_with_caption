import sys
import glob
import argparse
import numpy
from PIL import Image, ImageDraw, ImageFont

def add_caption(input_file, text, output_file="result.jpg"):
    image = Image.open(input_file) # open original
    exif_data = image._getexif() # get exif data

    if exif_data: # build caption
        image_date = exif_data[306] #306 is DateTime
        # exif 274 is imagerotation
        caption = text + "   " + str(image_date)
    else:
        caption = text

    image = image.rotate(90, expand=True) # rotate 90 deg counterclockwise
    size_image = numpy.array(image.size) # get size of picture

    path_fonts = "/usr/share/fonts/TTF/"
    size_font = int(size_image[1]*0.01) # calculate optimal fontsize
    font = ImageFont.truetype(path_fonts+"DejaVuSans.ttf", size_font)

    size_text = numpy.array(font.getsize(caption)) # get size of text

    margin = int(size_text[1]*0.3)
    size_blank_image = (size_image[0], size_image[1] + size_text[1] + margin*2) #gnügend Platz für den text
    blank_image = Image.new('RGB', size_blank_image, color="#000000") # new blank image

    canvas = ImageDraw.Draw(blank_image)
    canvas.text((0 + margin*5, 0 + margin), caption, font=font, fill="#ffffff") # text einfügen
    blank_image.paste(image, (0, 0 + size_text[1] + margin*2)) #original bild einfügen
    blank_image = blank_image.rotate(-90, expand=True) # zurück rotieren
    blank_image.save(output_file, exif=image.info['exif'])

#--------------------------------------------------------------------------------

if __name__ ==  "__main__":
    input_files = []

    parser = argparse.ArgumentParser(
            epilog="It is possible to pipe the output of ls into this script.") # create Parser
    parser.add_argument('-n', metavar='experiment number', nargs='?', dest='text', required=True)
    parser.add_argument('-t', metavar='filetype', nargs='?', dest='file_type')
    parser.add_argument('input_file', nargs='*')
    args = parser.parse_args()

    if args.file_type:  # add caption to all matching extentions in folder
        input_files = glob.glob('*.'+args.file_type)
    elif args.input_file:   # add caption to specified files
        input_files = args.input_file
    elif not sys.stdin.isatty(): # pipe files into app
        for line in sys.stdin.readlines():
            input_files.append(line.rstrip())
    else:
        parser.print_help()

    for f in input_files:
        print('Added caption to file: ', f)
        output = "_result"
        outname = f.split('.')[0] + output + ".jpg"
        add_caption(f, text=args.text, output_file=outname)

