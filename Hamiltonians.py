import numpy as np


#site con is for looking at adding a load at a specific site along with the input and output.
def oned_h(structure ,N , inpt=None, oupt=None,  A=(1/50), B=(1/93), C=(1/75) , Zin=(1/50), Zout=(1/50), looped=False, site_con = False, site = 0, Zsite = 1/50, return_H=True):
    if looped == False: 
        M = np.zeros((N+1,N+1), dtype = complex)
        for i, val in enumerate(structure[-1]):
            M[i,i+1] = A if val == 'A' else (B if val == 'B' else C)
            M[i+1,i] = A if val == 'A' else (B if val == 'B' else C)
            
        if not return_H:
            return M, None

        H = np.zeros((N+1,N+1), dtype = complex)
        for i in range(N):
            i=int(i)
            # if i>0 and i<N-1: 
            #     H[i,i+1] = M[i,i+1]/(np.sqrt(M[i+1,i+2]+M[i+1,i])*np.sqrt(M[i,i+1]+M[i,i-1]))
            #     H[i+1,i] = H[i,i+1]
            # elif i==0:
            #     H[i,i+1] = M[i,i+1]/(np.sqrt(M[i+1,i+2]+M[i+1,i])*np.sqrt(M[i,i+1]))
            #     H[i+1,i] = H[i,i+1]
            # elif i==N-1:
            #     H[i,i+1] = M[i,i+1]/(np.sqrt(M[i,i+1])*np.sqrt(M[i+1,i]+M[i,i-1]))
            #     H[i+1,i] = H[i,i+1]
            H[i,i+1] = M[i,i+1]/( np.sqrt(sum(M[i+1,:])) * np.sqrt(sum(M[:,i])) )
            H[i+1,i] = H[i,i+1]
                
        if inpt != None:
            if inpt == 0:     
                H[inpt,inpt] = 1j * Zin / (np.sqrt(M[inpt,inpt+1]))**2
            elif inpt == N:
                H[inpt,inpt] = 1j * Zin / (np.sqrt(M[inpt,inpt-1]))**2
            elif inpt == N-1:
                H[inpt,inpt] = 1j * Zin / (np.sqrt(M[inpt,inpt-1]+M[inpt,inpt+1])*np.sqrt(M[inpt+1,inpt]))
            else:
                H[inpt,inpt] = 1j * Zin / (np.sqrt(M[inpt,inpt-1]+M[inpt,inpt+1])*np.sqrt(M[inpt+1,inpt+2]+M[inpt+1,inpt]))
        
                
        if oupt != None:      
            if oupt == 0:     
                H[oupt,oupt] = 1j * Zout / (np.sqrt(M[oupt,oupt+1]))**2
            elif oupt == N:
                H[oupt,oupt] = 1j * Zout / (np.sqrt(M[oupt,oupt-1]))**2
            elif oupt == N-1:
                H[oupt,oupt] = 1j * Zout / (np.sqrt(M[oupt,oupt-1]+M[oupt,oupt+1])*np.sqrt(M[oupt+1,oupt]))
            else:
                H[oupt,oupt] = 1j * Zout / (np.sqrt(M[oupt,oupt-1]+M[oupt,oupt+1])*np.sqrt(M[oupt+1,oupt+2]+M[oupt+1,oupt]))
                
        if site_con == True:
            if site == 0:     
                H[site,site] = 1j * Zsite / (np.sqrt(M[site,site+1]))**2
            elif site == N:
                H[site,site] = 1j * Zsite / (np.sqrt(M[site,site-1]))**2
            elif site == N-1:
                H[site,site] = 1j * Zsite / (np.sqrt(M[site,site-1]+M[site,site+1])*np.sqrt(M[site+1,site]))
            else:
                H[site,site] = 1j * Zsite / (np.sqrt(M[site,site-1]+M[site,site+1])*np.sqrt(M[site+1,site+2]+M[site+1,site]))
   
    else:
        M = np.zeros((N,N), dtype = complex)
        
        for i, val in enumerate(structure[-1]):
            if i == N-1:
                M[i,0] = A if val == 'A' else (B if val == 'B' else C)
                M[0,i] = A if val == 'A' else (B if val == 'B' else C)
            else:
                M[i,i+1] = A if val == 'A' else (B if val == 'B' else C)
                M[i+1,i] = A if val == 'A' else (B if val == 'B' else C)
        if not return_H:
            return M, None

        
        H = np.zeros((N,N), dtype = complex)
        for i in range(N):
            i=int(i)
        
            # if i>0 and i<N-2: 
            #     H[i,i+1] = M[i,i+1]/(np.sqrt(M[i+1,i+2]+M[i+1,i])*np.sqrt(M[i,i+1]+M[i,i-1]))
            #     H[i+1,i] = H[i,i+1]
            # elif i==0:
            #     H[i,i+1] = M[i,i+1]/(np.sqrt(M[i+1,i+2]+M[i+1,i])*np.sqrt(M[i,i+1]+M[i,N-1]))
            #     H[i+1,i] = H[i,i+1]
            # elif i==N-2:
            #     H[i,i+1] = M[i,i+1]/(np.sqrt(M[i,i+1]+M[i+1,0])*np.sqrt(M[i+1,i]+M[i,i-1]))
            #     H[i+1,i] = H[i,i+1]
            # elif i==N-1:
            #     H[i,0] = M[i,0]/(np.sqrt(M[0,1]+M[0,i])*np.sqrt(M[i,0]+M[i,i-1]))
            #     H[0,i] = H[i,0]
            if i==N-1:
                H[i,0] = M[i,0]/( np.sqrt(sum(M[i,:])) * np.sqrt(sum(M[:,i])) )
                H[0,i] = H[i,0]
            else:    
                H[i,i+1] = M[i,i+1]/( np.sqrt(sum(M[i+1,:])) * np.sqrt(sum(M[:,i])) )
                H[i+1,i] = H[i,i+1]
            
            if inpt is not None:
                if inpt == 0:
                    H[inpt, inpt] = 1j * Zin / (np.sqrt(M[inpt, (inpt + 1) % N]))**2
                elif inpt == N - 1:
                    H[inpt, inpt] = 1j * Zin / (np.sqrt(M[inpt, (inpt - 1) % N] + M[inpt, (inpt + 1) % N]) * np.sqrt(M[(inpt + 1) % N, inpt]))
                else:
                    H[inpt, inpt] = 1j * Zin / (np.sqrt(M[inpt, (inpt - 1) % N] + M[inpt, (inpt + 1) % N]) * np.sqrt(M[(inpt + 1) % N, (inpt + 2) % N] + M[(inpt + 1) % N, inpt]))
            
            if oupt is not None:
                if oupt == 0:
                    H[oupt, oupt] = 1j * Zout / (np.sqrt(M[oupt, (oupt + 1) % N]))**2
                elif oupt == N - 1:
                    H[oupt, oupt] = 1j * Zout / (np.sqrt(M[oupt, (oupt - 1) % N] + M[oupt, (oupt + 1) % N]) * np.sqrt(M[(oupt + 1) % N, oupt]))
                else:
                    H[oupt, oupt] = 1j * Zout / (np.sqrt(M[oupt, (oupt - 1) % N] + M[oupt, (oupt + 1) % N]) * np.sqrt(M[(oupt + 1) % N, (oupt + 2) % N] + M[(oupt + 1) % N, oupt]))

            if site_con == True:
                if site == 0:
                    H[site, site] = 1j * Zsite / (np.sqrt(M[site, (site + 1) % N]))**2
                elif site == N - 1:
                    H[site, site] = 1j * Zsite / (np.sqrt(M[site, (site - 1) % N] + M[site, (site + 1) % N]) * np.sqrt(M[(site + 1) % N, site]))
                else:
                    H[site, site] = 1j * Zsite / (np.sqrt(M[site, (site - 1) % N] + M[site, (site + 1) % N]) * np.sqrt(M[(site + 1) % N, (site + 2) % N] + M[(site + 1) % N, site]))
            
    
    return M, H

