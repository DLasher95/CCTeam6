import mido
import random
from Scripts import Scale
from mido import MidiFile, MidiTrack, Message, MetaMessage


# create midi file, add a track
m = MidiFile()

# create single channel track
m.tracks.append(MidiTrack())
track = m.tracks[0]

# set song information
bpm = random.randint(70, 160)
tempo = mido.bpm2tempo(bpm)

# create create timings
q = m.ticks_per_beat
w = q * 4
h = q * 2
e = q // 2
s = q // 4

# set meta information (only tempo is required)
track.append(MetaMessage('set_tempo', tempo=tempo, time=0))
track.append(MetaMessage('time_signature', numerator=4, denominator=4, clocks_per_click=24, notated_32nd_notes_per_beat=8, time=0))
track.append(MetaMessage('key_signature', key=Scale.get_note_name(0)))

# type cannot be overridden
msg_note_on = Message(type='note_on', channel=0, note=60, velocity=100, time=0)
msg_note_off = Message(type='note_off', channel=0, note=60, velocity=100, time=0)

# set instrument
# https://i.gyazo.com/38682c2adf56d01422a7266f62c4794f.png
instrument = 48
msg_program = Message(type='program_change', channel=0, program=instrument, time=0)
track.append(msg_program)

def generate_chords(rhythm, progression, key, mode, voices=3, octave=5):
    if len(rhythm) != len(progression):
        print('Incompatible rhythm and progression')
        return
    messages = []
    current = []
    offset = octave * 12
    for i in range(len(progression) + 1):
        # turn off current chord
        for k, n in enumerate(current):
            # only add delay for 2nd chord and beyond...
            messages.append(msg_note_off.copy(note=n, time=rhythm[i - 1] if k == 0 else 0))

        # turn on new chord, only if it's not the end of the progression
        if i < len(progression):
            chord = Scale.chord(key=key, mode=mode, root=progression[i], voices=voices)
            current.clear()
            for note in chord:
                messages.append(msg_note_on.copy(note=note+offset))
                current.append(note+offset)
            #print(string_values(current))
    return messages
def generate_rhythm(length, options):
    rhythm = []
    while sum(rhythm) < length:
        beat = random.choice(options)
        # ensure length is not exceeded
        while sum(rhythm) + beat > length:
            beat = random.choice(options)
        rhythm.append(beat)
    return rhythm
def generate_progression(rhythm):
    # set all to 0
    p = [0] * len(rhythm)
    for i in range(1, len(p)):
        while True:
            p[i] = random.randint(0, 6)
            if p[i] != p[i - 1]:
                break

    # 4, 5, or 6
    while True:
        p[len(p) - 1] = random.randint(3, 5)
        if p[-1] != p[-2]:
            break
    return p

# params
def mode_by_score(score):
    # brightest first
    ranked_modes = [3, 0, 4, 1, 5, 2, 6]
    if score < 0 or score > 1:
        print('Expected score in range [0,1]')
        return -1

    # get int nearest score
    return round(score)
def bpm_by_score(score):
    if score < 0 or score > 1:
        print('Excpected value in range [0,1]')
        return -1

    bpm_min, bpm_max = 40, 180
    bpm_range = bpm_max - bpm_min
    return bpm_min + round(bpm_range * score)

def string_values(p):
    # https://www.geeksforgeeks.org/python-program-to-convert-a-list-to-string/
    return '[' + ', '.join(map(str, p)) + ']'


key, mode = Scale.random_key_mode()
print(Scale.get_note_name(key) + ' ' + Scale.get_mode_name(mode) + ' at ' + str(bpm) + 'bpm')
rhythm = generate_rhythm(2 * w, [w, h, q])
progression = generate_progression(rhythm)
print('Rhythm: ' + string_values(rhythm))
print('Progression: ' + string_values(progression))

# write messages
repeats = 4
for i in range(0, repeats):
    for msg in generate_chords(rhythm=rhythm, progression=progression, key=key, mode=mode, voices=1, octave=5):
        track.append(msg)

# https://www.w3schools.com/python/python_file_remove.asp
# because saving raises errors if the file already exists
import os
if os.path.exists('generated.mid'):
    os.remove('generated.mid')
m.save('generated.mid')