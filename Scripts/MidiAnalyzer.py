import Markov as mk
import time
import threading
import mido
from mido import MidiFile

# https://mido.readthedocs.io/en/latest/midi_files.html
tracks = []

def load_ports():
    # for potential sound generation...
    # does basically nothing right now
    inports = mido.get_input_names()
    outports = mido.get_output_names()
    print('In: ' + inports[0] + ' | Out: ' + outports[0])
    inport = mido.open_input(inports[0])
    outport = mido.open_output(outports[0])
    return inport, outport
def print_messages():
    for msg in midi_file:
        try:
            print(f'Channel: {msg.channel} - Note: {msg.note}({GetNoteName(msg.note)}) - Velocity {msg.velocity} - Time: {msg.time}')
        except:
            #print(f'{msg}')
            i=0
def print_meta_messages():
    for msg in midi_file:
        if msg.is_meta:
            print(msg)
def play_midi(m):
    print(f'Loading {m}...')
    for msg in m:
        time.sleep(msg.time)
        try:
            print(f'{msg} = {GetNoteName(msg.note % 12, False)}')
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
def GetNoteValue(midiNote):
    # print(f'note={midiNote.note % 12} vel={item.velocity} time={item.time}')
    print(f'{GetNoteName(midiNote.note % 12)}')
def GetNoteName(value, flats=True):
    value %= 12
    if value == 0:
        return 'C'
    elif value == 1:
        return 'Db' if flats else 'C#'
    elif value == 2:
        return 'D'
    elif value == 3:
        return 'Eb' if flats else 'D#'
    elif value == 4:
        return 'E'
    elif value == 5:
        return 'F'
    elif value == 6:
        return 'Gb' if flats else 'F#'
    elif value == 7:
        return 'G'
    elif value == 8:
        return 'Ab' if flats else 'G#'
    elif value == 9:
        return 'A'
    elif value == 10:
        return 'Bb' if flats else 'A#'
    elif value == 11:
        return 'B'
def get_max_channel():
    max = -1
    for msg in midi_file:
        try:
            if msg.channel > max:
                max = msg.channel
        except:
            i = 0
    return max
def copy(item, n, velocity, length):
    item.copy(note=n, velocity=velocity,time=length)





    #midi_path = 'Some MIDI Files/Castlevania - Heart of Fire.mid'
midi_path = 'Some MIDI Files/Darude_-_Sandstorm.mid'
midi_file = MidiFile(midi_path)


mk.train(midi_file)


