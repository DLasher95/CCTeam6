import mido
import os
import random
import math
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

def generate_chord_messages(rhythm, progression, key, mode, track=0, voices=3):
    if len(rhythm) != len(progression):
        print('Incompatible rhythm and progression')
        return
    messages = []
    current = []
    octave = 5
    offset = octave * 12
    for i in range(len(progression) + 1):
        # turn off each note of the current chord
        for k, n in enumerate(current):
            # only add delay for 2nd chord and beyond...
            messages.append(msg_note_off.copy(note=n, time=rhythm[i - 1] if k == 0 else 0, channel=track, velocity=50))

        # turn on new chord, only if it's not the end of the progression
        if i < len(progression):
            chord = Scale.chord(key=key, mode=mode, root=progression[i], voices=voices)
            current.clear()
            for note in chord:
                messages.append(msg_note_on.copy(note=note+offset, channel=track))
                current.append(note+offset)
    return messages
def generate_note_messages(rhythm, notes, track=0):
    if len(rhythm) != len(notes):
        print('Incompatible rhythm and progression')
        return
    messages = []
    currently_playing = -1

    for i, note in enumerate(notes):
        # turn on note
        messages.append(msg_note_on.copy(note=note, time=0, channel=track))
        # wait some time, turn off note
        messages.append(msg_note_off.copy(note=note, time=rhythm[i], channel=track))

    return messages

def generate_rhythm(length, options, min=-1, max=-1, max_length=-1, min_length=-1, debug=False):
    rhythm = []
    # while there are not enough or are too many beats in the rhythm
    while 0 <= min > len(rhythm) or 0 <= max < len(rhythm):
        rhythm = []
        while sum(rhythm) < length:
            beat = generate_beat(options)

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
def generate_beat(options):
    beat = random.choice(options)
    # tie randomly
    if random.random() < model.params['complexity']:
        beat += random.choice(options)

    return beat
def generate_progression(rhythm, debug=False):
    # ensure that (one of) the longest beat(s) is the tonic
    longest = max(rhythm)
    # https://thispointer.com/python-how-to-find-all-indexes-of-an-item-in-a-list/
    longest_indices = [i for i, r in enumerate(rhythm) if r == longest]

    # randomly set one of these to the tonic
    tonic_index = random.choice(longest_indices)

    # a 'happy' progression should not be composed primarily of minor chords...
    num_major_chords = round(model.params['happiness'] * len(rhythm))
    num_minor_chords = len(rhythm) - num_major_chords
    current_num_major, current_num_minor = 0, 0

    # set all to invalid
    p = [-1] * len(rhythm)
    p[tonic_index] = 0
    if is_major(0, model.mode):
        current_num_major += 1

    for i in range(0, len(p)):
        # dont set if it has already been set
        if p[i] >= 0:
            continue
        while True:
            p[i] = random.randint(0, 6)

            # doesn't match previous, and doesn't match next (if next exists)
            non_duplicate = p[i] != p[i - 1] and (i == len(p) - 1 or p[i] != p[i + 1])
            holds_major_constraint = current_num_major + is_major(p[i], model.mode) <= num_major_chords
            holds_minor_constraint = current_num_minor + (not is_major(p[i], model.mode)) <= num_minor_chords

            if non_duplicate and holds_major_constraint and holds_minor_constraint:
                current_num_major += is_major(p[i], model.mode)
                break

    # final interval
    cadence = False
    if cadence:
        # end with 4th, 5th, or 6th
        while True:
            p[len(p) - 1] = random.randint(4, 6)
            holds_major_constraint = current_num_major + is_major(p[len(p) - 1], model.mode) <= num_major_chords
            holds_minor_constraint = current_num_minor + (not is_major(p[len(p) - 1], model.mode)) <= num_minor_chords
            if p[-1] != p[-2] and holds_minor_constraint and holds_major_constraint:
                break
    if debug:
        print_progression(p)
    return p
