import numpy as np

# from modules import *

# def main():
#     print(matrix_generators.fibonacci(0, 5))
    
# main()
a_list = [1, 2, 3, 4, 5, 6, 7, 8, 9]
our_array = np.array(a_list)
# Split a Python List into Chunks using For Loops
chunked_list = [list(array) for array in np.array_split(np.array(our_list), 3)]
print(chunked_list)

# Returns: [[1, 2, 3], [4, 5, 6], [7, 8, 9]]