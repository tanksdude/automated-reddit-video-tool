import os, sys
import subprocess
import argparse
import time

# py -3 comment_to_speech.py input_splits/lorem_ipsum_speech.txt speech_outputs/lorem_ipsum_$.mp4 -t input_splits/lorem_ipsum_image.txt

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

# Video parameters:
VIDEO_FPS = "60"
VIDEO_VID_BITRATE = "10M"
VIDEO_AUD_BITRATE = "256k"
VIDEO_VID_CODEC = "libx264" # libaom-av1 for AV1
VIDEO_AUD_CODEC = "aac" # doesn't everything nowadays use AAC?
# video size controlled by the image size

def text_to_speech_func(wav_file_name, text_file_name):
	# make sure to do -w arg before the -f arg, because sometimes it just won't write to a wav file otherwise
	return subprocess.run(["balcon.exe", "-n", "ScanSoft Daniel_Full_22kHz", "-enc", "utf8", "-w", wav_file_name, "-f", text_file_name])
	# Linux espeak: subprocess.run(["espeak", "-v", "english+f4", "-w", wav_file_name, "-f", text_file_name])

def text_to_image_func(img_file_name, text_file_name, img_size, font_size, back_color, text_color, img_extended_size):
	#return subprocess.run(["magick", "-size", img_size, "-background", back_color, "-fill", text_color, "-family", "Times New Roman", "-pointsize", font_size, "pango:@" + text_file_name, "-gravity", "center", "-extent", img_extended_size, img_file_name])
	return subprocess.run(["magick", "-size", img_size, "-background", back_color, "-fill", text_color, "-font", "Verdana", "-pointsize", font_size, "pango:@" + text_file_name, "-gravity", "center", "-extent", img_extended_size, img_file_name])
	# https://imagemagick.org/Usage/text/#caption

def speech_and_image_to_vid_func(vid_file_name, wav_file_name, img_file_name, framerate, vid_bitrate, aud_bitrate):
	return subprocess.run(["ffmpeg.exe", "-i", wav_file_name, "-i", img_file_name, "-c:v", VIDEO_VID_CODEC, "-c:a", VIDEO_AUD_CODEC, "-r", framerate, "-b:v", vid_bitrate, "-b:a", aud_bitrate, "-loglevel", "error", "-y", vid_file_name])
	# loglevels: quiet, fatal, error, warning
	# https://ffmpeg.org/ffmpeg.html#Main-options

parser = argparse.ArgumentParser()
parser.add_argument("input_speech_file", help="text to read aloud")
parser.add_argument("-t", "--input_text_file", metavar="input_text_file", required=False, help="text to show on screen")
parser.add_argument("output_mp4_files", help="output video files (needs a '$' in its name)")

args = parser.parse_args()

#if len(sys.argv) < 3:
#	sys.exit(f"Usage: {sys.argv[0]} [input_comment.txt] [output_vid_$.mp4] [optional_image_text.txt]")

input_speech_text_file_path = args.input_speech_file
output_vid_file_path = args.output_mp4_files
if output_vid_file_path.find('$') == -1:
	sys.exit("Bad output vid file names")
input_image_text_file_path = args.input_text_file

start_time = time.time()

def gen_output_vid_file_path(num):
	return output_vid_file_path.replace("$", str(num))

def gen_output_wav_file_path(num):
	return gen_output_vid_file_path(num) + ".wav"

def gen_output_img_file_path(num):
	return gen_output_vid_file_path(num) + ".png"

try:
	input_speech_text_file = open(input_speech_text_file_path, "r", encoding="utf8")
except FileNotFoundError:
	sys.exit("File \"" + input_speech_text_file_path + "\" not found!")
except IsADirectoryError:
	sys.exit("\"" + input_speech_text_file_path + "\" is a directory; could not read")
except PermissionError:
	sys.exit("Could not read \"" + input_speech_text_file_path + "\" due to permissions granted!")
except Exception as e:
	sys.exit("Other error while reading file \"" + input_speech_text_file_path + "\": ", e)

speech_text_file_lines = input_speech_text_file.readlines()
input_speech_text_file.close()

image_text_file_lines = ""
if input_image_text_file_path != None:
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
else:
	image_text_file_lines = speech_text_file_lines

# split the sentences into their own files, then convert it to text-to-speech:

files_count = 0
curr_file_read = ""

for line in speech_text_file_lines:
	line = line[0:-1] # every line should end in a \n
	#print(line, end="")
	if len(line) == 0:
		continue

	files_count += 1
	output_file = open(gen_output_wav_file_path(files_count)+".temp", "w", encoding="utf8")
	output_file.write(line)
	output_file.close()

	result = text_to_speech_func(gen_output_wav_file_path(files_count), gen_output_wav_file_path(files_count)+".temp")
	#print(result)
	os.remove(gen_output_wav_file_path(files_count)+".temp")

print("Made " + str(files_count) + " audio files")

# split the sentences into their own files, append them, then convert it to an image:

files_count = 0
curr_file_read = ""

for line in image_text_file_lines:
	line = line[0:-1] # every line should end in a \n
	#print(line, end="")
	if len(line) == 0:
		curr_file_read += "\n\n"
		continue

	files_count += 1
	curr_file_read += line
	output_file = open(gen_output_img_file_path(files_count)+".temp", "w", encoding="utf8")
	output_file.write(curr_file_read)
	output_file.close()

	result = text_to_image_func(gen_output_img_file_path(files_count), gen_output_img_file_path(files_count)+".temp", IMAGE_SIZE, IMAGE_FONT_SIZE, IMAGE_BACKGROUND_COLOR, IMAGE_TEXT_COLOR, IMAGE_SIZE_EXTENDED)
	#print(result)
	os.remove(gen_output_img_file_path(files_count)+".temp")

print("Made " + str(files_count) + " images")

# merge the audio files and images into a video

for i in range(1, files_count+1):
	result = speech_and_image_to_vid_func(gen_output_vid_file_path(i), gen_output_wav_file_path(i), gen_output_img_file_path(i), VIDEO_FPS, VIDEO_VID_BITRATE, VIDEO_VID_BITRATE)
	#print(result)

print("Made " + str(files_count) + " videos")

# remove unnecessary audio files and images

for i in range(1, files_count+1):
	os.remove(gen_output_wav_file_path(i))
	os.remove(gen_output_img_file_path(i))

print("Deleted " + str(files_count) + " audio files and " + str(files_count) + " images")

end_time = time.time()
print("Executed in " + str(end_time - start_time) + "s")
