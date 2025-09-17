import numpy as np


#dim 2 Redheffer Scattering star product

def s(A, B):
    if A.shape != B.shape:
        raise ValueError("Invalid Operation: Matrices A and B are different shapes!")
    
    if A[1, 1] * B[0, 0] == 1:
        raise ValueError("Invalid Operation: Math Error - Division by zero (A[1,1] * B[0,0] = 1).")
    
    try:
        G = 1 / (1 - A[1, 1] * B[0, 0])
        S11 = A[0, 0] + A[0, 1] * G * A[1, 0] * B[0, 0]
        S12 = A[0, 1] * G * B[0, 1]
        S21 = A[1, 0] * G * B[1, 0]
        S22 = B[1, 1] + B[1, 0] * G * A[1, 1] * B[0, 1]
        
        S = np.array([[S11, S12], [S21, S22]])
        return S
    
    except Exception as e:
        raise RuntimeError(f"An unexpected error occurred: {e}")


    
        





#TESTING AREA - MAKE SURE THIS COMMENTED OUT BEFORE SAVING MODULE#

# A = np.identity(2)
# B = np.identity(2)
# A[1,1] = 2
# A[0,1] = 0.6
# B[0,1] = 0.4

    
# S = D2_RHStar(A, B)