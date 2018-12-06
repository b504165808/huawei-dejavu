import os


class SoundRecord(object):

    def recoder_read(self, filename, file_path='Q:\huawei\huawei-dejavu\pub_utils\sound_recording\sound_rds'):

        print(u'开启录音搜寻器····')
        msc_path = file_path

        # 循环录音存放目录下所有文件
        rd_list = os.listdir(msc_path)
        if rd_list:

            if filename in rd_list:
                print('已经找到此录音')
                return True
            else:
                print('未找到此录音')
                return False
        print('录音目录下为空,未找到此录音')
        return False


if __name__ == '__main__':

    SoundRecord().recoder_read('user_voice_0001.wav')