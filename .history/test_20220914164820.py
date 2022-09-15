import numpy as np

row = [1,2,3,4]

def generateSerialMatrix(row):
    interval = []
    columns = []
    matrix = []
    for tone in row:
        x = (tone - row[0])
        interval.append(x)
        columns.append([row[tone] * len(row))
    for trans in columns:
        print(trans)
        
generateSerialMatrix(row)