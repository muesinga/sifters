import numpy as np

row = [1,2,3,4]

def generateSerialMatrix(row):
    interval = []
    columns = []
    matrix = []
    for tone in row:
        interval.append(tone - row[0])
        columns.concatenate(np.array(10))
    print(columns)
        
generateSerialMatrix(row)