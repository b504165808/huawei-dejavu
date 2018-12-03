# -*-coding:utf-8-*-

import eyed3
from pydub import AudioSegment
import os, re


def utils_cuter(func):

    def cuter_func():

        print(u'开启音乐分割器····')
        msc_path = 'Q:\huawei\huawei-dejavu\mp3'
        new_cut_msc_path = r"Q:\huawei\huawei-dejavu\new_mp3"
        new_msc_res = os.walk(new_cut_msc_path)

        try:
            lir = [li for x, km, li in new_msc_res][0]
        except IndexError:
            lir = ['']
        # 循环目录下所有文件

        for each in os.listdir(msc_path):
            filename = re.findall(r"(.*?)\.mp3", each)  # 取出.mp3后缀的文件名
            if filename:
                if filename[0]+'_new.mp3' not in lir and filename[0]+'_new2.mp3' not in lir:
                    print(filename[0])
                    filename[0] += '.mp3'
                    mp3file_path = msc_path+'\cut_here'+filename[0]
                    mp3file_path = mp3file_path.replace('cut_here', '')

                    mp3_audio_file = eyed3.load(mp3file_path)
                    mp3_duration = int(mp3_audio_file.info.time_secs)

                    print(u'此音乐时长为：{}秒'.format(mp3_duration))
                    mp3 = AudioSegment.from_mp3(mp3file_path)  # 打开mp3文件
                    where_cut = mp3_duration/2

                    # 切割前where_cut秒并覆盖保存
                    mp3[where_cut * 1000+500:].export(mp3file_path.replace('\mp3', r'\new_mp3').replace('.mp3', '_new.mp3'), format="mp3")
                    # 切割后where_cut秒并覆盖保存
                    mp3[:where_cut * 1000+500].export(mp3file_path.replace('\mp3', r'\new_mp3').replace('.mp3', '_new2.mp3'), format="mp3")

                    # # 分割音乐后删除原音乐
                    # os.system('rm -rf %s' % mp3file_path)
                else:
                    print(filename[0] + '：此音乐已经在之前已经切割过了，跳过······')
        return func()
    return cuter_func


