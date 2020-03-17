import random
import mido
from mido import MidiFile
# what things to store?

# random choice
# https://stackoverflow.com/questions/4859292/how-to-get-a-random-value-from-dictionary-in-python
notes = []
#random.choice(notes)

# dictionaries
# https://www.w3schools.com/python/python_dictionaries.asp
# { note : recorded_data[] }
channel_notes = {}
note_velocities = {}
note_neighbors = {}
note_times = {}
note_successors = {}

def train(midi):
    for i, msg in enumerate(midi):
        try:
            if not notes.__contains__(msg.note):
                # initialize lists
                notes.append(msg.note)
                note_velocities[msg.note] = []
                note_successors[msg.note] = []
                note_times[msg.note] = []
            # add data
            note_velocities[msg.note].append(msg.velocity)
            note_times[msg.note].append(msg.time)
            note_successors[msg.note].append(midi[i+1].note)
        except:
            i=0
    print(f'Notes: {len(notes)}')
    print(f'Velocity keys: {len(note_velocities.keys())}')
    print(f'Time keys: {len(note_times.keys())}')
    print(f'Successors keys: {len(note_successors.keys())}')