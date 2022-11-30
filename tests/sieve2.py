import numpy as np
import re

from music21 import *

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
    # if type(siev) == list:
    modulo = []
    for siv in siev:
        modulo.append([int(s) for s in re.findall(r'(\d+)@', siv)])
    return modulo
    # else:
    #     modulo = [int(s) for s in re.findall(r'(\d+)@', siev)]
    # return modulo

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
    note_length = 0.25
    return [pattern, midi_key[index], note_length]

def parse(sievs):
    pattern = []
    # if len(sievs) > 1:
    i = 0
    rep = normalize_periodicity(sievs)
    if len(sievs) > 1:
        for siev in sievs:
            binary = initialize(siev, rep[i])
            assigned_pattern = assign(binary, i)
            pattern.append(assigned_pattern)
            pattern = assigned_pattern
            i += 1
    else:
        print('hello world')
        # binary = initialize(sievs, rep)
        # pattern = assign(binary, i)
    # return pattern

###################################################

def generate_part(pattern, midi_key, note_length, id):
    part = stream.Part(id='part{n}'.format(n=id))
    part.append(instrument.UnpitchedPercussion())
    period, repeat_pattern = len(pattern), 1
    numerator, denominator = largest_prime_factor(period), 4
    i = 0
    if id == 1:
            part.append(tempo.MetronomeMark('fast', 144, note.Note(type='quarter')))
    for _ in range(repeat_pattern):
        for point in pattern:
            if point == 1:
                part.insert(i*note_length, note.Note(midi=midi_key, quarterLength=note_length))
            i += 1
    part.insert(0, meter.TimeSignature('{n}/{d}'.format(n=numerator, d=denominator)))
    part.insert(0, clef.PercussionClef())
    part.makeMeasures(inPlace=True)
    part.makeRests(fillGaps=True, inPlace=True)
    return part

def generate_score(siev):
    s = stream.Score()
    id = 1
    sievs = parse(siev)
    for siv in sievs:
        pattern, midi_key, note_length = siv[0], siv[1], siv[2]
        s.insert(0, generate_part(pattern, midi_key, note_length, id))
        id += 1
    s.insert(0, metadata.Metadata())
    s.metadata.title = 'Sifters'
    s.metadata.composer = 'Aarib Moosey'
    return s

###################################################

psappha_sieve = ['((8@0|8@1|8@7)&(5@1|5@3))']

if __name__ == '__main__':
    # composition = generate_score(psappha_sieve)
    # composition.show()
    res = parse(psappha_sieve)
    print(res)