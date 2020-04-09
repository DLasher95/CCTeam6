import mido
import os
import random
from Scripts import Scale, Instruments, Composition_Param_Calculator as pc
from mido import MidiFile, MidiTrack, Message, MetaMessage


class Composition:
    def __init__(self):
        self.midi_file = MidiFile()
        self.name = 'example'
        self.tracks = 0
    def add_track(self, instrument=-1):
        self.midi_file.tracks.append(MidiTrack())
        return self.midi_file.tracks.count() - 1
    def save_file(name='generated'):
        file_name = name + '.mid' if name.__contains__('.mid') else name
        # https://www.w3schools.com/python/python_file_remove.asp
        # because saving raises errors if the file already exists
        if os.path.exists(file_name):
            os.remove(file_name)
        m.save(file_name)


def set_bpm(bpm=-1):
    # tempo is the only requirement
    if bpm <= 60:
        bpm = random.randint(70, 160)
        print('BPM set to ' + str(bpm))
    tempo = mido.bpm2tempo(bpm)
    m.tracks[0].append(MetaMessage('set_tempo', tempo=tempo, time=0))
    #track.append(MetaMessage('time_signature', numerator=4, denominator=4, clocks_per_click=24, notated_32nd_notes_per_beat=8, time=0))
    #track.append(MetaMessage('key_signature', key=Scale.get_note_name(0)))
def set_instrument_single_track(ins=-1, debug=False):
    # https://i.gyazo.com/38682c2adf56d01422a7266f62c4794f.png
    if not (0 <= ins <= 127):
        ins = random.randint(0, 127)
    if debug:
        print('Instrument set to: ' + Instruments.instruments[ins])
    msg_program = Message(type='program_change', channel=0, program=ins, time=0)
    m.tracks[0].append(msg_program)
def set_instruments(instruments):
    for i,ins in enumerate(instruments):
        m.tracks[i].append(Message(type='program_change', channel=i, program=ins, time=0))

def generate_messages(rhythm, progression, key, mode, track=0, voices=3):
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
            messages.append(msg_note_off.copy(note=n, time=rhythm[i - 1] if k == 0 else 0, channel=track))

        # turn on new chord, only if it's not the end of the progression
        if i < len(progression):
            chord = Scale.chord(key=key, mode=mode, root=progression[i], voices=voices)
            current.clear()
            for note in chord:
                messages.append(msg_note_on.copy(note=note+offset, channel=track))
                current.append(note+offset)
            #print(string_values(current))
    return messages
def generate_rhythm(length, options, min=-1, max=-1, max_length=-1, min_length=-1, debug=False):
    rhythm = []
    # while there are not enough or are too many beats in the rhythm
    while 0 <= min > len(rhythm) or 0 <= max < len(rhythm):
        rhythm = []
        while sum(rhythm) < length:
            beat = random.choice(options)

            # 50% chance to add a tie
            if random.random() < 0.5:
                beat += random.choice(options)

            # Rules
            # length must equal rhythm
            # ensure length of measure is not exceeded
            while sum(rhythm) + beat > length:
                beat = random.choice(options)
                if random.random() < 0.5:
                    beat += random.choice(options)
            rhythm.append(beat)

    if debug:
        print_rhythm(rhythm)
    return rhythm
def generate_beat(options, min_length=-1, max_length=-1):
    beat = random.choice(options)
    # tie randomly
    if random.random() < 0.5:
        beat += random.choice(options)

    # while max_length < 0 or beat > max_length or beat < min_length

    return beat
def generate_progression(rhythm, debug=False):
    # ensure that (one of) the longest beat(s) is the tonic
    longest = max(rhythm)
    # https://thispointer.com/python-how-to-find-all-indexes-of-an-item-in-a-list/
    longest_indices = [i for i, r in enumerate(rhythm) if r == longest]
    #for i,r in enumerate(rhythm):
        #if r == longest:
            #longest_indices.append(i)

    # randomly set one of these to the tonic
    tonic_index = random.choice(longest_indices)

    # set all to invalid
    p = [-1] * len(rhythm)
    p[tonic_index] = 0

    for i in range(0, len(p)):
        # dont set if it has already been set
        if p[i] >= 0:
            continue
        while True:
            p[i] = random.randint(0, 6)
            # doesn't match previous, and doesn't match next (if next exists)
            if p[i] != p[i - 1] and (i == len(p) - 1 or p[i] != p[i + 1]):
                break

    cadence = False
    if cadence:
        # end with 4th, 5th, or 6th
        while True:
            p[len(p) - 1] = random.randint(4, 6)
            if p[-1] != p[-2]:
                break
    if debug:
        print_progression(p)
    return p
def existing_tonic_length(intervals):
    min_tonic_ratio = 1 / 4
    min_tonic_length = 1 / 4 * w

    # get existing tonic length
    existing_tonic_length = 0
    for existing_beat in rhythmA:
        if existing_beat == intervals[0]:
            existing_tonic_length += existing_beat

