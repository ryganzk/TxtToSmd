# What Is TxtToSmd?

I created this tool in the span of a couple days to aid with inserting custom music tracks into Pokemon Mystery Dungeon: Explorers of Sky, all without any knowledge or usage of hex editing. Instead, the provided application converts text into hexadecimal data, which is then compiled into a usable smd document!

# What Are Smd Files?

EoS uses smd files to determine music tracks, and what sounds to generate from them. Smd files contain hexadecimal data for individual tracks that tells the game whether to play a note, pause for a fixed duration, or apply a wide variety of effects to itself. These files do not contain information on the sample the track is tied to, as the game contains swd files that serve that purpose.

# How To Use

The application allows you to create a new smd file from scratch, or replace an existing one with the specified text document. Currently replacing an existing document will guarantee better results, as there are still hex bytes whos function is unknown and cannot be replicated at this time.

All you have to do is bring the installer, the designated text file, and the designated smd file if performing a replace. From there open the python script and follow the instructions. When the console prints out "Complete!" your smd file has successfuly been generated/updated.

This guide will not cover how to extract or import smd files from an EoS rom, however I would highly recommend checking out Tinke, a tool specifically made for that purpose

# Commands

There's quite a decent amount of commands, so here's a list of ones I can see being commonly used. For the ones not specified, check out [psy_commando's documentation on the smd file format](https://projectpokemon.org/docs/mystery-dungeon-nds/dse-smdl-format-r13/#Trk_Chunk), as all of the commands are found here.
 
| Command | Parameters | Function |
| --- | --- | --- |
| StartOfTrack() | 0 | Indicates the beginning of a new track (MUST BE USED) |
| EndOfTrack() | 0 | Indicates the end of a new track (MUST BE USED) |
| PlayNote()| 2-3 | Plays the specified note (see PlayNote section for more information) |
| FixedDurationPause() | 1 | Pauses for a specified duration (explicitly uses pause constants, a list of which can be found below) |
| SetTempo() | 1 | Sets the tempo of the song |
| LoopPoint() | 0 | Marks the location for the song to repeat once EndOfTrack() is reached |

# PlayNote

The PlayNote command is arguably the most important command, as that'll be your primary way of generating a tone in your custom music track. As such it's the only command that takes more than one parameter to fully utilize it.

The first parameter determines the volume of the played note. As is the case with all volume-related commands, this value ranges from 0 to 127. The second parameter determines the played note, as well as the octave. For instance, **C4** means the note played will be a C, and on the fourth octave. If a note has a sharp, simply include it after the note's letter (i.e. **A#5**). Octave numbers are between 2 and 5, and can be used in conjunction with the SetOctave() command for an even greater scope. The third parameter determines the amount of time the note is held in ticks. This parameter is completely optional, as an empty field simply represents a 0. Pause constants (described below) can be used below, as the application will use the tick amount they're equivalent to

# Pause Constants

Here's a list of all constants, as well as their corresponding tick values:

| Constant Name | Tick Value |
| --- | --- |
| HALF_NOTE | 96 |
| DOTTED_QUARTER_NOTE | 72 |
| TRIPLET_WHOLE_NOTE | 64 |
| QUARTER_NOTE | 48 |
| DOTTED_EIGHTH_NOTE | 36 |
| TRIPLET_HALF_NOTE | 32 |
| EIGHTH_NOTE | 24 |
| DOTTED_SIXTEENTH_NOTE | 18 |
| TRIPLET_QUARTER_NOTE | 16 |
| SIXTEENTH_NOTE | 12 |
| DOTTED_THIRTY_SECOND_NOTE | 9 |
| TRIPLET_EIGHTH_NOTE | 8 |
| THIRTY_SECOND_NOTE | 6 |
| DOTTED_SIXTY_FOURTH_NOTE | 4 |
| TRIPLET_SIXTEENTH_NOTE | 3 |
| SIXTY_FOURTH_NOTE | 2 |

# PLEASE READ THIS BEFORE CONTINUING

EoS smd files contain a starting track that is completely devoid of note data. I assume this is done so the rest of the tracks are able to be played smoothly. A good majority of these files contain hex data that translates to this:

StartOfTrack()<br/>
SetTrackExpression(INSERT_VOLUME)<br/>
TempoBPM(INSERT_BPM)<br/>
LoopPoint()<br/>
Pause16Bits(9)<br/>
EndOfTrack()

# Next Steps

I'll try to look at EoS's swd files and see if I can create a similar script for it. Hopefully now that I've finalized my first ever python script, I'll be able to create something slightly more optimized as a result??? Of course if issue reports are filed on this repository, fixing them will be my priority

# Credits

psy_commando for the documentation on PMD's smd files, I wouldn't have been able to create this parser if it weren't for how in-depth the man went with researching them
The entire SkyTemple community for the idea and links to a metric fuckton of information regarding EoS's inner mechanisms as a whole
