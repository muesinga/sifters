# from modules import *

# def main():
#     print(matrix_generators.fibonacci(0, 5))
    
# main()

def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        return lst[i:i + n]
        
print(chunks([1,2,3,4], 5))