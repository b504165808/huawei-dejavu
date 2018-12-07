# -*-coding:utf-8-*-
import json
import os
import re

from dejavu.database_sql import SQLDatabase
# from pub_utils.music_cuter.cuter import utils_cuter

import warnings
from dejavu import Dejavu
from dejavu.recognize import FileRecognizer, MicrophoneRecognizer
from pub_utils.sound_recording.r_judger import SoundRecord

warnings.filterwarnings("ignore")


# load config from a JSON file (or anything outputting a python dictionary)

# 开启装饰器，先将完全mp3分割为2段，将新的两段mp3全部转成WAV


# @utils_cuter  # 切割器
# @api_comparator # 转码器
class DejavuRunner(object):
	def __init__(self):
		with open("dejavu.cnf.SAMPLE") as f:
			self.config = json.load(f)
			# create a Dejavu instance
			self.djv = Dejavu(self.config)

	def fingerprints_saver(self, msc_path=r"Q:\huawei\huawei-dejavu\mp3", msc_type=".mp3"):
		# 读取磁盘进行存储指纹
		print('正在存储指纹.....')
		self.djv.fingerprint_directory(msc_path, [msc_type], 3)
		print('音乐波谱指纹存储完毕！')

	def file_recognizer_func(self, what_file):
		"""
		:param what_file: 需要被识别的音乐文件路径
		:return:
		"""

		# 更改源码后  支持直接添加MP3指纹
		# Fingerprint all the wav's in the directory we give it

		print(u'正在识别指定音乐·······')
		song = self.djv.recognize(FileRecognizer, '', '', what_file,)
		print(u'已经识别出指定音乐！')

		if song:
			song['song_name'] = re.sub('(_new\d+)|(_new)', '', str(song['song_name']))
		print("From file we recognized: %s\n" % song)
		print('正在返回此段音乐的指纹.......')
		rows = SQLDatabase().return_short_hash(song_id=song['song_id'], offset=song['offset'], confidence=song['confidence'])

		for row in rows:
			print('fingerprint:', row[0])

	def sound_record_recognizer_func(self):

		# 读取麦克风获取音频进行识别
		# Or recognize audio from your microphone for `secs` seconds

		print('开始获取话筒数据流.....')
		secs = 5
		# id默认为 1  进入识别程序后根据情况更新
		id_num = 1
		record_id = 'voice_%d' % id_num
		# 基础录音路径
		record_path = 'pub_utils/sound_recording/sound_rds'
		song = self.djv.recognize(MicrophoneRecognizer, record_path=record_path, record_id=record_id, seconds=secs)

		if song is None:
			print("Nothing recognized -- did you play the song out loud so your mic could hear it? :)")
			print('没有识别到录音所对应的音乐，%s录音信息(song_name)更新程序跳过！' % (record_id + '.wav'))

		else:
			song['song_name'] = re.sub('(_new\d+)|(_new)', '', str(song['song_name']))
			print("From mic with %d seconds we recognized: %s\n" % (secs, song))
			print('识别到录音所对应的音乐，正在完善录音信息(song_name)....')
			cur_wavfile_name = [name for name in os.listdir(record_path) if '.wav' in name][-1]
			new_cur_wavfile_name = cur_wavfile_name.replace('.wav', '') + song['song_name'] + '.wav'
			os.rename(os.path.join(record_path, cur_wavfile_name), os.path.join(record_path, new_cur_wavfile_name))

		print('识别程序完毕！')

	def record_searcher(self, music_name):

		is_here = SoundRecord().recoder_read(filename=music_name)
		if is_here:
			print('对应音乐录音存在')
		else:
			print('对应音乐录音不存在')
		return is_here


# 模拟调用录音
if __name__ == '__main__':
	what_file = r'Q:\huawei\huawei-dejavu\mp3\Sean-Fournier--Falling-For-You.mp3'
	DejavuRunner().file_recognizer_func(what_file=what_file)
	DejavuRunner().sound_record_recognizer_func()
	is_here = DejavuRunner().record_searcher(music_name='Sean-Fournier--Falling-For-You')
	print(is_here)
