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

def n_dim_scatter_junction(n, w, Z=50, Z0=50):
    d1 = range(n)
    d2=d1
    
    Ga = ( Z * np.cos(w) + 1j * Z0 * np.sin(w) ) /  ( Z * np.cos(w) - 1j * Z0 * np.sin(w) )
    Gb = ( Z0 * np.cos(w) + 1j * Z * np.sin(w) ) /  ( Z0 * np.cos(w) - 1j * Z * np.sin(w) )
    b_list = []
    
    for i in d1:
        b = np.zeros(n, dtype=complex)
        for j in d2:
            if j == i:
                b[j] = ( Ga + (1-n) * Gb ) / (n) 
            else:
                b[j] = ( Ga + Gb ) / (n)
        
        b_list.append(b)
        
    return np.array(b_list)




#TESTING AREA - MAKE SURE THIS COMMENTED OUT BEFORE SAVING MODULE#

# A = np.identity(2)
# B = np.identity(2)
# A[1,1] = 2
# A[0,1] = 0.6
# B[0,1] = 0.4

    
# S = D2_RHStar(A, B)

# S, debug = n_dim_scatter_junction(3,np.pi/3)