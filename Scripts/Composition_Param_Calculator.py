import random
import numpy as np
from Scripts import NltkUtil as nl, Instruments as insts, Scale

def calculate_params(words, debug=False):
    speed_score = calculate_speed_score(words)
    happiness_score = calculate_happiness_score(words)
    complexity_score = calculate_complexity_score(words)
    pitch_score = calculate_pitch_score(words)

    num_instruments = num_instruments_by_complexity(complexity_score)
    instruments, inst_debug = pick_instruments(words, num_instruments=num_instruments, print_selected=debug)
    range_min, range_max = range_by_pitch_and_complexity(pitch_score, complexity_score)

    bpm = bpm_by_score(speed_score)
    mode = mode_by_score(happiness_score)

    if debug:
        print('[' + ', '.join(w for w in words) + ']')
        print(inst_debug)
        print('Happiness score:  ' + str(happiness_score))
        print('Speed score:      ' + str(speed_score))
        print('Complexity score: ' + str(complexity_score))
        print('Pitch score:      ' + str(pitch_score))
        print('BPM: ' + str(bpm))
        print('Mode: ' + str(mode) + ' (' + str(Scale.get_mode_name(mode)) + ')')
        print('Range: ' + str(range_min) + ' - ' + str(range_max))

    return instruments, bpm, mode

def pick_instruments(phrase, num_instruments, selection_range=15, debug=False, print_selected=False):
    sorted_instrument_scores = rate_instruments(phrase=phrase, debug=debug)
    keys = list(sorted_instrument_scores.keys())
    top_keys = keys[:selection_range]

    if debug:
        print("Top " + str(selection_range) + " instruments: ")
        for k in top_keys:
            pad_len = 30
            this_pad = pad_len - len(insts.instruments[k])
            pad = ' ' * this_pad
            print(insts.instruments[k] + ': ' + pad + str(sorted_instrument_scores[k]))

    # https://docs.scipy.org/doc/numpy-1.13.0/reference/generated/numpy.random.permutation.html
    ret_instruments = np.random.permutation(top_keys)[:num_instruments]

    # adds a string with selected instruments and scores to return
    selected_str = 'Selected instruments: ' + str(num_instruments) + '\n'
    for k in ret_instruments:
        pad_len = 30
        this_pad = pad_len - len(insts.instruments[k])
        pad = ' ' * this_pad
        selected_str += insts.instruments[k] + ': ' + pad + str(sorted_instrument_scores[k]) \
                        + ('\n' if k != ret_instruments[-1] else '')

    return ret_instruments, selected_str
def rate_instruments(phrase, debug=False, debug_len=10):
    scores = {}
    # score each instrument
    for i, inst in enumerate(insts.melodic_instruments):
        score = nl.score_many_to_many(phrase, insts.instruments[i].split())
        scores[i] = score

    # https://stackoverflow.com/questions/613183/how-do-i-sort-a-dictionary-by-value
    sorted_scores = {k: v for k, v in sorted(scores.items(), key=lambda item: item[1], reverse=True)}

    # prints 'most relevant' [10] instruments and their scores
    if debug:
        print("Scores")
        count = 0
        for k in sorted_scores:
            if count >= debug_len:
                break
            pad_len = 30
            this_pad = pad_len - len(insts.instruments[k])
            pad = ' ' * this_pad
            print(insts.instruments[k] + ': ' + pad + str(sorted_scores[k]))
            count += 1

    return sorted_scores

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
def calculate_complexity_score(words, debug=False):
    complex_score = nl.score_many_to_one(words, 'complex')
    simple_score = nl.score_many_to_one(words, 'simple')
    if debug:
        print('Complexity: [%.2f' % round(simple_score, 2) + ', %.2f' % round(complex_score, 2) + ']')
    return normalize_score(simple_score, complex_score)
def calculate_pitch_score(words, debug=False):
    high_score = nl.score_many_to_one(words, 'high')
    low_score = nl.score_many_to_one(words, 'low')
    if debug:
        print('Complexity: [%.2f' % round(low_score, 2) + ', %.2f' % round(high_score, 2) + ']')
    return normalize_score(low_score, high_score)
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

# methods define min and max params
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
def num_instruments_by_complexity(complexity):
    min_instruments = 1
    max_instruments = 5
    diff = max_instruments - min_instruments
    diff *= complexity
    diff = round(diff)
    # print('NUM: ' + str(min_instruments + diff))
    return min_instruments + diff
def range_by_pitch_and_complexity(pitch, complexity):
    MIN_PITCH = 20
    MAX_PITCH = 100
    max_range = MAX_PITCH - MIN_PITCH
    pitch_center = MIN_PITCH + round(pitch * max_range)
    pitch_range = round(max_range * complexity)

    # may be negative
    ret_min = pitch_center - pitch_range // 2
    ret_max = pitch_center + pitch_range // 2

    # adjust range to fit between MIN and MAX pitch
    # theoretically these shouldn't both be true...
    if ret_min < MIN_PITCH:
        diff = MIN_PITCH - ret_min
        ret_min += diff
        ret_max += diff
    elif ret_max > MAX_PITCH:
        diff = ret_max - MAX_PITCH
        ret_max -= diff
        ret_min -= diff
    return ret_min, ret_max

def random_score():
    return random.random()


