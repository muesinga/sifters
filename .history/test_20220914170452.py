import numpy as np

row = [1,2,3,4]

def generateSerialMatrix(row):
    interval = []
    columns = []
    matrix = []
    for tone in row:
        x = (tone - row[0])
        interval.append(x)
        columns.append([(row[0] + (row[0] - tone))] * len(row))
    # for trans in columns:
    #     x = np.add(trans, columns)
    #     matrix.append(x)
    print(np.add(tr))
generateSerialMatrix(row)