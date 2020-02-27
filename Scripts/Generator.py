import mido
from Scripts import Scale
from mido import MidiFile, MidiTrack, Message, MetaMessage


# create midi file, add a track
m = MidiFile()

# create single channel track
m.tracks.append(MidiTrack())
track = m.tracks[0]

# set song information
bpm = 120
tempo = mido.bpm2tempo(bpm)

# create create timings
q = m.ticks_per_beat
w = q * 4
h = q * 2
e = q // 2
#t = q // 3
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
instrument = 54
msg_program = Message(type='program_change', channel=0, program=instrument, time=0)
track.append(msg_program)

# measure must add up to [w] ticks in 4/4
measure = [h, q, q, h, q, q, h]
progression = [0, 1, 2, 3, 4, 5, 6]

def generate_chords(rhythm, progression, key, mode):
    if len(rhythm) != len(progression):
        print('Incompatible rhythm and progression')
        return
    messages = []
    current = []
    octave = 5
    offset = octave * 12
    for i in range(len(progression) + 1):
        # turn off current chord
        for k, n in enumerate(current):
            # only add delay for 2nd chord and beyond...
            messages.append(msg_note_off.copy(note=n, time=measure[i - 1] if k == 0 else 0))

        # turn on new chord, only if it's not the end of the progression
        if i < len(progression):
            chord = Scale.chord(key=key, mode=mode, root=progression[i], voices=3)
            current.clear()
            for note in chord:
                messages.append(msg_note_on.copy(note=note+offset))
                current.append(note+offset)
            print(string_values(current))


    return messages
def string_values(p):
    # https://www.geeksforgeeks.org/python-program-to-convert-a-list-to-string/
    return '[' + ', '.join(map(str, p)) + ']'

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


key, mode = Scale.random_key_mode()
print('Rhythm: ' + string_values(measure))
print('Progression: ' + string_values(progression))
print(Scale.get_note_name(key) + ' ' + Scale.get_mode_name(mode))
print(string_values(Scale.get_scale(key=key, mode=mode)))

for msg in generate_chords(rhythm=measure, progression=progression, key=key, mode=mode):
    track.append(msg)
    #print(msg)



m.save('generated__.mid')