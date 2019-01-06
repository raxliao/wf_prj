import numpy as np
def generate_design_matrix(x1,y1,z1):
    A = np.zeros((3,7))

    A[0,0] = 1
    A[0,1] = 0
    A[0,2] = 0
    A[0,3] = x1
    A[0,4] = 0
    A[0,5] = z1
    A[0,6] = -1*y1

    A[1, 0] = 0
    A[1, 1] = 1
    A[1, 2] = 0
    A[1, 3] = y1
    A[1, 4] = z1
    A[1, 5] = 0
    A[1, 6] = -1 * x1

    A[2, 0] = 0
    A[2, 1] = 0
    A[2, 2] = 1
    A[2, 3] = z1
    A[2, 4] = -1*y1
    A[2, 5] = x1
    A[2, 6] = 0

    return A