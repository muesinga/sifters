import numpy as np

x = np.empty([2,2])

print(x)

# x = [1,2,4,5,5]
# y = [3,4]
# print(x.extend(y))
# print(x)

# row = [1,2,3,4]

# def generateSerialMatrix(row):
#     interval = []
#     columns = []
#     matrix = []
#     for tone in row:
#         x = [1,23]
#         interval.append(tone - row[0])
#         np.concatenate(columns,  x)
#     # print(columns)
        
# generateSerialMatrix(row)

# a = np.array([[1, 2], [3, 4]])
# b = np.array([[5, 6]])
# np.concatenate((a, b), axis=0)
# # array([[1, 2],
# #        [3, 4],
# #        [5, 6]])
# np.concatenate((a, b.T), axis=1)
# # array([[1, 2, 5],
# #        [3, 4, 6]])
# c = np.concatenate((a, b), axis=None)
# # array([1, 2, 3, 4, 5, 6])

# print(c)