def bdg_h_l(i, N, u, t, d):
    Hbdg = np.zeros((N, N))
    while i < N:
        i = int(i)
        ipos = int((i/2))   #nth term
        ineg = int((i/2)-1) #n-1 term
        if i==0:
            sig_n = (abs(u) + abs(t[ipos]) + abs(d[ipos]))**(-1/2)
            sig_n1 = (abs(u) + abs(t[ipos]) + abs(t[ipos+1]) + abs(d[ipos])+ abs(d[ipos+1]))**(-1/2)
            sig_neg = 0
        elif i==N-4:
            sig_n = (abs(u) + abs(t[ineg]) + abs(t[ipos]) + abs(d[ineg]) + abs(d[ipos]))**(-1/2)
            sig_n1 = (abs(t[ipos]) + abs(d[ipos]))**(-1/2)
            sig_neg = (abs(u) + abs(t[ineg-1]) + abs(t[ineg]) + abs(d[ineg-1]) + abs(d[ineg]))**(-1/2)
            
        elif i==N-2:
            sig_n = (abs(u) + abs(t[ineg]) + abs(d[ineg]))**(-1/2)
            sig_n1 = 0
            sig_neg = (abs(u) + abs(t[ineg-1]) + abs(t[ineg]) + abs(d[ineg-1]) + abs(d[ineg]))**(-1/2)
        else:
            sig_n = (abs(u) + abs(t[ineg]) + abs(t[ipos]) + abs(d[ineg]) + abs(d[ipos]))**(-1/2)
            sig_n1 = (abs(u) + abs(t[ipos]) + abs(t[ipos+1]) + abs(d[ipos])+ abs(d[ipos+1]))**(-1/2)
            sig_neg = (abs(u) + abs(t[ineg-1]) + abs(t[ineg]) + abs(d[ineg-1]) + abs(d[ineg]))**(-1/2)
            
            
            
            
        Hbdg[i, i] = sig_n*u*sig_n
        Hbdg[i+1, i+1] = -1*sig_n*u*sig_n
    
        if i+3 <= N:
            Hbdg[i, i+2] = sig_n*t[ipos]*sig_n1          #first row 3rd column ...
            Hbdg[i+1, i+3] = -1*sig_n*t[ipos]*sig_n1
    
            Hbdg[i, i+3] = sig_n*d[ipos]*sig_n1
            Hbdg[i+1, i+2] = -1*sig_n*d[ipos]*sig_n1
        if i-2 >= 0:
            Hbdg[i, i-2] = sig_n*t[ineg]*sig_neg
            Hbdg[i+1, i-1] = -1*sig_n*t[ineg]*sig_neg
    
            Hbdg[i, i-1] = -1*sig_n*d[ineg]*sig_neg
            Hbdg[i+1, i-2] = sig_n*d[ineg]*sig_neg
    
        i += 2
    
    return Hbdg

