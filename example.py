# -*-coding:utf-8-*-
import json
import os
import re

from pub_utils.music_cuter.cuter import utils_cuter

import warnings
from dejavu import Dejavu
from dejavu.recognize import FileRecognizer, MicrophoneRecognizer
warnings.filterwarnings("ignore")


# load config from a JSON file (or anything outputting a python dictionary)

# 开启装饰器，先将完全mp3分割为2段，将新的两段mp3全部转成WAV


# @utils_cuter  # 切割器
# @api_comparator # 转码器
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

	# 读取磁盘进行存储指纹 并识别
	# djv.fingerprint_directory(r"Q:\huawei\huawei-dejavu\mp3", [".mp3"], 3)
	# print(u'正在识别指定音乐·······')
	# song = djv.recognize(FileRecognizer, r'Q:\huawei\huawei-dejavu\mp3\liangzhilaohu.mp3')
	# print(u'已经识别出指定音乐！')
	# if song:
	# 	song['song_name'] = re.sub('(_new\d+)|(_new)', '', str(song['song_name']))
	# print("From file we recognized: %s\n" % song)

	# 读取麦克风获取音频进行识别
	# Or recognize audio from your microphone for `secs` seconds
	print('开始获取话筒数据流.....')
	secs = 5
	record_id = 'user_voice_0003'
	record_path = 'pub_utils/sound_recording/sound_rds'
	song = djv.recognize(MicrophoneRecognizer, record_path=record_path, record_id=record_id, seconds=secs)
	if song is None:
		print("Nothing recognized -- did you play the song out loud so your mic could hear it? :)")
		print('没有识别到录音所对应的音乐，录音信息(song_name)更新失败！')
	else:
		song['song_name'] = re.sub('(_new\d+)|(_new)', '', str(song['song_name']))
		print("From mic with %d seconds we recognized: %s\n" % (secs, song))
		print('识别到录音所对应的音乐，正在完善录音信息(song_name)....')
		os.rename(os.path.join(record_path, record_id+'.wav'), os.path.join(record_path, record_id+song['song_name']+'.wav'))
		print('录音信息更新成功！')
	print('识别程序完毕！')

	# Or use a recognizer without the shortcut, in anyway you would like
	# recognizer = FileRecognizer(djv)
	# song = recognizer.recognize_file("C:\Users\yefan\Desktop\workspace\dejavu-master\mp3\Sean-Fournier--Falling-For-You.mp3")
	# print("No shortcut, we recognized: %s\n" % song)
