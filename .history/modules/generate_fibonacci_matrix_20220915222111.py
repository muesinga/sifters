def generate_fibonacci_matrix(fund, length):
    matrix = []
    seq = []
    y = fund
    if fund == 0:
        i = 1
        for _ in range(length):
            seq.append(y)
            i, y = y, i + y
    else:
        i = fund
        for _ in range(length):
            seq.append(i)
            i, y = y, i + y
    for y in seq:
        x = []
        if y == 0:
            i = 1
            for _ in range(length):
                x.append(y)
                y, i = i, y + i
        else:
            i = 0
            for _ in range(length):
                
    print(seq)

generate_fibonacci_matrix(0, 5)