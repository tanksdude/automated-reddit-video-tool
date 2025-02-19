import os, sys
import subprocess
import argparse
import time

# python comment_to_speech.py input_splits/lorem_ipsum_text.txt output_speech/lorem_ipsum_$.mp4 -s input_splits/lorem_ipsum_speech.txt

# Image parameters:
IMAGE_WIDTH = 960 - 2*32
IMAGE_HEIGHT = 640 - 2*32
IMAGE_W_BORDER = 32
IMAGE_H_BORDER = 32
IMAGE_FONT_SIZE = "20"
IMAGE_NEW_PARAGRAPH_SEP = "\n\n"
IMAGE_BACKGROUND_COLOR = "black"
IMAGE_TEXT_COLOR = "white"
# evaluated image parameters:
IMAGE_SIZE = str(IMAGE_WIDTH) + "x" + str(IMAGE_HEIGHT)
IMAGE_SIZE_EXTENDED = str(IMAGE_WIDTH + 2*IMAGE_W_BORDER) + "x" + str(IMAGE_HEIGHT + 2*IMAGE_H_BORDER)

# Video parameters:
VIDEO_FPS = "60"
VIDEO_VID_CRF = "18" # using constant rate factor is more efficient than forcing a constant bitrate; range is 0-51 for H.264 ("sane" range is 18-28), where 0 is lossless, ~18 is visually lossless, and 51 is very lossy
VIDEO_AUD_BITRATE = "256k"
VIDEO_VID_CODEC = "libx264"
VIDEO_AUD_CODEC = "copy" # "copy" doesn't re-encode, which apparently works for wav; "aac" for AAC, "libopus" for Opus ("opus" is experimental, don't use it)
# video size controlled by the image size

def text_to_speech_func(wav_file_name, text_file_name):
	# make sure to do -w arg before the -f arg, because sometimes it just won't write to a wav file otherwise
	return subprocess.run(["balcon", "-n", "ScanSoft Daniel_Full_22kHz", "-enc", "utf8", "-w", wav_file_name, "-f", text_file_name])
	# Linux espeak: subprocess.run(["espeak", "-v", "english+f4", "-w", wav_file_name, "-f", text_file_name])

def text_to_image_func(img_file_name, text_file_name, img_size, font_size, back_color, text_color, img_extended_size):
	#return subprocess.run(["magick", "-size", img_size, "-background", back_color, "-fill", text_color, "-family", "Times New Roman", "-pointsize", font_size, "pango:@" + text_file_name, "-gravity", "center", "-extent", img_extended_size, img_file_name])
	return subprocess.run(["magick", "-size", img_size, "-background", back_color, "-fill", text_color, "-font", "Verdana", "-pointsize", font_size, "pango:@" + text_file_name, "-gravity", "center", "-extent", img_extended_size, img_file_name])
	# https://imagemagick.org/Usage/text/#caption

def speech_and_image_to_vid_func(vid_file_name, wav_file_name, img_file_name, framerate, vid_crf, aud_bitrate):
	return subprocess.run(["ffmpeg", "-i", wav_file_name, "-i", img_file_name, "-c:v", VIDEO_VID_CODEC, "-c:a", VIDEO_AUD_CODEC, "-r", framerate, "-crf", vid_crf, "-b:a", aud_bitrate, "-loglevel", "error", "-y", vid_file_name])
	# loglevels: quiet, fatal, error, warning
	# https://ffmpeg.org/ffmpeg.html#Main-options

parser = argparse.ArgumentParser()
parser.add_argument("input_text_file", help="text to show on screen")
parser.add_argument("-s", "--input_speech_file", metavar="input_speech_file", required=False, help="text to read aloud")
parser.add_argument("output_mp4_files", help="output video files (needs a '$' in its name)")
parser.add_argument("-n", "--video_number", metavar="video_number", required=False, help="update/generate a specific video", type=int) #maybe try action="extend"
parser.add_argument("-a", "--audio_only", required=False, help="only output audio files, no video", action="store_true")

