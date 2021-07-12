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
        match hexData[index + 1][1]:
            case '0':
                noteName = 'C'
            case '1':
                noteName = 'C#'
            case '2':
                noteName = 'D'
            case '3':
                noteName = 'D#'
            case '4':
                noteName = 'E'
            case '5':
                noteName = 'F'
            case '6':
                noteName = 'F#'
            case '7':
                noteName = 'G'
            case '8':
                noteName = 'G#'
            case '9':
                noteName = 'A'
            case 'a':
                noteName = 'A#'
            case 'b':
                noteName = 'B'
        octave = (int(hexData[index + 1][0], 16) % 4) + 2
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
                    match hexData[j][1]:
                        case '0':
                            hexData[j] = 'FixedDurationPause(HALF_NOTE)'
                        case '1':
                            hexData[j] = 'FixedDurationPause(DOTTED_QUARTER_NOTE)'
                        case '2':
                            hexData[j] = 'FixedDurationPause(TRIPLET_WHOLE_NOTE)'
                        case '3':
                            hexData[j] = 'FixedDurationPause(QUARTER_NOTE)'
                        case '4':
                            hexData[j] = 'FixedDurationPause(DOTTED_EIGHTH_NOTE)'
                        case '5':
                            hexData[j] = 'FixedDurationPause(TRIPLET_HALF_NOTE)'
                        case '6':
                            hexData[j] = 'FixedDurationPause(EIGHTH_NOTE)'
                        case '7':
                            hexData[j] = 'FixedDurationPause(DOTTED_SIXTEENTH_NOTE)'
                        case '8':
                            hexData[j] = 'FixedDurationPause(TRIPLET_QUARTER_NOTE)'
                        case '9':
                            hexData[j] = 'FixedDurationPause(SIXTEENTH_NOTE)'
                        case 'a':
                            hexData[j] = 'FixedDurationPause(DOTTED_THIRTY_SECOND_NOTE)'
                        case 'b':
                            hexData[j] = 'FixedDurationPause(TRIPLET_EIGHTH_NOTE)'
                        case 'c':
                            hexData[j] = 'FixedDurationPause(THIRTY_SECOND_NOTE)'
                        case 'd':
                            hexData[j] = 'FixedDurationPause(DOTTED_SIXTY_FOURTH_NOTE)'
                        case 'e':
                            hexData[j] = 'FixedDurationPause(TRIPLET_SIXTEENTH_NOTE)'
                        case 'f':
                            hexData[j] = 'FixedDurationPause(SIXTY_FOURTH_NOTE)'
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