def generate_melody(prog_intervals, prog_rhythm, rhythm_options):
    notes = []
    rhythm = []

    # define elsewhere?
    max_step = 10

    # specify, according to part or instrument?
    _min = model.range_min
    _max = model.range_max

    chromatic_range = range(_min, _max)

    scale_chromatic_values = Scale.get_scale(model.key, model.mode)
    # restore 0-11 values. Probably should be somewhere else...
    scale_chromatic_values = [c % 12 for c in scale_chromatic_values]
    # print("Scale values: " + str(scale_chromatic_values))

    # get members of range that fit in the scale
    scaled_range = []
    for n in chromatic_range:
        if n % 12 in scale_chromatic_values:
            scaled_range.append(n)

    #print("Full range: " + str(chromatic_range))
    #print("Scaled range: " + str(scaled_range))

    prev_note = random.choice(scaled_range)

    while sum(rhythm) < sum(prog_rhythm):
        # generate next note
        scale_note = random.choice([n for n in scaled_range if -10 <= n - prev_note <= 10])
        chromatic_note = random.choice([n for n in chromatic_range if -10 <= n - prev_note <= 10])
        next_note = scale_note

        next_beat = generate_beat(rhythm_options)
        while sum(rhythm) + next_beat > sum(prog_rhythm):
            next_beat = generate_beat(rhythm_options)

        # which progression interval is the melody currently in?
        sum_rhythm = sum(rhythm)
        current_interval = 0
        for i in range(len(prog_rhythm)):
            sum_here = sum(prog_rhythm[:i+1])
            if sum_rhythm > sum_here:
                current_interval = i
                break

        rhythm.append(next_beat)
        notes.append(next_note)
        prev_note = next_note

    return rhythm, notes

def existing_tonic_length(intervals, rhythm):
    min_tonic_ratio = 1 / 4
    min_tonic_length = 1 / 4 * w

    # get existing tonic length
    existing_tonic_length = 0
    for existing_beat in rhythm:
        if existing_beat == intervals[0]:
            existing_tonic_length += existing_beat
def is_major(interval, mode):
    ionian = [True, False, False, True, True, False, False]
    return ionian[(mode + interval) % 7]

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

def generate_section(length, num_tracks=-1, key_change=0):
    num_tracks = num_tracks if len(m.tracks) > num_tracks > 0 else len(m.tracks)

    # a section is defined by a progression
    prog_rhythm = generate_rhythm(length=length, options=[q, w, h], min=2)
    prog_intervals = generate_progression(prog_rhythm)

    # part 0 = melody
    # part 1 = accompaniment

    parts = [None] * num_tracks
    for i in range(num_tracks):
        messages = []

        if i == 0:
            mel_rhythm, mel_notes = generate_melody(prog_intervals=prog_intervals, prog_rhythm=prog_rhythm, rhythm_options=[q, e, s])
            messages = generate_note_messages(rhythm=mel_rhythm, notes=mel_notes, track=i)
        elif i == 1:
            messages = generate_chord_messages(prog_rhythm, prog_intervals, key=model.key, mode=model.mode)

        parts[i] = messages

    return parts
def write_section(parts):
    for i,p in enumerate(parts):
        for msg in p:
            m.tracks[i].append(msg)

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

words = random.choice(examples)

model = pc.calculate_model(words)
model.print_model()


# create midi file and add tracks
m = MidiFile()
for i,j in enumerate(model.instruments):
    m.tracks.append(MidiTrack())

set_instruments(model.instruments)

# type cannot be overridden. Copy these to append messages
msg_note_on = Message(type='note_on', channel=0, note=60, velocity=100, time=0)
msg_note_off = Message(type='note_off', channel=0, note=60, velocity=100, time=0)

set_bpm(model.bpm)

# create create timings
q = m.ticks_per_beat
w = q * 4
h = q * 2
e = q // 2
s = q // 4

A = generate_section(length=w * 3, num_tracks=2)
B = generate_section(length=w * 4, num_tracks=2, key_change=-2)
C = generate_section(length=w * 2, num_tracks=2, key_change=2)

write_section(A)
write_section(B)
write_section(A)
write_section(B)
write_section(C)
write_section(A)

# export file
save_file()


