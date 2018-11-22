# -*-coding:utf-8-*-
import json
import os
import warnings

from towav.mp3_to_wav import api_comparator

warnings.filterwarnings("ignore")
from dejavu import Dejavu
from dejavu.recognize import FileRecognizer, MicrophoneRecognizer

# load config from a JSON file (or anything outputting a python dictionary)

# 开启装饰器，将mp3全部转成WAV


@api_comparator
def rd_config():
	with open("dejavu.cnf.SAMPLE") as f:
		config = json.load(f)
		return config


if __name__ == '__main__':

	# create a Dejavu instance

	djv = Dejavu(rd_config())
	# mp3_to_wav

	# Fingerprint all the wav's in the directory we give it
	djv.fingerprint_directory("C:\Users\yefan\Desktop\workspace\dejavu-master\wav", [".wav"], 3)
	print('正在识别出指定音乐·······')
	song = djv.recognize(FileRecognizer, 'C:\Users\yefan\Desktop\workspace\dejavu-master\wav\Sean-Fournier--Falling-For-You.wav')
	print('已经识别出指定音乐！')
	print("From file we recognized: %s\n" % song)

	# Or recognize audio from your microphone for `secs` seconds
	secs = 5
	song = djv.recognize(MicrophoneRecognizer, seconds=secs)
	if song is None:
		print("Nothing recognized -- did you play the song out loud so your mic could hear it? :)")
	else:
		print("From mic with %d seconds we recognized: %s\n" % (secs, song))

	# Or use a recognizer without the shortcut, in anyway you would like
	recognizer = FileRecognizer(djv)
	song = recognizer.recognize_file("C:\Users\yefan\Desktop\workspace\dejavu-master\mp3\Josh-Woodward--I-Want-To-Destroy-Something-Beautiful.mp3")
	print("No shortcut, we recognized: %s\n" % song)
