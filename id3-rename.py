# -*- coding: utf-8 -*-
# author: cgcel


import os
import argparse
import mutagen
from tqdm import tqdm


def format_song_name(dir_path):
    # 消除特殊字符
    intab = "/\:?*|\"\'<>$"
    outtab = "___________"
    trantab = str.maketrans(intab, outtab)

    files = os.listdir(dir_path)
    for filename in tqdm(files):
        file_path = os.path.join(dir_path, filename)
        file = mutagen.File(file_path)
        song_name = ''
        song_artist = ''

        try:
            file_type = filename.split('.')[-1]
            song_name = file.tags["TIT2"].text[0].strip().translate(trantab)
            # print(song_name)
            song_artist = file.tags["TPE1"].text[0].strip().translate(trantab)
            # print(song_artist)
        except Exception as e:
            print(e)

        try:
            if 'TITLE' in str(file.tags):
                for i in file.tags:
                    if i[0] == 'TITLE':
                        song_name = i[1]
                    if i[0] == "ARTIST":
                        song_artist = i[1]
        except Exception as e:
            print(e)
            continue

        if song_name != '' and song_artist != '':
            format_name = "{}-{}.{}".format(song_artist, song_name, file_type)
            if format_name == filename:
                pass
            else:
                format_file_path = os.path.join(dir_path, format_name)
                os.rename(file_path, format_file_path)
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
    except Exception as e:
        print(e)

