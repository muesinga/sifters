import numpy as np

row = [1,2,3,4]

def generateSerialMatrix(row):
    interval = []
    columns = []
    matrix = []
    for tone in row:
        interval.append(tone - row[0])
        np.concatenate(columns, interval, axis)
    print(columns)
        
generateSerialMatrix(row)