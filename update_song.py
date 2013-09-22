from os import listdir
from os.path import isfile, join
import pickle
import json
from shutil import copyfile
import sys
import ipdb
from pprint import pprint
import pyechonest

mypath = "/YOUR_USER_FOLDER/Projects/music-hackday/sectionizer/"


MEDIA="/YOUR_USER_FOLDER/FOLDER_OF_MP3S/" # + name + ".mp3"
JSON="/YOUR_USER_FOLDER/Projects/music-hackday/sectionizer/json/" #+ name + ".json"
PICKLE="/YOUR_USER_FOLDER/Projects/music-hackday/sectionizer/pkl/"
OUTPATH_MEDIA="/YOUR_USER_FOLDER/Projects/music-hackday/wavesurfer.js/example/media/"
OUTPATH_JSON="/YOUR_USER_FOLDER/Projects/music-hackday/wavesurfer.js/"

def copy_file_starts_with(start_str, from_folder, to_file):
    mypath = from_folder
    # print mypath
    files = [ f for f in listdir(mypath) if isfile(join(mypath,f)) ]
    # print files
    for f in files:
        if f.startswith(start_str):
            # print f
            print "about to copy from", from_folder + f, "to", to_file
            # return
            copyfile(from_folder + f, to_file)

def modify_annotation(json_dir_path):
    # lets make some assumptions about pop songs...

    """
    - beat machine ... so if beat is consistent enough, then let's set that as our global BPM
    - sections should align with bars
    - the first downbeat might be tough to find... can we "center" the beats around a solid, middle section
        and then extrapolate?
    - can we figure out chorus / verse by similar tatums? (as done by Paul)
    """

    ASSUME_CLICK_TRACK = True
    ASSUME_ONE_TEMPO = True # right now cant handle tempo change in song

    t = pickle.load(open(json_dir_path + "demo.pickle", "r"))

#
    # [song sections] sections should align with bars or beats
    # f

    inbeats = t.beats
    outbeats = []

    # Find a group of solid beats and extrapolate ...
    # Get BPM according to the beats...
    bpm_from_beats = 1 / ( reduce(lambda x, y: x+y[u'duration'], t.beats, 0) / len(t.beats) / 60 )

    if ASSUME_CLICK_TRACK:
        bpm = round(t.tempo)
    else:
        bpm = t.tempo

    spb = 60/bpm

    # find the window with the lowest deviation from
    window_size = 16
    deviation_from_spb = map(lambda x: abs(x['duration'] - spb), inbeats)

    idx = 0
    results = []
    while idx + window_size < len(deviation_from_spb):
        window = deviation_from_spb[idx:idx+window_size]
        window_avg = sum(window) / window_size
        results.append(window_avg)
        idx += 1

    best_window_idx = results.index(min(results))
    best_window = inbeats[best_window_idx : best_window_idx + window_size]
    best_window_confs = map(lambda x: x['confidence'], best_window)
    most_confident_beat = best_window_confs.index(max(best_window_confs))

    # extrapolate from this one!
    central_beat_start = inbeats[best_window_idx + most_confident_beat]['start']

    outbeats = [central_beat_start]
    pre_center_time = central_beat_start
    while pre_center_time > 0:
        pre_center_time -= spb
        outbeats.append(pre_center_time)

    post_center_time = central_beat_start
    while post_center_time < t.duration:
        post_center_time += spb
        outbeats.append(post_center_time)

    obeats_temp = []
    outbeats.sort()
    for o in outbeats:
        FLEX = .1 # can be off by this many seconds
        # if o > (t.end_of_fade_in - FLEX)
        # if o > (t.end_of_fade_in):
        if o > 0:
            obeats_temp.append({
                'start' : o,
                'confidence' : 1,
                'duration' : spb
            })
    # ipdb.set_trace()

    # count the number of beats per section. add +/- to make them fit with the time signature!


    print "about to write outjson"
    outjson = {}
    outjson['beats'] = obeats_temp
    outjson['bars'] = t.bars

    section_size = 16
    outjson['sections'] = obeats_temp[::section_size] # assume a section approx every section_size beats.. (note: depends on song starting on beat 1. downbeat pain)

    if t.song_id == u'SOAHVZF131634A84FA' or (t.song_id == u'SOGUUMT13F4F4835CB' and t.title == u'The Way'):
        # song 016 and song 014
        outjson['sections'] = obeats_temp[2::section_size] # there are 2 beats at start..
    # elif t.song_id == u'SOYAJLU13E58ED149E' and t.title == u'Come And Get It': # song 15
        # outjson['sections'] = obeats_temp[3::section_size] # there are 2 beats at start..

    outjson['sections'] = obeats_temp[2::section_size] # there are 2 beats at start..

    # Things that affect..
    #  - section size
    #  - start_of_fade_in
    #  - offset for first section (suppose strong first beat, no fade in, yet 2 beats of sound)

    # TODO: find the "beatmatched section" which is nearest to the section in the real song...
    osec_temp = []
    for s in t.sections:
        neighbors = find_adjacent_all(outjson, s['start'])
        osec_temp.append(neighbors['closest_section'])
    outjson['sections'] = osec_temp


    # TESTING
    # ipdb.set_trace()
    # find_adjacent_all(t, -1) # edge case
    # find_adjacent_all(t, 10)
    # find_adjacent_all(t, 5000) # edge case

    # pprint(outjson['sections'])

    # TODO: How to handle songs that don't start immediately?
    # TODO: How to guess "downbeats"?
    #   - strong confidence beats
    #   - may align with bars

    f = open(json_dir_path + "demo_modified.json", "w")
    f.write(json.dumps(outjson, sort_keys=True, indent=2))

    return outjson


