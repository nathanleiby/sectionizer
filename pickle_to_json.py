from os import listdir
from os.path import isfile, join
import pickle
import json

mypath = "/Users/pika/Projects/music-hackday/sectionator/"
files = [ f for f in listdir(mypath) if isfile(join(mypath,f)) ]
for f in files:
    if f.endswith(".pickle"):
        p = pickle.load(open(mypath + f,"r"))
        json_filename = f.rstrip(".pickle") + ".json"
        f = open(mypath + "json/" + json_filename,"w")

        d = {}
        keys = [
            'title',
            'danceability',
            'energy',
            'beats',
            'bars',
            'sections',
            'end_of_fade_in',
            'tempo',
            'tempo_confidence',
            'time_signature',
            'time_signature_confidence',
            'rhythm_version',
            'rhythm_string',
            'segments',
            'tatums'
        ]

        print p
        d['beats'] = p.beats
        d['bars'] = p.bars
        d['sections'] = p.sections

        f.write(json.dumps(d, sort_keys=True, indent=2))


