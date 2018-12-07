import os
import wave

import dejavu.fingerprint as fingerprint
import dejavu.decoder as decoder
import numpy as np
import pyaudio
import time


class BaseRecognizer(object):
    # 基础识别器，在所有识别器中数据汇总返回的地方
    def __init__(self, dejavu):
        self.dejavu = dejavu
        self.Fs = fingerprint.DEFAULT_FS

    def _recognize(self, *data, record_path='', record_id=''):
        """

        :param data: 录音np16 格式数据流
        :param record_path: 录音目录
        :param record_id: 录音id
        :return:
        """
        # 在此源码中增加了录音存储功能
        if record_path:

            print('开始存储录音......')
            username = record_id[:record_id.find('cut_here')]

            print('正在查看'+username+'用户的录音量')
            user_voice_path = record_path + '/' + username
            try:

                voice_num = len(os.listdir(record_path+'/'+username))
                print('用户当前录音数量为：%d' % voice_num)
                record_id = record_id[:record_id.rfind('_')]+'_'+str(voice_num+1)
                print('更新id_num为%d' % int(voice_num+1))

            except WindowsError:
                print('当前不存在此用户之前使用记录，正在新建用户目录.....')
                os.makedirs(user_voice_path)
                print('用户目录新建成功，正在存储录音.....')
            record_id = record_id.replace('cut_here', '')
            sf = wave.open('%s/%s.wav' % (user_voice_path, record_id), 'wb')
            sf.setnchannels(1)
            sf.setsampwidth(2)
            sf.setframerate(44100)
            sf.writeframes(np.array(data).tostring())
            sf.close()
            print('录音存储完毕！')
        matches = []
        for d in data:

            matches.extend(self.dejavu.find_matches(d, Fs=self.Fs))
        return self.dejavu.align_matches(matches)

    def recognize(self):
        pass  # base class does nothing


class FileRecognizer(BaseRecognizer):
    # 文件识别器，读取磁盘音乐进行识别的地方
    def __init__(self, dejavu, record_path='', record_id=''):
        super(FileRecognizer, self).__init__(dejavu)

    def recognize_file(self, filename):
        print(filename)
        frames, self.Fs, file_hash = decoder.read(filename, self.dejavu.limit)
        print(file_hash)
        t = time.time()
        match = self._recognize(*frames)
        t = time.time() - t

        if match:
            match['match_time'] = t

        return match

    def recognize(self, filename,):
        return self.recognize_file(filename)


class MicrophoneRecognizer(BaseRecognizer):
    # 麦克风识别器，读取麦克风数据的地方
    default_chunksize   = 8192
    default_format      = pyaudio.paInt16
    default_channels    = 2
    default_samplerate  = 44100

    def __init__(self, dejavu, record_path='', record_id=''):
        self.record_path = record_path
        self.record_id = record_id
        super(MicrophoneRecognizer, self).__init__(dejavu)
        self.audio = pyaudio.PyAudio()
        self.stream = None
        self.data = []
        # 声道
        self.channels = MicrophoneRecognizer.default_channels
        # 块大小
        self.chunksize = MicrophoneRecognizer.default_chunksize
        # 采样率
        self.samplerate = MicrophoneRecognizer.default_samplerate
        self.recorded = False

    def start_recording(self, channels=default_channels,
                        samplerate=default_samplerate,
                        chunksize=default_chunksize):
        self.chunksize = chunksize
        self.channels = channels
        self.recorded = False
        self.samplerate = samplerate

        if self.stream:
            self.stream.stop_stream()
            self.stream.close()

        self.stream = self.audio.open(
            format=self.default_format,
            channels=channels,
            rate=samplerate,
            input=True,
            frames_per_buffer=chunksize,
        )

        self.data = [[] for i in range(channels)]

    def process_recording(self):
        # 录音开始
        data = self.stream.read(self.chunksize)
        # 将录音data转成int16 并转为字符串
        nums = np.fromstring(data, np.int16)

        for c in range(self.channels):
            self.data[c].extend(nums[c::self.channels])

    def stop_recording(self):
        # 录音结束
        self.stream.stop_stream()
        self.stream.close()
        self.stream = None
        self.recorded = True

    def recognize_recording(self):
        # 录音识别
        if not self.recorded:
            raise NoRecordingError("Recording was not complete/begun")

        return self._recognize(*self.data, record_path=self.record_path,record_id=self.record_id)

    def get_recorded_time(self):
        return len(self.data[0]) / self.rate

    def recognize(self, seconds=10):
        self.start_recording()
        for i in range(0, int(self.samplerate / self.chunksize
                              * seconds)):
            self.process_recording()
        self.stop_recording()
        return self.recognize_recording()


class NoRecordingError(Exception):
    pass
