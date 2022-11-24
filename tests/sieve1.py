import numpy as np
import re

from music21 import *

def save(stream):
    return stream.write('midi', 'data/track/generated.midi')

def play(midi_file):
    stream = converter.parse(midi_file)
    stream.show('midi')

def intersect(sievs):
    intersection = '|'.join(sievs)
    return intersection

###################################################

def largest_prime_factor(n):
    return next(n // i for i in range(1, n) if n % i == 0 and is_prime(n // i))

def is_prime(m):
    return all(m % i for i in range(2, m - 1))
# https://www.w3resource.com/python-exercises/challenges/1/python-challenges-1-exercise-35.php

###################################################

def parse_modulo(siev):
    if type(siev) == tuple:
        modulo = []
        for siv in siev:
            modulo.append([int(s) for s in re.findall(r'(\d+)@', siv)])
        return modulo
    else:
        modulo = [int(s) for s in re.findall(r'(\d+)@', siev)]
        return modulo

def find_lcm(modulo):
    if type(modulo[0]) == list:
        multiples = []
        for mod in modulo:
            multiples.append(np.lcm.reduce(mod))
        return multiples
    else:
        return np.lcm.reduce(modulo)
    
def find_repeats(period, lcm):
    repeats = []
    for m in lcm:
        repeats.append(int(period/m))
    return repeats

def merge(list1, list2):
    merged_list = [(list1[i], list2[i]) for i in range(0, len(list1))]
    return merged_list
# https://www.geeksforgeeks.org/python-merge-two-lists-into-list-of-tuples/

def normalize_periodicity(sievs):
    mod = parse_modulo(sievs)
    lcm = find_lcm(mod)
    # period if all note length are same
    period = find_lcm(lcm)
    repeats = find_repeats(period, lcm)
    # multi = merge(sivs, repeats)
    # return multi
    return repeats

###################################################

def find_period(siev):
    numbers = [int(s) for s in re.findall(r'(\d+)@', siev)]
    unique_numbers = list(set(numbers))
    product = np.prod(unique_numbers)
    return product

def initialize(siev, rep):
    events = sieve.Sieve(siev)
    period = find_period(siev)
    events.setZRange(0, (rep * period) - 1)
    binary = events.segment(segmentFormat='binary')
    return binary

def assign(pattern, index):
    # method for selecting midi key
    midi_key = [35, 60, 76, 80, 80, 80 ,80]
    note_length = 0.5
    return [pattern, midi_key[index], note_length]

def parse(sievs):
    pattern = []
    i = 0
    rep = normalize_periodicity(sievs)
    for siev in sievs:
        binary = initialize(siev, rep[i])
        assigned_pattern = assign(binary, i)
        pattern.append(assigned_pattern)
        i += 1
    return pattern

###################################################

# to find denominator make dict to assign note length to with denominator
# seperate note length and beat length variables
# to find denominator make dict to assign note length to with denominator
# seperate note length and beat length variables
# denominator = beat length
# method for finding time signature numerator/denominator
# no it has to be note_length = denominator
# how can I use the makeNotation function to 'smooth' out a time signature with its beat

def segment_to_point(measure, segment, midi_key, note_length):
    for point in segment:
        if point == 0:
            measure.append(note.Rest(quarterLength=note_length))
        else:
            measure.append(note.Note(midi=midi_key, quarterLength=note_length))

def generate_measure(segment, midi_key, note_length, numerator, measure_num):
    measure = stream.Measure(number=measure_num)
    if measure_num == 1:
        measure.append(meter.TimeSignature('{n}/{d}'.format(n=numerator, d=8)))
        measure.append(clef.PercussionClef())
        segment_to_point(measure, segment, midi_key, note_length)
        return measure
    else:
        segment_to_point(measure, segment, midi_key, note_length)
        return measure

def generate_part(pattern, midi_key, note_length, id):
    part = stream.Part(id='part{n}'.format(n=id))
    part.append(instrument.UnpitchedPercussion())
    period = len(pattern)
    numerator = largest_prime_factor(period)
    measure_num = 1
    repeat_pattern = 1
    divisor = period/numerator
    split_pattern = np.array_split(pattern, divisor)
    for _ in range(repeat_pattern):
        for segment in split_pattern:
            part.append(generate_measure(segment, midi_key, note_length, numerator, measure_num))
            measure_num += 1
    return part

def generate_score(siev):
    s = stream.Score()
    id = 1
    if len(siev) > 1:
        sievs = parse(siev)
        for siv in sievs:
            pattern, midi_key, note_length = siv[0], siv[1], siv[2]
            s.insert(0, generate_part(pattern, midi_key, note_length, id))
            id += 1
    else:
        print('hello world')
    s.insert(0, metadata.Metadata())
    s.metadata.title = 'Sifters'
    s.metadata.composer = 'Aarib Moosey'
    p1m1 = s.parts[0].measure(1)
    p1m1.insert(0, tempo.MetronomeMark('fast', 144, note.Note(type='half')))
    return s

psappha_sieve = '((8@0|8@1|8@7)&(5@1|5@3))', '((8@0|8@1|8@2)&5@0)', '((8@5|8@6)&(5@2|5@3|5@4))', '(8@6&5@1)', '(8@3)', '(8@4)', '(8@1&5@2)'

if __name__ == '__main__':
    print(parse(psappha_sieve))