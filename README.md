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

    Regular beat.

## Why I'm building this

I'd like to be able to

1. Take any song and very easily produce something like the infinite Gangam style or Bangarang song.
2. Pick multiple songs and sync them up, if possible (this was my initial goal, but i took a right-turn and looked at the "sections" problem starting last evening)
3. Learn more about WebAudioAPI

## Example Songs during Demo

1. easy one : Daft Punk
2. harder one : has a pause at start.. but can use start_of thing to work it
3. harder yet : has 4 and 8 bar fills, so i can't just guess that sections are repeatedly in blocks of 16
4. to improve in the future...

## Future Work

- could use machine learning or other techniques to do this at scale. right now i am just investigating and using heuristics (4/4 songs mostly, even tempo)
- ideally, want to run this against hundereds of songs with EN-annotations, automated-Python-annotations, and gold "human" annotations so i can see how i'm improving or breaking the algo with each change
- then, can do a real analysis of effectiveness
