'''

File: tetris.py
Author: Hadayat Seddiqi
Date: 4.5.13
Description: Recognize tetris pieces with a quantum Hopfield network.

'''

import scipy as sp

nQubits = 9
T = 10.0
#T = sp.arange(2,23,4.0) # Output a sequence of anneal times
dt = 0.01

# Output parameters
output = 1 # Turn on/off all output except final probabilities
eigspecdat = 0 # Output data for eigspec
eigspecplot = 0 # Plot eigspec
eigspecnum = 2**nQubits # Number of eigenvalues
fidelplot = 0 # Plot fidelity
fideldat = 0 # Output fidelity data
fidelnumstates = 2**nQubits # Check fidelity with this number of eigenstates
overlapdat = 0 # Output overlap data
overlapplot = 0 # Plot overlap
outputdir = 'data/hopfield/tetris' # In relation to run.py
probout = 1 # Calculate final state probabilities

errchk = 0 # Error-checking on/off
eps = 0.01 # Numerical error in normalization condition (1 - norm < eps)

# Specify a QUBO (convert to Ising = True), or alpha, beta directly 
# (convert = False), and also specify the signs on the Ising Hamiltonian 
# terms (you can specify coefficients too for some problems if needed)
isingConvert = 0
isingSigns = {'hx': -1, 'hz': -1, 'hzz': -1}

neurons = nQubits
memories = [ [ 1, 1, 1, 1,   1,-1,-1, 1,   1,-1,-1, 1 ],  # Block
             [ 1, 1, 1,-1,   1,-1,-1,-1,   1, 1, 1, 1 ],  # L
             [ 1, 1, 1, 1,  -1, 1, 1, 1,  -1,-1,-1, 1 ],  # Reverse-L
             [ 1,-1, 1, 1,   1,-1,-1, 1,   1, 1,-1, 1 ],  # S
             [ 1, 1,-1, 1,   1,-1,-1, 1,   1,-1, 1, 1 ],  # Z
             [ 1, 1, 1, 1,  -1,-1,-1,-1,   1, 1, 1, 1 ] ] # Long

memories = [ [ 1, 1, 1,   1,-1,-1,   1,-1,-1 ],  # Block
             [ 1,-1, 1,   1,-1,-1,   1, 1,-1 ],  # S
             [ 1,-1, 1,  -1,-1, 1,  -1, 1, 1 ],  # Z
             [ 1, 1,-1,  -1,-1,-1,   1, 1, 1 ],  # L
             [ 1, 1, 1,  -1, 1, 1,  -1,-1,-1 ] ] # Anti-L

inputstate = [1,1,1,1,  1,-1,-1,-1,  1,-1,-1,1] # Almost a block

inputstate = [1,1,1,  -1,-1,-1,  1,-1,-1] # Almost a block

# This is gamma, the appropriate weighting on the input vector
isingSigns['hz'] *= 1 - (len(inputstate) - inputstate.count(0))/(2*neurons)

alpha = sp.array(inputstate)
beta = sp.zeros((neurons,neurons))
delta = sp.array([])

# Construct pattern matrix
for i in range(neurons):
    for j in range(neurons):
        for p in range(len(memories)):
            beta[i,j] += ( memories[p][i]*memories[p][j] -
                           len(memories)*(i == j) )

beta = sp.triu(beta)/float(neurons)
print beta