def generate_fibonacci_matrix(fund, length):
    matrix = []
    seq = []
    if fund == 0:
        i = 1
        for _ in range(length):
            seq.append