args = parser.parse_args()

input_image_text_file_path = args.input_text_file
output_vid_file_path = args.output_mp4_files
if output_vid_file_path.find('$') == -1:
	sys.exit("Bad output vid file names")
input_speech_text_file_path = args.input_speech_file
replace_video_number = args.video_number
audio_only = args.audio_only

def gen_output_vid_file_path(num):
	return output_vid_file_path.replace("$", str(num))

def gen_output_wav_file_path(num):
	return gen_output_vid_file_path(num) + ".wav"

def gen_output_img_file_path(num):
	return gen_output_vid_file_path(num) + ".png"

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
	sys.exit("Other error while reading file \"" + input_image_text_file_path + "\": ", e)

image_text_file_lines = input_image_text_file.readlines()
input_image_text_file.close()

speech_text_file_lines = None
if input_speech_text_file_path != None:
	try:
		input_speech_text_file = open(input_speech_text_file_path, "r", encoding="utf8")
	except FileNotFoundError:
		sys.exit("File \"" + input_speech_text_file_path + "\" not found!")
	except IsADirectoryError:
		sys.exit("\"" + input_speech_text_file_path + "\" is a directory; could not read")
	except PermissionError:
		sys.exit("Could not read \"" + input_speech_text_file_path + "\" due to permissions granted!")
	except Exception as e:
		sys.exit("Other error while reading file \"" + input_speech_text_file_path + "\":", e)

	speech_text_file_lines = input_speech_text_file.readlines()
	input_speech_text_file.close()
else:
	speech_text_file_lines = image_text_file_lines

if len(image_text_file_lines) != len(speech_text_file_lines):
	sys.exit("Lines in image text file and speech text file don't match")

files_count = 0 # for the vid_$.mp4 file; the file number won't match the line number
curr_text_file_read = ""

for i in range(len(image_text_file_lines)):
	speech_line = speech_text_file_lines[i]
	image_line = image_text_file_lines[i]
	speech_line = speech_line[0:-1] # every line should end in a \n
	image_line = image_line[0:-1]
	if len(speech_line) == 0:
		curr_text_file_read += IMAGE_NEW_PARAGRAPH_SEP
		continue
	curr_text_file_read += image_line

	files_count += 1

	if (replace_video_number == None) or (replace_video_number == files_count):
		# speech file:
		output_file = open(gen_output_wav_file_path(files_count)+".temp", "w", encoding="utf8")
		output_file.write(speech_line)
		output_file.close()

		result = text_to_speech_func(gen_output_wav_file_path(files_count), gen_output_wav_file_path(files_count)+".temp")
		os.remove(gen_output_wav_file_path(files_count)+".temp")

		if not audio_only:
			# image file:
			output_file = open(gen_output_img_file_path(files_count)+".temp", "w", encoding="utf8")
			output_file.write(curr_text_file_read)
			output_file.close()

			result = text_to_image_func(gen_output_img_file_path(files_count), gen_output_img_file_path(files_count)+".temp", IMAGE_SIZE, IMAGE_FONT_SIZE, IMAGE_BACKGROUND_COLOR, IMAGE_TEXT_COLOR, IMAGE_SIZE_EXTENDED)
			os.remove(gen_output_img_file_path(files_count)+".temp")

			# video:
			result = speech_and_image_to_vid_func(gen_output_vid_file_path(files_count), gen_output_wav_file_path(files_count), gen_output_img_file_path(files_count), VIDEO_FPS, VIDEO_VID_CRF, VIDEO_AUD_BITRATE)

			# cleanup:
			os.remove(gen_output_wav_file_path(files_count))
			os.remove(gen_output_img_file_path(files_count))

		# break early if only one video is being updated:
		if (replace_video_number != None):
			break

end_time = time.time()
if replace_video_number == None:
	print("Made " + str(files_count) + " videos in " + str(end_time - start_time) + "s")
else:
	print("Replaced video " + str(replace_video_number) + " in " + str(end_time - start_time) + "s")
