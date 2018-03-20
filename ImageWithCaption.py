from PIL import Image, ImageFont, ImageDraw, ImageStat
import numpy as np

path_fonts = "/usr/share/fonts/TTF/"
size_font = 15
font = ImageFont.truetype(path_fonts+"DejaVuSans.ttf", size_font)
filename_image = "test.jpg"

#load image
image = Image.open(filename_image)
#create drawable canvas
canvas = ImageDraw.Draw(image)
# get size of imge
size_image = np.array(image.size)
# 3% margin
margin_image = size_image*0.03

text = "Beispiel\nText"
# text size
size_text = np.array(canvas.multiline_textsize(text, font, spacing=2))
# where to position the text
position_text = size_image - margin_image - size_text
# area under text
area_text = np.append(position_text, (size_image-size_text))

#------------------------------------------------------------------------

cropped_image = image.crop(area_text)

median = np.array(ImageStat.Stat(cropped_image).median)
color_text = "#"+str(hex(255 - int(np.average(median))))*3


#------------------------------------------------------------------------

# draw text on image
canvas.multiline_text(position_text, text, font=font, align="center", fill=color_text)
del canvas

image.save("result.jpg")


print(hex(255-int(np.average(median))))
