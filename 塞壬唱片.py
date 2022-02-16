"""
用法
1. 确保安装 Python3
2. 安装依赖
    pip3 install requests
    pip3 install eyed3
3. Run
    python3 塞壬唱片.py
4. 等啊等啊等
"""


import requests
import os
import eyed3

# 获取专辑列表
print('正在获取专辑列表...')
req_albums = requests.get('https://monster-siren.hypergryph.com/api/albums')
sou_albums = req_albums.json().get('data')
albums = {}
for i in sou_albums:
    albums[i['cid']] = i
print('完成')

print('------')

# 建立专辑文件夹
print('正在建立专辑文件夹...')
for i in albums.values():
    print(i['name'], end=',')
    if not os.path.isdir(i['name']):
        os.mkdir(i['name'])
print()
print('完成')

print('------')

# 获取专辑封面
print('正在获取专辑封面...')
imgs = {}
for i in albums.values():
    print(i['name'], end=',')
    img_type = os.path.splitext(i['coverUrl'])[-1]
    img_path = i['name']+'/cover'+img_type
    if not os.path.isfile(img_path):
        req_img = requests.get(i['coverUrl'])
        sou_img = req_img.content
        imgs[i['cid']] = [sou_img,img_type]
        with open(img_path, 'wb') as f:
            f.write(sou_img)
            f.close()
    else:
        with open(img_path, 'rb') as f:
            sou_img = f.read()
            imgs[i['cid']] = [sou_img,img_type]
            f.close()
print()
print('完成')

print('------')

# 获取专辑介绍
print('正在获取专辑介绍...')
for i in albums.values():
    print(i['name'], end=',')
    intro_path = i['name']+'/intro.txt'
    if not os.path.isfile(intro_path):
        req_intro = requests.get(f'https://monster-siren.hypergryph.com/api/album/{i["cid"]}/data')
        sou_intro = req_intro.json().get('data')
        with open(intro_path, 'w', encoding='utf8') as f:
            f.write('艺术家:' + '/'.join(sou_intro.get('artistes'))+'\n')
            f.write('所属:' + sou_intro.get('belong')+'\n')
            f.write(sou_intro.get('intro'))
            f.close()
print()
print('完成')

print('------')

# 获取歌曲列表
print('正在获取单曲列表...')
req_songs = requests.get('https://monster-siren.hypergryph.com/api/songs')
sou_songs = req_songs.json().get('data').get('list')
songs = {}
for i in sou_songs:
    songs[i['cid']] = i
print('完成')

print('------')

# 获取歌曲
print('正在获取单曲...')
for i in songs.values():
    a = albums[i['albumCid']]
    print(f'正在获取 {a["name"]} - {i["name"]}...', end=' ')
    req_song = requests.get(f'https://monster-siren.hypergryph.com/api/song/{i["cid"]}')
    sou_song = req_song.json().get('data')
    i['name'] = i['name'].replace(':','-')
    # mp3
    global_mp3_path = None
    if sou_song['sourceUrl'] != None:
        print('mp3', end='')
        mp3_path = a["name"] + '/' + i['name'] + '.mp3'
        global_mp3_path = mp3_path
        if not os.path.isfile(mp3_path):
            req_mp3 = requests.get(sou_song['sourceUrl'])
            with open(mp3_path, 'wb') as f:
                f.write(req_mp3.content)
                f.close()
        # meta data
        audiofile = eyed3.load(mp3_path)
        audiofile.initTag()
        image_type = imgs[a['cid']][1].replace('.','')
        if image_type == 'jpg':
            image_type = 'jpeg'
        audiofile.tag.images.set(3, imgs[a['cid']][0], f"image/{image_type}")
        audiofile.tag.artist = '/'.join(a['artistes'])
        audiofile.tag.album = a["name"]
        audiofile.tag.album_artist = '/'.join(a['artistes'])
        audiofile.tag.title = i['name']
        audiofile.tag.save(version=eyed3.id3.ID3_V2_3)
        print('*', end=' ')

    # lrc
    if sou_song['lyricUrl'] != None:
        print('lrc', end=' ')
        lrc_path = a["name"] + '/' + i['name'] + '.lrc'
        req_lrc = requests.get(sou_song['lyricUrl'])
        with open(lrc_path, 'w', encoding='utf8') as f:
            f.write(req_lrc.text)
            f.close()
        if global_mp3_path is not None:
            audiofile = eyed3.load(global_mp3_path)
            audiofile.tag.lyrics.set(req_lrc.text)
            audiofile.tag.save(version=eyed3.id3.ID3_V2_3)
        print('*', end=' ')
    # mv
    if sou_song['mvUrl'] != None:
        print('mv', end='')
        mv_path = a["name"] + '/' + i['name'] + '.mp4'
        if not os.path.isfile(mv_path):
            req_mv = requests.get(sou_song['mvUrl'])
            with open(mv_path, 'wb') as f:
                f.write(req_mv.content)
                f.close()
            mvc_type = os.path.splitext(sou_song['mvCover'])[-1]
            mvc_path = a["name"] + '/' + i['name'] + mvc_type
            req_mvc = requests.get(sou_song['mvCover'])
            with open(mvc_path, 'wb') as f:
                f.write(req_mvc.content)
                f.close()
        print('*', end=' ')
    print()
    