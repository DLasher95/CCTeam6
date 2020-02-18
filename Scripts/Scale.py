# Modes
    # 0 = Ionian
    # 1 = Dorian,
    # 2 = Phrygian,
    # 3 = Lydian,
    # 4 = Mixolydian,
    # 5 = Aeolian,
    # 6 = Locrian
#   # Notes / Keys
    # 0 = C
    # 1 = C# / Db
    # 2 = D
    # 3 = D# / Eb
    # 4 = E
    # 5 = F
    # 6 = F# / Gb
    # 7 = G
    # 8 = G# / Ab
    # 9 = A
    # 10 = A# / Bb
    # 11 = B


import random
c_major = [0, 2, 4, 5, 7, 9, 11]
key, mode = 0, 0
scale = c_major[:]


def print_scale():
    print(f'\'{get_note_name(key)} {get_mode_name(mode)}\'')
    for i in range(0, 7):
        interval = (mode + i) % 7
        note = (c_major[interval] - c_major[mode] + key) % 12
        print(get_note_name(note))

def get_note_name(value, flats=True):
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
def get_mode_name(value):
    value %= 7
    if value == 0:
        return 'Ionian'
    elif value == 1:
        return 'Dorian'
    elif value == 2:
        return 'Phrygian'
    elif value == 3:
        return 'Lydian'
    elif value == 4:
        return 'Mixolydian'
    elif value == 5:
        return 'Aeolian'
    elif value == 6:
        return 'Locrian'

key = random.randrange(0, 12)
mode = random.randrange(0, 7)

print_scale()