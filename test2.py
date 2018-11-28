import re

songname = 'Sean-Fournier--Falling-For-You_new'
songname = re.sub('(_new\d+)|(_new)', '', songname)
print songname

song = {'song_id': 2, 'song_name': 'Choc--Eigenvalue-Subspace-Decomposition_new2', 'file_sha1': '7E240F94E715BE2F3403E0E836F44D76F34CAFDD', 'confidence': 4, 'offset_seconds': 18.99392, 'match_time': 45.04700016975403, 'offset': 409}
song['song_name'] = re.sub('(_new\d+)|(_new)', '', str(song['song_name']))
print("From file we recognized: %s\n" % song)