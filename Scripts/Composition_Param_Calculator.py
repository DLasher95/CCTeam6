import random
from Scripts import NltkUtil as nl, Instruments as ints, Scale

def calculate_instrument(phrase, debug=False):
    max = 0
    ins = 0
    for i in ints.non_fx_instruments:
        score = nl.score_many_to_many(phrase, ints.instruments[i].split())
        if score > max:
            max = score
            ins = i
    if debug:
        print('Instrument: ' + ints.instruments[ins] + ' (%.2f' % round(max, 2) + ')')
    return ins, max

# return normalized
def calculate_speed_score(words, debug=False):
    slow_score = nl.score_many_to_one(words, 'slow')
    fast_score = nl.score_many_to_one(words, 'fast')

    if debug:
        print('BPM: [%.2f' % round (slow_score, 2) + ', %.2f' % round(fast_score, 2) + ']')
    return normalize_score(slow_score, fast_score)
def calculate_happiness_score(words, debug=False):
    happy_score = nl.score_many_to_one(words, 'happy')
    sad_score = nl.score_many_to_one(words, 'sad')

    if debug:
        print('Happiness: [%.2f' % round(sad_score, 2) + ', %.2f' % round(happy_score, 2) + ']')
    return normalize_score(sad_score, happy_score)
def normalize_score(neg_score, pos_score):
    # send higher value to 1
    # inflate other score by same amount
    # calculate normalized difference
    # divide by 2
    # offset from 0.5
    ratio = 0
    if pos_score > neg_score:
        ratio = 1 / pos_score
    else:
        ratio = 1 / neg_score
    norm_neg = ratio * neg_score
    norm_pos = ratio * pos_score
    normalized_difference = norm_pos - norm_neg
    offset = normalized_difference / 2
    return 0.5 + offset

def mode_by_score(happiness):
    # brightest first
    ranked_modes = [6, 2, 5, 1, 4, 0, 3]
    if happiness < 0 or happiness > 1:
        print('Expected score in range [0,1]')
        return -1

    # multiply by 6 because...
    # score = 1   -> index = 6 (last)
    # score = 0.5 -> index = 3 (middle)
    index = round(happiness * 6)
    return ranked_modes[index]
def bpm_by_score(speed):
    if speed < 0 or speed > 1:
        print('Excpected value in range [0,1]')
        return -1

    bpm_min, bpm_max = 40, 180
    bpm_range = bpm_max - bpm_min
    return bpm_min + round(bpm_range * speed)
def random_score():
    return random.random()

def calculate_params(words, debug=False):
    instrument, max_ins_score = calculate_instrument(words)
    speed_score = calculate_speed_score(words)
    bpm = bpm_by_score(speed_score)
    happiness_score = calculate_happiness_score(words)
    mode = mode_by_score(happiness_score)

    if debug:
        print('[' + ', '.join(w for w in words) + ']')
        print('Happiness: ' + str(happiness_score))
        print('Speed: ' + str(speed_score))
        print('Instrument: ' + str(ints.instruments[instrument]) + ' (' + str(max_ins_score) + ')')
        print('BPM: ' + str(bpm))
        print('Mode: ' + str(mode) + ' (' + str(Scale.get_mode_name(mode)) + ')')

    return instrument, bpm, mode