def find_adjacent_all(track, second):
    """ Returns adjacent beats, tracks, sections """

    myBeats=None
    myBars=None
    mySections=None

    if type(track) == pyechonest.track.Track:
        myBeats = track.beats
        myBars = track.bars
        mySections = track.sections
    else:
        myBeats = track['beats']
        myBars = track['bars']
        mySections = track['sections']

    r = {}
    r['adjacent_beats'] = find_adjacent(myBeats, second)
    r['closest_beat'] = find_closest(r['adjacent_beats'], second)
    r['adjacent_bars'] = find_adjacent(myBars, second)
    r['closest_bar'] = find_closest(r['adjacent_bars'], second)
    r['adjacent_sections'] = find_adjacent(mySections, second)
    r['closest_section'] = find_closest(r['adjacent_sections'], second)

    # pprint(r)
    # ipdb.set_trace()
    return r

def find_adjacent(list_of_items, second):
    # NOTE: Assumes list_of_items is ordered
    prev = None
    for b in list_of_items:
        # first item through 2nd-to-last item
        if (prev is None or second > prev['start']) and second < b['start']:
            return [prev, b]
        prev = b

    # last item -- didnt find it yet
    return [b, None]

def find_closest(adjacent, second):
    # takes min and decides which is closer
    closest = None
    if adjacent[0] is None:
        return adjacent[1]
    elif adjacent[1] is None:
        return adjacent[0]
    else:
        left_distance = abs(adjacent[0]['start'] - second)
        right_distance = abs(adjacent[1]['start'] - second)
        print left_distance, right_distance
        if left_distance < right_distance:
            return adjacent[0]
        else:
            return adjacent[1]


def main():
    print 'Number of arguments:', len(sys.argv), 'arguments.'
    print 'Argument List:', str(sys.argv)
    args = sys.argv[1:]
    if args[0]:
        if args[0] == 'a':
            # annotation only
            print "recompiling annotation..."
            modify_annotation(OUTPATH_JSON)
        elif args[0] == 'many':
            for i in range(1,21):
                copy_and_annotate(str(i))
                f = open(json_dir_path + "demo_modified.json", "w")
                f.write(json.dumps(outjson, sort_keys=True, indent=2))
        else:
            start_str = args[0]
            copy_and_annotate(start_str)
    else:
        print "need a song #, e.g. '017'"


def copy_and_annotate(start_str):
    try:
        start_int = int(start_str)
        if start_int in range(101) and start_int != 0:
            copy_file_starts_with(start_str, MEDIA, OUTPATH_MEDIA + "demo.mp3")
            copy_file_starts_with(start_str, JSON, OUTPATH_JSON + "demo.json")
            copy_file_starts_with(start_str, PICKLE, OUTPATH_JSON + "demo.pickle")
            modify_annotation(OUTPATH_JSON)
        else:
            print "start_int must be between 1 and 100"
    except:
        raise
        print "invalid start_str", start_str


if __name__ == "__main__":
    main()