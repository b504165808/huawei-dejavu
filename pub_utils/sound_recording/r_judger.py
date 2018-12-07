import os


class SoundRecord(object):

    def recoder_read(self, filename,msc_path='pub_utils/sound_recording/sound_rds'):

        print(u'开启录音搜寻器····')

        print('正在查询与'+filename+'相匹配的录音.......')
        # 循环录音存放目录下所有文件
        rd_list = [rd_name for rd_name in os.listdir(msc_path) if filename in rd_name]
        print('音乐对应的录音列表:', rd_list)
        if rd_list:

            if filename in rd_list:
                print('已经找到此录音%s' % filename)
                return True
            else:
                print('未找到此录音')
                return False
        print('录音目录下为空,未找到此录音')
        return False