def bdg_h( N, u, t, d):
    Hbdg = np.zeros((N, N))
    i=0
    while i < N:
        i = int(i)
        if i==0:
            sig_n = (abs(u) + abs(t) + abs(d))**(-1/2)
            sig_n1 = (abs(u) + abs(t) + abs(t) + abs(d)+ abs(d))**(-1/2)
            sig_neg = 0
        elif i==N-4:
            sig_n = (abs(u) + abs(t) + abs(t) + abs(d) + abs(d))**(-1/2)
            sig_n1 = (abs(t) + abs(d))**(-1/2)
            sig_neg = (abs(u) + abs(t) + abs(t) + abs(d) + abs(d))**(-1/2)
            
        elif i==N-2:
            sig_n = (abs(u) + abs(t) + abs(d))**(-1/2)
            sig_n1 = 0
            sig_neg = (abs(u) + abs(t) + abs(t) + abs(d) + abs(d))**(-1/2)
        else:
            sig_n = (abs(u) + abs(t) + abs(t) + abs(d) + abs(d))**(-1/2)
            sig_n1 = (abs(u) + abs(t) + abs(t) + abs(d)+ abs(d))**(-1/2)
            sig_neg = (abs(u) + abs(t) + abs(t) + abs(d) + abs(d))**(-1/2)
            
            
            
            
        Hbdg[i, i] = sig_n*u*sig_n
        Hbdg[i+1, i+1] = -1*sig_n*u*sig_n
    
        if i+3 <= N:
            Hbdg[i, i+2] = sig_n*t*sig_n1          #first row 3rd column ...
            Hbdg[i+1, i+3] = -1*sig_n*t*sig_n1
    
            Hbdg[i, i+3] = sig_n*d*sig_n1
            Hbdg[i+1, i+2] = -1*sig_n*d*sig_n1
        if i-2 >= 0:
            Hbdg[i, i-2] = sig_n*t*sig_neg
            Hbdg[i+1, i-1] = -1*sig_n*t*sig_neg
    
            Hbdg[i, i-1] = -1*sig_n*d*sig_neg
            Hbdg[i+1, i-2] = sig_n*d*sig_neg
    
        i += 2
    
    return Hbdg


def H_Graphene(n, m): #creates the basic adjacency matrix for graphene with n rows and m columns 
    total_atoms = n * m
    
    adjacency_matrix = np.zeros((total_atoms, total_atoms), dtype=float)
    
    def get_index(i, j):
        return i * m + j

    for i in range(n):
        for j in range(m):
            current_index = get_index(i, j)
            if (i + j) % 2 == 0:
                neighbors = [(i, j + 1), (i + 1, j), (i, j - 1)]
            else:
                neighbors = [(i - 1, j), (i, j + 1), (i, j - 1)]
                

            for ni, nj in neighbors:
                if 0 <= ni < n and 0 <= nj < m:
                    neighbor_index = get_index(ni, nj)
                    adjacency_matrix[current_index][neighbor_index] = 1/50
                    adjacency_matrix[neighbor_index][current_index] = 1/50
    
    A = adjacency_matrix
    
    H = np.zeros((total_atoms, total_atoms), dtype=complex)
    scaling_matrix = np.zeros((total_atoms, total_atoms), dtype=float)
    for i in range(len(A[:,0])):
        for j in range(len(A[0,:])):
            denom = np.sqrt(sum(A[i, :])) * np.sqrt(sum(A[:, j]))
            if denom != 0:
                H[i, j] = A[i, j] / denom
                scaling_matrix[i,j] = denom
                
            else:
                H[i, j] = 0.0
                
    return H, scaling_matrix