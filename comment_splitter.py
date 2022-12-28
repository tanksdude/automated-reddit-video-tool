import os, sys
import re
import argparse
import time

# py -3 comment_splitter.py input_comments/lorem_ipsum.txt input_splits/lorem_ipsum_speech.txt -c input_comments/censored_words_dict.txt

SPLIT_CHARS = "".join([".", ";", "!", "\\?"])
SPLIT_REGEX = "[" + SPLIT_CHARS + "]+\\S*\\s+"
CENSORED_WORDS_SPLIT_CHAR = "|" # only for parsing the censored words file

parser = argparse.ArgumentParser()
parser.add_argument("input_comment_file", help="comment to split")
parser.add_argument("-c", "--censored_words_dict", metavar="censored_words_dict", required=False, help="word replacement dictionary")
parser.add_argument("output_comment_file", help="output split comment file")

args = parser.parse_args()

#if len(sys.argv) < 3:
#	sys.exit(f"Usage: {sys.argv[0]} [input_comment.txt] [output_comment.txt] [optional_censored_word_dict.txt]")

input_file_path = args.input_comment_file
output_file_path = args.output_comment_file
censored_words_dict_path = args.censored_words_dict

start_time = time.time()

try:
	input_file = open(input_file_path, "r", encoding="utf8")
except FileNotFoundError:
	sys.exit("File \"" + input_file_path + "\" not found!")
except IsADirectoryError:
	sys.exit("\"" + input_file_path + "\" is a directory; could not read")
except PermissionError:
	sys.exit("Could not read \"" + input_file_path + "\" due to permissions granted!")
except Exception as e:
	sys.exit("Other error while reading file \"" + input_file_path + "\":", e)

file_text = input_file.read().rstrip()
input_file.close()

censored_words_file_text = None
if censored_words_dict_path != None:
	try:
		censored_words_input_file = open(censored_words_dict_path, "r", encoding="utf8")
	except FileNotFoundError:
		sys.exit("File \"" + censored_words_dict_path + "\" not found!")
	except IsADirectoryError:
		sys.exit("\"" + censored_words_dict_path + "\" is a directory; could not read")
	except PermissionError:
		sys.exit("Could not read \"" + censored_words_dict_path + "\" due to permissions granted!")
	except Exception as e:
		sys.exit("Other error while reading file \"" + censored_words_dict_path + "\":", e)

	censored_words_file_text = censored_words_input_file.read().rstrip()
	censored_words_input_file.close()

# split file text on newline (mostly to trim excess newlines)

file_lines = []

while len(file_text) > 0:
	re_match = re.search("[\n]+", file_text)
	if re_match == None:
		# not found, rest of the text gets appended
		file_lines.append(file_text)
		break
	else:
		start = re_match.span()[0]
		end = re_match.span()[1]
		#print(file_text[0:end])
		file_lines.append(file_text[0:start+1])
		file_text = file_text[end:]

# split each line on a period or whatever

file_sentences = []

for line in file_lines:
	file_sentences.append([])
	while len(line) > 0:
		re_match = re.search(SPLIT_REGEX, line)
		if re_match == None:
			# not found, rest of the text gets appended
			file_sentences[-1].append(line)
			break
		else:
			start = re_match.span()[0]
			end = re_match.span()[1]
			#print(line[0:end])
			file_sentences[-1].append(line[0:end])
			line = line[end:]

# word censoring

if censored_words_file_text != None:
	censored_words_dict = {}

	censored_words_file_lines = censored_words_file_text.split("\n")
	for line in censored_words_file_lines:
		key, val = line.split(CENSORED_WORDS_SPLIT_CHAR, 1)
		censored_words_dict[key] = val

	for line_index in range(len(file_sentences)):
		for sentence_index in range(len(file_sentences[line_index])):
			for key, val in censored_words_dict.items():
				file_sentences[line_index][sentence_index] = re.sub("\\b" + key + "\\b", val, file_sentences[line_index][sentence_index])

# write each line to the output file

output_file = open(output_file_path, "w", encoding="utf8")
for line in file_sentences:
	for sentence in line:
		output_file.write(sentence + "\n")
output_file.close()

end_time = time.time()
print("Wrote " + output_file_path + ", execution time " + str(end_time - start_time))
