# -*-coding:utf-8-*-
import os
import stat
import sys

from pydub import AudioSegment
import wave
import io
# mp3转换器

def api_comparator(func):

    def mp3wav():

        wav_path = r"Q:\huawei\huawei-dejavu\wav"
        mp3_res = os.walk(r'Q:\huawei\huawei-dejavu\mp3')
        wav_res = os.walk(wav_path)
        try:
            lir = [li for x, km, li in wav_res][0]
        except IndexError:
            lir = ['']
        for m_pt, o, mp3_list in mp3_res:
            for cur in mp3_list:
                if '.mp3' in cur:
                    if cur.replace('.mp3', '')+'.wav' not in lir:
                        flie_path = m_pt + '\cut_here' + cur

                        fp = open(flie_path.replace('cut_here', ''), 'rb')

                        data = fp.read()
                        fp.close()
                        # 主要部分
                        aud = io.BytesIO(data)
                        sound = AudioSegment.from_file(aud, format='mp3')
                        raw_data = sound._data
                        # 写入到文件，验证结果是否正确。
                        l = len(raw_data)
                        flie_wav_path = wav_path + "\cut_here" + cur
                        flie_wav_path = flie_wav_path.replace('cut_here', '').replace('.mp3', '.wav')

                        f = wave.open(flie_wav_path, 'wb')
                        f.setnchannels(1)
                        f.setsampwidth(1)
                        f.setframerate(6000)
                        f.setnframes(l)
                        f.writeframes(raw_data)
                        f.close()
                    else:
                        print cur+'此音乐已经在之前转化过WAV格式了，跳过······'
        return func()
    return mp3wav
