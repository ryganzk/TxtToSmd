import os
from sre_constants import JUMP

commands= [
    ['90', 'RepeatLastPause()', 0],
    ['91', 'AddToLastPause()', 1], 
    ['92', 'Pause8Bits()', 1],
    ['93', 'Pause16Bits()', 2], 
    ['94', 'Pause24Bits()', 3],
    ['95', 'PauseUntilRelease()', 1],
    ['98', 'EndOfTrack()', 0],
    ['99', 'LoopPoint()', 0],
    ['9c', '9C()', 1],
    ['9d', '9D()', 0],
    ['9e', '9E()', 0],
    ['a0', 'SetTrackOctave()', 1],
    ['a1', 'AddToTrackOctave()', 1],
    ['a4', 'SetTempo()', 1],
    ['a5', "SetTempo()", 1],
    ['a8', 'A8()', 2],
    ['a9', 'A9()', 1],
    ['aa', 'AA()', 1],
    ['ab', 'SkipNextByte()', 0],
    ['ac', 'SetProgram()', 1],
    ['af', 'AF()', 3],
    ['b0', 'B0()', 0],
    ['b1', 'B1()', 1],
    ['b2', 'B2()', 1],
    ['b3', 'B3()', 1],
    ['b4', 'B4()', 2],
    ['b5', 'B5()', 1],
    ['b6', 'B6()', 1],
    ['bc', 'BC()', 1],
    ['be', 'BE()', 1],
    ['bf', 'BF()', 1],
    ['c0', 'C0()', 1],
    ['c3', 'C3()', 1],
    ['cb', 'SkipNext2Bytes()', 0],
    ['d0', 'D0()', 1],
    ['d1', 'D1()', 1],
    ['d2', 'D2()', 1],
    ['d3', 'D3()', 2],
    ['d4', 'D4()', 3],
    ['d5', 'D5()', 2],
    ['d6', 'D6()', 2],
    ['d7', 'PitchBend()', 2],
    ['d8', 'D8()', 2],
    ['db', 'DB()', 1],
    ['df', 'DF()', 1],
    ['e0', 'SetTrackVolume()', 1],
    ['e1', 'E1()', 1],
    ['e2', 'E2()', 3],
    ['e3', 'SetTrackExpression()', 1],
    ['e7', 'E7()', 1],
    ['e8', 'SetTrackPan()', 1],
    ['e9', 'E9()', 1],
    ['ea', 'EA()', 3],
    ['ef', 'EF()', 1],
    ['f2', 'F2()', 2],
    ['f3', 'F3()', 3],
    ['f6', 'F6()', 1]
]

def GetFile(fileName, directory):
    for root, dir, files in os.walk(directory):
        if fileName in files: return True
    return False

smdDoc = input('What is the name of the file you would like to receive a text definition for? ')
while(GetFile(smdDoc + '.smd', os.getcwd()) == False): smdDoc = input('That file could not be found, try again: ')

with open (smdDoc + '.smd', 'rb') as i:
    chnls = []
    lines = i.read().hex().split('656f632000000001')[0].split('74726b2000000001')[1:]
    for j in lines:
        index = lines.index(j)
        chnls.append(j[19])
        while(j[-4:-2] == '98'): j = j[:-2]
        lines[index] = j[24:]

    hexData = [''.join(lines)[index : index + 2] for index in range(0, len(''.join(lines)), 2)]

    def NoteTicks(iterator, index):
        switchNote = {
            '0': 'C',
            '1': 'C#',
            '2': 'D',
            '3': 'D#',
            '4': 'E',
            '5': 'F',
            '6': 'F#',
            '7': 'G',
            '8': 'G#',
            '9': 'A',
            'a': 'A#',
            'b': 'B',
        }

        noteName = switchNote.get(hexData[index + 1][1])

        switchOct = {
            0: '0',
            1: '-',
            3: '+'
        }

        octave = switchOct.get(int(hexData[index + 1][0], 16) % 4, '')

        tickVar = ''
        hexData.pop(index + 1)
        for l in range(iterator):
            tickVar = hexData[index + 1] + tickVar
            hexData.pop(index + 1)
        if tickVar == '': hexData[index] = 'PlayNote(' + str(int(hexData[index], 16)) + ', ' + noteName + str(octave) + ')'
        else: hexData[index] = 'PlayNote(' + str(int(hexData[index], 16)) + ', ' + noteName + str(octave) + ', ' + str(int(tickVar, 16)) + ')'
            

    for j in range(len(hexData)):
        try:
            if hexData[j][0].isnumeric():
                if int(hexData[j][0]) < 8:
                    if int(hexData[j + 1][0], 16) < 8:
                        if int(hexData[j + 1][0], 16) < 4:
                            NoteTicks(0, j)
                        else:
                            NoteTicks(1, j)
                    else:
                        if int(hexData[j + 1][0], 16) < 12:
                            NoteTicks(2, j)
                        else:
                            NoteTicks(3, j)
                elif int(hexData[j][0]) == 8:
                    switchPause = {
                        '0': 'FixedDurationPause(HALF_NOTE)',
                        '1': 'FixedDurationPause(DOTTED_QUARTER_NOTE)',
                        '2': 'FixedDurationPause(TRIPLET_WHOLE_NOTE)',
                        '3': 'FixedDurationPause(QUARTER_NOTE)',
                        '4': 'FixedDurationPause(DOTTED_EIGHTH_NOTE)',
                        '5': 'FixedDurationPause(TRIPLET_HALF_NOTE)',
                        '6': 'FixedDurationPause(EIGHTH_NOTE)',
                        '7': 'FixedDurationPause(DOTTED_SIXTEENTH_NOTE)',
                        '8': 'FixedDurationPause(TRIPLET_QUARTER_NOTE)',
                        '9': 'FixedDurationPause(SIXTEENTH_NOTE)',
                        'a': 'FixedDurationPause(DOTTED_THIRTY_SECOND_NOTE)',
                        'b': 'FixedDurationPause(TRIPLET_EIGHTH_NOTE)',
                        'c': 'FixedDurationPause(THIRTY_SECOND_NOTE)',
                        'd': 'FixedDurationPause(DOTTED_SIXTY_FOURTH_NOTE)',
                        'e': 'FixedDurationPause(TRIPLET_SIXTEENTH_NOTE)',
                        'f': 'FixedDurationPause(SIXTY_FOURTH_NOTE)'
                    }
                    
                    hexData[j] = switchPause.get(hexData[j][1])
            for k in commands:
                if hexData[j] == k[0]:
                    hexVar = ''

                    for l in range(k[2]):
                        if hexData[j + 1] != '00': hexVar = hexData[j + 1] + hexVar
                        hexData.pop(j + 1)
                    if k[2] > 0: 
                        if hexVar == '': hexVar = '0'
                        hexData[j] = k[1][:-1] + str(int(hexVar, 16)) + k[1][-1:]
                    else: hexData[j] = k[1]
                if hexData[j] == 'EndOfTrack()' and j != len(hexData) - 1:
                    hexData[j] += '\n\nStartOfTrack(' + str(int(chnls[1], 16)) + ')'
                    chnls.pop(1)
        except IndexError:
            ''

with open(smdDoc + '.txt', 'w') as j:
    j.write('StartOfTrack(0)\n' + ''.join(f"{element}\n" for element in hexData))

print('Complete!')