def print_rhythm(rhythm):
    print('Rhythm: [' + ', '.join('%.2f' % round(r / w, 2) for r in rhythm) + ']')
def print_progression(progression):
    print('Progression: [' + ', '.join(str(p + 1) for p in progression) + ']')
def save_file(name='generated'):
    file_name = name + '.mid' if not name.__contains__('.mid') else name
    # https://www.w3schools.com/python/python_file_remove.asp
    # because saving raises errors if the file already exists
    if os.path.exists(file_name):
        os.remove(file_name)
    m.save(file_name)

examples = [
    ['white', 'sheep', 'standing', 'field', 'happiness'],
    ['man', 'umbrella', 'standing', 'front', 'building', 'fear', 'sadness', 'calmness'],
    ['man', 'holding', 'cell', 'phone', 'hand', 'anger'],
    ['brown', 'bear', 'standing', 'field', 'next', 'tree', 'calmness'],
    ['dog', 'sitting', 'green', 'grass', 'covered', 'field', 'happiness'],
    ['vase', 'flowers', 'sitting', 'table', 'fear', 'happiness'],
    ['man', 'suit', 'tie', 'calmness'],
    ['man', 'sitting', 'table', 'laptop', 'calmness'],
    ['man', 'wearing', 'hat', 'tie', 'anger'],
    ['black', 'white', 'cat', 'sitting', 'couch', 'fear'],
    ['woman', 'sitting', 'bench', 'pink', 'umbrella', 'calmness']
]

# random.seed(42)
# pc.np.random.seed(42)

phrase = random.choice(examples)

instruments, bpm, mode = pc.calculate_params(phrase, debug=True)

# create midi file and add tracks
m = MidiFile()
for i,j in enumerate(instruments):
    m.tracks.append(MidiTrack())

set_instruments(instruments)
#set_instrument(instruments[0])

# type cannot be overridden. Copy these to append messages
msg_note_on = Message(type='note_on', channel=0, note=60, velocity=100, time=0)
msg_note_off = Message(type='note_off', channel=0, note=60, velocity=100, time=0)

set_bpm(bpm)

# create create timings
q = m.ticks_per_beat
w = q * 4
h = q * 2
e = q // 2
s = q // 4


scale = Scale.Scale(mode=mode)
print(Scale.get_note_name(scale.key) + ' ' + Scale.get_mode_name(scale.mode) + ' at ' + str(bpm) + 'bpm')

def generate_section(length, t_num=-1, key_change=0):
    t_num = t_num if len(m.tracks) > t_num >= 0 else len(m.tracks)

    parts = [None] * t_num
    for i in range(t_num):
        # print('PART: ' + str(i))
        # generate messages for each part
        rhythm = generate_rhythm(length=length, options=[e, h, w], min=2, max=8)
        melody = generate_progression(rhythm)
        messages = generate_messages(rhythm=rhythm, progression=melody, key=(scale.key + key_change) % 12, mode=scale.mode, voices=1, track=i)
        parts[i] = messages

        #for msg in messages:
        # for msg in parts[i]:
        #     m.tracks[i].append(msg)
    return parts
def write_section(parts):
    for i,p in enumerate(parts):
        for msg in p:
            m.tracks[i].append(msg)

A = generate_section(length=w * 3)
B = generate_section(length=w * 4, key_change=-3)
C = generate_section(length=w * 2, key_change=4)

write_section(A)
write_section(B)
write_section(A)
write_section(B)
write_section(C)
write_section(A)

# print('-------------------------------------')
# for msg in m:
#     print(msg)
#
#
# for track in m.tracks:
#     for msg in track:
#         print(msg)

# rhythmA = generate_rhythm(length=2 * w, options=[h, q], min=2, debug=True)
# progressionA = generate_progression(rhythmA, debug=True)
#
# rhythmB = generate_rhythm(length=2 * w, options=[h, q], min=2, debug=True)
# progressionB = generate_progression(rhythmB, debug=True)
#
# rhythmC = generate_rhythm(length=2 * w, options=[h, q], min=2, debug=True)
# progressionC = generate_progression(rhythmC, debug=True)
#
# for A in generate_messages(rhythm=rhythmA, progression=progressionA, key=scale.key, mode=scale.mode):
#     m.tracks[0].append(A)
# for B in generate_messages(rhythm=rhythmB, progression=progressionB, key=scale.key, mode=scale.mode):
#     m.tracks[0].append(B)
# for A in generate_messages(rhythm=rhythmA, progression=progressionA, key=scale.key, mode=scale.mode):
#     m.tracks[0].append(A)
# for C in generate_messages(rhythm=rhythmC, progression=progressionC, key=scale.key, mode=scale.mode):
#     m.tracks[0].append(C)
# for A in generate_messages(rhythm=rhythmA, progression=progressionA, key=scale.key, mode=scale.mode):
#      m.tracks[0].append(A)
# for B in generate_messages(rhythm=rhythmB, progression=progressionB, key=scale.key, mode=scale.mode):
#     m.tracks[0].append(B)

# export file
save_file()



