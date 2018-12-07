import os
import re

# os.rename(os.path.join('Q:\huawei\huawei-dejavu\pub_utils\sound_recording\sound_rds'+'\Mr_cho', 'Mr_cho_voice_2.wav'), os.path.join('Q:\huawei\huawei-dejavu\pub_utils\sound_recording\sound_rds'+'\Mr_cho', 'Mr_cho_voice_2' + '_liangzhilaohu' +'.wav'))
user_name = 'Mr_cho'
id_num = 1
record_id = '%scut_here_voice_%s' % (user_name, id_num)
record_path = 'pub_utils/sound_recording/sound_rds'
song = {'song_name': 'liangzhilaohu'}
record_id = record_id.replace('cut_here', '')
# os.rename(os.path.join(record_path+'/'+user_name, record_id+'.wav'), os.path.join(record_path+'/'+user_name, record_id + '_' + song['song_name'] + '.wav'))
s = [name for name in os.listdir(record_path+'/'+user_name) if '.wav' in name][-1]
print(s)