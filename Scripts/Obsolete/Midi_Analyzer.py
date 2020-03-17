from Scripts import Scale
import time
import threading
import mido
from mido import MidiFile, MidiTrack

# https://mido.readthedocs.io/en/latest/midi_files.html
# http://support.ircam.fr/docs/om/om6-manual/co/MIDI-Concepts.html

tracks = []

def print_ports():
    # for potential sound generation...
    # nonfunctional
    inports = mido.get_input_names()
    outports = mido.get_output_names()
    for i, p in enumerate(inports):
        print('Inport: ' + i + ' ' + p)
    for i, p in enumerate(outports):
        print('Outport: ' + i + ' ' + p)
def print_notes():
    for msg in midi_file:
        try:
            print(f'Channel: {msg.channel} - {msg.type} - Note: {msg.note}({Scale.get_note_name(msg.note)}{msg.note//12 - 1}) - Vol: {msg.velocity} - Time: {msg.time}')
        except:
            i=0
def print_messages():
    for msg in midi_file:
        print(msg)
def print_meta_messages():
    for msg in midi_file:
        if msg.is_meta:
            print(msg)
def play_midi(m):
    print(f'Loading {m}...')
    for msg in m:
        time.sleep(msg.time)
        try:
            print(f'{msg}')
        except:
            nope = 0

def set_tracks():
    print(f'Tracks: {len(midi_file.tracks)}')
    for track in midi_file.tracks:
        print(track.name)
        tracks.append(track)
def print_tracks():
    for track in tracks:
        print(track.name)
        for msg in track:
            print(f'{track.name} - {msg}')
def print_tracks_info():
    print(f'Tracks: {len(tracks)}')
    for track in tracks:
        print(track.name)
def play_track(track):
    for msg in track:
        print(msg)
        time.sleep(msg.time)
def play_tracks():
    for track in tracks:
        thrd = threading.Thread(target=play_track(track))
    for msg in track:
        print(f'{track}: {msg}')
        time.sleep(msg.time)

def get_max_channel():
    max = -1
    for msg in midi_file:
        try:
            if msg.channel > max:
                max = msg.channel
        except:
            i = 0
    return max
def copy_note(item, n, velocity, length):
    item.copy_note(note=n, velocity=velocity, time=length)
def copy_file(file):
    mid = MidiFile()
    for i, track in enumerate(file.tracks):
        mid.tracks.append(MidiTrack())
        for msg in track:
            if msg.type == 'note_on' or msg.type == 'note_off' or msg.type == 'program_change':
                mid.tracks[i].append(msg.copy())
    filename = '../generated.mid'
    mid.save(filename)
    return filename

file_name = '../../Example MIDI Files/Mario_something.mid'
midi_file = MidiFile(file_name)

print_messages()