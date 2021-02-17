'''
Quantum Computing Project
Author: Petros Zantis

The following class, Entangled, ...
'''
import numpy as np
from BasisStates import BasisStates

class Entangled(object):
    
    '''
    Below is the constructor of the class, ...
    '''
    def __init__(self, matrix) :  # for now uses TensorProduct class, maybe merge later
        
        self.vector = matrix
        
        # check that sum of abs squared of elements is 1
    
    '''
    maybe getters and setters here 
    + modulus checker (always ==1)
    '''
        
    def apply_gate(self, gate):    
        
        assert(gate.qbitdim == 2)   # ensure that its a double qubit gate
        print(f"\nApplying the {gate.name} gate to state\n{self.vector}:\n")
        new = gate.operator.dot(self.vector)
        self.vector = new
