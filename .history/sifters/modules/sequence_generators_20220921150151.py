def fibonacci(fund, length):
    i = 0
    y = fund
    seq = []
    # What if fund = 0
    for _ in range(length):
        seq.append(i)
        i, y = y, i + y
    return seq

def midi_to_freq(matrix):
    freq = []
    for row in matrix:
        for tone in row:
            