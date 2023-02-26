# -*- coding: utf-8 -*-
# author: cgcel


import os
import argparse
import mutagen
from tqdm import tqdm
import re


def format_song_name(dir_path):

    files = os.listdir(dir_path)
    for filename in tqdm(files):
        if os.path.isdir(filename):
            continue
        file_path = os.path.join(dir_path, filename)
        file = mutagen.File(file_path)
        song_name = ''
        song_artist = ''

        try:
            file_type = filename.split('.')[-1]
            song_name = re.sub('[\/:*?"<>|]', '_',
                               file.tags["TIT2"].text[0].strip()) # 消除特殊字符
            # print(song_name)
            song_artist = re.sub('[\/:*?"<>|]', '_',
                                 file.tags["TPE1"].text[0].strip())
            # print(song_artist)
        except Exception as e:
            print(e)

        try:
            if 'TITLE' in str(file.tags):
                for i in file.tags:
                    if i[0] == 'TITLE':
                        song_name = re.sub('[\/:*?"<>|]', '_', i[1].strip()) # 消除特殊字符
                        # print(song_name)
                    if i[0] == "ARTIST":
                        song_artist = re.sub('[\/:*?"<>|]', '_', i[1].strip())
                        # print(song_artist)
        except Exception as e:
            print(e)
            continue
        
        try:
            if song_name != '' and song_artist != '':
                format_name = "{}-{}.{}".format(song_artist, song_name, file_type)
                if format_name == filename:
                    pass
                else:
                    format_file_path = os.path.join(dir_path, format_name)
                    os.rename(file_path, format_file_path)
        except Exception as e:
            print(e)
    print("Transfer completed.")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="命令行参数")
    parser.add_argument('--path', help="dir path with songs")
    args = parser.parse_args()
    try:
        target_dir = args.path
        if target_dir is None:
            target_dir = os.getcwd()
        # print(target_dir)
        format_song_name(target_dir)
        # format_song_name("test")
    except Exception as e:
        print(e)
