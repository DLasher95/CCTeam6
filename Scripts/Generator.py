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
instrument = 63
msg_program = Message(type='program_change', channel=0, program=instrument, time=0)
track.append(msg_program)

# measure must add up to [w] ticks in 4/4
measure = [h, q, q, h, q, w, h, q, q, w]
progression = [0, 3, 4, 2, 6, 5, 1, 6, 3, 5]

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

print('Rhythm: ' + string_values(measure))
print('Progression: ' + string_values(progression))

key, mode = Scale.random_key_mode()
for msg in generate_chords(rhythm=measure, progression=progression, key=key, mode=mode):
    track.append(msg)
    print(msg)

print(Scale.get_note_name(key) + ' ' + Scale.get_mode_name(mode))

m.save('generated__.mid')