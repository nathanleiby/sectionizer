#!/usr/bin/env python
# encoding: utf-8

from pyechonest import config
import json
from os import listdir
from os.path import isfile, join
from pyechonest import track
import subprocess
# import ipdb
import pickle

#config.ECHO_NEST_API_KEY="SECRET"

mypath = "/Users/pika/Projects/music-hackday/sectionator/media/"

def main():

    files = [ f for f in listdir(mypath) if isfile(join(mypath,f)) ]
    for f in files[0:2]:
        if f.endswith(".mp3"):
            fetch_en_annotations(f)

def fetch_en_annotations(filename):
    songname = filename.rstrip('.mp3')
    print songname, "to json annotation"
    # from pyechonest import artist
    # bk = artist.Artist('bikini kill')
    # print "Artists similar to: %s:" % (bk.name,)
    # for similar_artist in bk.similar: print "\t%s" % (similar_artist.name,)

    f = open(mypath + filename)
    t = track.track_from_file(f, 'mp3')
    outfile = songname + '.json'
    print t.analysis_url
    myurl = t.analysis_url

    annotation = subprocess.check_output(["curl", myurl])
    # ipdb.set_trace()

    open(songname+'.json', 'w').write(json.dumps(annotation))
    pickle.dump(t, open(songname + ".pickle", "w"))
    # (Pdb) tt = pickle.load(open(songname + ".pickle", "r"))

# def convert(input):
#     if isinstance(input, dict):
#         return {convert(key): convert(value) for key, value in input.iteritems()}
#     elif isinstance(input, list):
#         return [convert(element) for element in input]
#     elif isinstance(input, unicode):
#         return input.encode('utf-8')
#     else:
#         return input


if __name__ == "__main__":
    main()
