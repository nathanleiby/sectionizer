sectionizer
===========

uses EchoNest API and heuristics to guess the exact beat where sections start. build during Music Hack Day Chicago 2013.

During HackDay, I'm looking particularly at "Billboard" songs, which are formulaic and regular.

## How it Works


1. **Use EchoNest API to fetch song details**. I'm particularly using
    - beats (start, confidence)
    - bars
    - sections
    - end_of_fade_in
2. **Python post-processing**. Take EchoNest's guesses for sections and then "do work". My goal is to make the beat more exact and get the section starts *exactly* right. Challenges:
    - Pause at the start of song
    - Variable Tempo
    - Changing phrase length (extra measure thrown in, some 8-bar, some 16)
    - and more TBD... especially as I move away from Pop music
3. **Visualization**
    - Visualization so i can listen and compare EN's sections vs my sections.

## Caveat: Pop Music simplicity

Regular beat. 4/4. Similar length phrases. Repeated Areas.

## Why I'm building this

I'd like to be able to

1. Take any song and very easily produce something like the infinite Gangam style or Bangarang song.
2. Pick multiple songs and sync them up, if possible (this was my initial goal, but i took a right-turn and looked at the "sections" problem starting last evening)
3. Learn more about WebAudioAPI

## Example Songs during Demo

1. easy one : Daft Punk

`004 Daft Punk - Get Lucky (feat. Pharrell Williams).mp3`

%run update_song.py 004

2. harder one : has sound at start .. but can offset by beats... I need to get better at automating this

`016 Capital Cities - Safe and Sound.mp3`

%run update_song.py 016

3. harder one : has quiet at start.. but can use start_of thing to work it

`017 Pink - Just Give Me A Reason feat. Nate Ruess.mp3`

%run update_song.py 017

4. to improve... total mess

`015 Selena Gomez - Come and Get It.mp3`

%run update_song.py 015

5. others that work ok

`012 Maroon 5 - Love Somebody.mp3`

%run update_song.py 012

`007 Florida Georgia Line ft. Nelly - Cruise.mp3`

%run update_song.py 007

`009 Anna Kendrick - Cups.mp3`

%run update_song.py 009

## Future Work

More Sections.

- Right now I am basically finding "the closet place to an EN guessed section". But there are more sections in the song than just these. (or occasionally, they might not be real user-perceived sections.)
- Granualarity of sections? (e.g. fills/prechorus/break/pickup/other vs intro/verse/chorus/outro)

Improved quality.

- could use machine learning or other techniques to do this at scale. right now i am just investigating and using heuristics (4/4 songs mostly, even tempo)
- ideally, want to run this against hundereds of songs with EN-annotations, automated-Python-annotations, and gold "human" annotations so i can see how i'm improving or breaking the algo with each change
- then, can do a real analysis of effectiveness

Naming Sections

If I can look for similar sounds, e.g. as done by Paul in [Pop Structure](http://musicmachinery.com/2012/11/19/visualizing-the-structure-of-pop-music/), I would like to be able to guess what's a chorus vs a verse, intro, etc.

## Related Projects

- Webaudio API book http://chimera.labs.oreilly.com/books/1234000001552/ch04.html
- http://moduscreate.com/touch-dj-a-sencha-touch-dj-app/
- webAudio spec https://dvcs.w3.org/hg/audio/raw-file/tip/webaudio/specification.html
- EchoNest Analyze track documentation ...  http://developer.echonest.com/docs/v4/_static/AnalyzeDocumentation.pdf
- pop structure http://musicmachinery.com/2012/11/19/visualizing-the-structure-of-pop-music/
- Remix.JS graph http://tide-pool.ca/remix-graph/examples/graph.html?trid=TRJNCBX14141A5C329
- infinite song .. http://static.echonest.com/mobiustube/

