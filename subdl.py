import os
from pythonopensubtitles.opensubtitles import OpenSubtitles

global LOGIN = ""
global PASSWORD = ""

def get_query(string):
    return string[0:string.find("-") - 1]

def get_season(string):
    start = string.find("-") + 2
    s_e = string[start : start + 6]
    return int(s_e[1:3])

def get_episode(string):
    start = string.find("-") + 2
    s_e = string[start : start + 6]
    return int(s_e[4:6])

def get_list():
    lang_id = "eng"
    extensions = (".mp4", ".mkv", ".avi")
    tmp = [x for x in os.listdir() if x.endswith(extensions)]
    res = []
    for x in tmp:
        new = {
            "sublanguageid": lang_id, 
            "query": get_query(x),
            "season": get_season(x),
            "episode": get_episode(x)
        }
        res.append(new)
    return res

def get_filename(d):
    return f"{d['query']} - S{d['season']:02}E{d['episode']:02}.srt"
    
def main():
    ost = OpenSubtitles()
    token = ost.login(LOGIN, PASSWORD)
    subs = get_list()
    id_list = []
    filenames = dict()
    for sub in subs:
        sub_name = get_filename(sub)
        #subtitle already in directory
        if sub_name in os.listdir():
            continue
        data = ost.search_subtitles([sub])
        #no sub found
        if len(data) == 0:
            continue
        sub_id = data[0]["IDSubtitleFile"]
        id_list.append(int(sub_id))
        filenames[sub_id] = sub_name
    for file in id_list:
        x = ost.download_subtitles([file], override_filenames = filenames)
        
if __name__ == "__main__":
    main()
