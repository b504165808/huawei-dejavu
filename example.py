# -*-coding:utf-8-*-
import json
import re

from pub_utils.music_cuter.cuter import utils_cuter

import warnings
from dejavu import Dejavu
from dejavu.recognize import FileRecognizer, MicrophoneRecognizer
warnings.filterwarnings("ignore")


# load config from a JSON file (or anything outputting a python dictionary)

# 开启装饰器，先将完全mp3分割为2段，将新的两段mp3全部转成WAV


@utils_cuter
# @api_comparator
def rd_config():
	with open("dejavu.cnf.SAMPLE") as f:
		config = json.load(f)
		return config


if __name__ == '__main__':

	# create a Dejavu instance

	djv = Dejavu(rd_config())
	# mp3_to_wav
	# 更改源码后  支持直接添加MP3指纹
	# Fingerprint all the wav's in the directory we give it
	djv.fingerprint_directory(r"Q:\huawei\huawei-dejavu\new_mp3", [".mp3"], 3)
	print(u'正在识别指定音乐·······')
	song = djv.recognize(FileRecognizer, r'Q:\huawei\huawei-dejavu\mp3\Sean-Fournier--Falling-For-You.mp3')
	print(u'已经识别出指定音乐！')
	song['song_name'] = re.sub('(_new\d+)|(_new)', '', str(song['song_name']))
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
	song = recognizer.recognize_file("C:\Users\yefan\Desktop\workspace\dejavu-master\mp3\Sean-Fournier--Falling-For-You.mp3")
	print("No shortcut, we recognized: %s\n" % song)
