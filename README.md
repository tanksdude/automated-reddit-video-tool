# Automated Reddit Video Tool

A Python program that takes text input and can generate the sentence-by-sentence reading and text-to-speech stuff that's common in Reddit reading videos.

It's not fully automated, but at least it's simple. This program is not designed to be fully automated because that allows a person to add a special flare to the video. (The videos that add practically nothing are so boring, but hey, quantity over quality for these things.)

In the future, I may make a version which can actually read from a web page to generate the images. (But that's super complicated so don't wait anxiously.)

## Getting Started

There are quite a few programs needed to properly do something like this. At the very least:

* a text-to-speech program, because that's the point of Reddit readings
* an image editor/manipulator, to turn text into an image
* a program to convert the image and audio into a video
* a video editor, to put the audio and video/images together (this part is manual)

For this project, I just used whatever free and good stuff existed. Since the source code is here, you should be able to swap out a requirement pretty easily, if you know what you're doing. I used:

* [Balabolka](http://balabolka.site/balabolka.htm) (command line version) for text-to-speech (I couldn't figure out how to make [eSpeak](https://espeak.sourceforge.net/) use Daniel UK through the command line)
* [ImageMagick](https://imagemagick.org/) for image creation (*way* easier than learning [GIMP](https://www.gimp.org/) scripting)
* [FFmpeg](https://ffmpeg.org/) for merging an image and an audio file into a video file (good luck finding good alternatives to this)
* [Kdenlive](https://kdenlive.org/en/) for video editing (why are there so few good free video editors)

### Prerequisites

* the programs listed above
* Python 3
* Windows, since I couldn't figure out how to add Daniel UK to eSpeak
    * of course, since the source code is here, it's not hard to change some things to make it work on Linux (and if you got Daniel UK working, tell me how)

### Installation

* download this repository
* install [Balabolka](http://balabolka.site/bconsole.htm) command line utility, **then place the executable in the root folder**
* install [ImageMagick](https://imagemagick.org/script/download.php) (the full thing, so it will get added to PATH and usable by a command line)
* install [FFmpeg](https://www.gyan.dev/ffmpeg/builds/), **then place the executable in the root folder**
* Linux: probably `sudo apt install espeak`, `imagemagick`, and `ffmpeg`, and change some Python code
* get a video editor

## Running

Steps:

0. install the programs listed above (or change the script as you need)
1. Obtain the comment you wish to be read aloud. Paste it into a text file.
2. Split the comment by sentences: `py -3 comment_splitter.py [comment input file] [line-by-line output name]` (run this through the command line, in case you didn't know)
3. (Optional) Manually edit the output file to adjust anything you want. For example, extra pauses when reading a comma-separated list or splitting after emojis.
4. (TODO) (Optional) Generate a test image of the full comment, so you can fix the size and stuff: `py -3 comment_test_image.py [line-by-line input file] [png file output name]`
5. Take that output and have it read aloud: `py -3 comment_to_speech.py [line-by-line input file] [mp4 file names]` (have a "$" in the mp4 name, because that's where the numbers will go)
6. Note: To edit the parameters of the final output, you will need to edit the constants at the top of `comment_to_speech.py`. The font is Verdana because that's what Reddit uses.
7. Throw the mp4 files into your favorite video editor and do what you want!
8. (Optional) There's an AutoHotkey script included with this project (`kdenlive_size_adjustment.ahk`) to speed up editing in Kdenlive, since Kdenlive scales the video and I didn't want that.

There are ways to further automate this process but that's beyond the scope of this project.

### Bonus

Want the words to be censored? No problem!

TODO: currently not an option

Want the words spoken to be slightly different than the text that appears (since sometimes the text-to-speech voices introduce pauses where most people wouldn't pause)? No problem!

`py -3 comment_to_speech.py [line-by-line speech text input file] [mp4 file names] [line-by-line image text input file]` (they need to be the same number of lines, obviously)

### Known Usability Problem

Kdenlive automatically scales clips to the project's profile settings. Although it keeps the aspect ratio, it's still not preferable.

I got around this issue by making an AutoHotkey script to drag a Transform effect and update all the values necessary. Yes, I updated the script for each comment.

Alternatively, you could scale the image so you don't even need a background, but that makes a less interesting viewing experience.

## Contributing

This is intended to be an extremely simple way to automate the worst parts of Reddit readings (line-by-line advancement), so once it's done it's done.

If you want to do something with this project, the source code is right here.

## Versioning

1.0.0 is "done," and I dunno if I'll update it after that.

## License

This project is licensed under the GNU General Public License v3.0

## Acknowledgments

* Reddit readings
* myself for making me use Python to do something more "code-y" for once
* StackOverflow
