fund = 1
length = 12

def generate_fibonacci_sequence(fund, length):
    i = 0
    y = fund
    arr = []
    for _ in range(length):
        arr.append(i)
        i, y = y, i + y
    return arr
    # print(r)
    # print(range)

printgenerate_fibonacci_sequence(fund, length)

# for i in range(10):
#     print(1)
# print()