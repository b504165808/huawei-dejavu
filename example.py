# -*-coding:utf-8-*-
import json
import os
import re

from dejavu.database_sql import SQLDatabase
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


def main_runer(user_name):

	# create a Dejavu instance
	djv = Dejavu(rd_config())
	# mp3_to_wav
	# 更改源码后  支持直接添加MP3指纹
	# Fingerprint all the wav's in the directory we give it

	# 读取磁盘进行存储指纹 并识别
	print('正在存储指纹.....')
	djv.fingerprint_directory(r"Q:\huawei\huawei-dejavu\mp3", [".mp3"], 3)
	print('音乐波谱指纹存储完毕！')
	print(u'正在识别指定音乐·······')
	song = djv.recognize(FileRecognizer, '', '', r'Q:\huawei\huawei-dejavu\new_mp3\Sean-Fournier--Falling-For-You-short1.mp3',)
	print(u'已经识别出指定音乐！')

	if song:
		song['song_name'] = re.sub('(_new\d+)|(_new)', '', str(song['song_name']))
	print("From file we recognized: %s\n" % song)
	print('正在返回此段音乐的指纹.......')
	rows = SQLDatabase().return_short_hash(song_id=song['song_id'], offset=song['offset'], confidence=song['confidence'])
	for row in rows:
		print('fingerprint:', row)
	# 读取麦克风获取音频进行识别
	# Or recognize audio from your microphone for `secs` seconds

	# print('开始获取话筒数据流.....')
	# secs = 5
	# # id默认为 1  进入识别程序后根据情况更新
	# id_num = 1
	# record_id = '%scut_here_voice_%s' % (user_name, id_num)
	# record_path = 'pub_utils/sound_recording/sound_rds'
	# song = djv.recognize(MicrophoneRecognizer, record_path=record_path, record_id=record_id, seconds=secs)
	# record_id = record_id.replace('cut_here', '')
	# print(record_path, record_id + '.wav')
	# if song is None:
	# 	print("Nothing recognized -- did you play the song out loud so your mic could hear it? :)")
	# 	print('没有识别到录音所对应的音乐，%s录音信息(song_name)更新程序跳过！' % (record_id + '.wav'))
	# else:
	# 	song['song_name'] = re.sub('(_new\d+)|(_new)', '', str(song['song_name']))
	# 	print("From mic with %d seconds we recognized: %s\n" % (secs, song))
	# 	print('识别到录音所对应的音乐，正在完善录音信息(song_name)....')
	# 	cur_path = record_path + '/' + user_name
	# 	cur_wavfile_name = [name for name in os.listdir(cur_path) if '.wav' in name][-1]
	# 	new_cur_wavfile_name = cur_wavfile_name.replace('.wav', '') + song['song_name'] + '.wav'
	#
	# 	os.rename(os.path.join(cur_path, cur_wavfile_name), os.path.join(cur_path, new_cur_wavfile_name))
	# 	print(new_cur_wavfile_name+'录音信息更新成功！')
	# print('识别程序完毕！')

	# Or use a recognizer without the shortcut, in anyway you would like
	# recognizer = FileRecognizer(djv)
	# song = recognizer.recognize_file("C:\Users\yefan\Desktop\workspace\dejavu-master\mp3\Sean-Fournier--Falling-For-You.mp3")
	# print("No shortcut, we recognized: %s\n" % song)


# 模拟调用录音
if __name__ == '__main__':
	main_runer('Mr_cho')
