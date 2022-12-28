import os, sys
import subprocess
import argparse
import time

# py -3 comment_test_image.py input_splits/lorem_ipsum_speech.txt input_splits/lorem_ipsum_test_image.png

# Image parameters:
IMAGE_WIDTH = 900
IMAGE_HEIGHT = 700
IMAGE_W_BORDER = 50
IMAGE_H_BORDER = 50
IMAGE_FONT_SIZE = "24"
IMAGE_BACKGROUND_COLOR = "transparent"
IMAGE_TEXT_COLOR = "white"
# evaluated image parameters:
IMAGE_SIZE = str(IMAGE_WIDTH) + "x" + str(IMAGE_HEIGHT)
IMAGE_SIZE_EXTENDED = str(IMAGE_WIDTH + 2*IMAGE_W_BORDER) + "x" + str(IMAGE_HEIGHT + 2*IMAGE_H_BORDER)

def text_to_image_func(img_file_name, text_file_name, img_size, font_size, back_color, text_color, img_extended_size):
	#return subprocess.run(["magick", "-size", img_size, "-background", back_color, "-fill", text_color, "-family", "Times New Roman", "-pointsize", font_size, "pango:@" + text_file_name, "-gravity", "center", "-extent", img_extended_size, img_file_name])
	return subprocess.run(["magick", "-size", img_size, "-background", back_color, "-fill", text_color, "-font", "Verdana", "-pointsize", font_size, "pango:@" + text_file_name, "-gravity", "center", "-extent", img_extended_size, img_file_name])
	# https://imagemagick.org/Usage/text/#caption

parser = argparse.ArgumentParser()
parser.add_argument("input_split_comment_file", help="split comment input")
parser.add_argument("output_image_file", help="output image file")

args = parser.parse_args()

#if len(sys.argv) < 3:
#	sys.exit(f"Usage: {sys.argv[0]} [line-by-line_input.txt] [output_image.png]")

input_image_text_file_path = args.input_split_comment_file
output_img_file_path = args.output_image_file

start_time = time.time()

try:
	input_image_text_file = open(input_image_text_file_path, "r", encoding="utf8")
except FileNotFoundError:
	sys.exit("File \"" + input_image_text_file_path + "\" not found!")
except IsADirectoryError:
	sys.exit("\"" + input_image_text_file_path + "\" is a directory; could not read")
except PermissionError:
	sys.exit("Could not read \"" + input_image_text_file_path + "\" due to permissions granted!")
except Exception as e:
	sys.exit("Other error while reading file \"" + input_image_text_file_path + "\":", e)

image_text_file_lines = input_image_text_file.readlines()
input_image_text_file.close()

# split the sentences into their own files, append them, then convert it to an image:

curr_file_read = ""

for line in image_text_file_lines:
	line = line[0:-1] # every line should end in a \n
	#print(line, end="")
	if len(line) == 0:
		curr_file_read += "\n\n"
		continue
	curr_file_read += line

output_file = open(output_img_file_path+".temp", "w", encoding="utf8")
output_file.write(curr_file_read)
output_file.close()

result = text_to_image_func(output_img_file_path, output_img_file_path+".temp", IMAGE_SIZE, IMAGE_FONT_SIZE, IMAGE_BACKGROUND_COLOR, IMAGE_TEXT_COLOR, IMAGE_SIZE_EXTENDED)
#print(result)
os.remove(output_img_file_path+".temp")

end_time = time.time()
print("Executed in " + str(end_time - start_time) + "s")
