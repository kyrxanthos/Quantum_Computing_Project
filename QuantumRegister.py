# -*- coding: utf-8 -*-
"""
Created on Thu Feb  4 15:54:14 2021

@author: mikva
"""
import numpy as np
import sparse


class QuantumRegister:
    def __init__(self, n):
        """
        Initializes the quantum register of length n. Creates a list of default qubits
        in state |0> and initializes the wavevector which describes the register

        Parameters
        ----------
        n : int
            length of register

        Returns
        -------
        None.

        """
        Qbits = []

        for i in range(n): 
            Qbits.append(Qubit())
        self.Qbits = np.array(Qbits)
        self.initialize()        

    def __str__(self):        
        toPrint = ''

        toPrint += '\n'
        for i in range(self.Statevec.Elements.size):
            toPrint += f'|{i}> = {((self.Statevec.Elements[i])*np.conj(self.Statevec.Elements[i])).real}\n'
        
        return toPrint
    
    def initialize(self):
        """
        Sets the statevector according to the current state of qubits

        Returns
        -------
        None.

        """
        self.Statevec = sparse.Vector(np.array([1], dtype=complex))
        for qbit in self.Qbits[::-1]:
            self.Statevec = self.Statevec.outer(qbit.vals)
            
    def setStateVec(self, newVec):
        """
        Allows the user to set the state vector to a new vector. Automatically normalises the vector.
        
        Parameters
        ----------
        newVec : list or array
            The new vector to become the state vector.

        Returns
        -------
        None.

        """
        newVec = np.array(newVec, dtype=complex)
        assert self.Statevec.Dimension == newVec.size, 'Wrong dimensions for new statevector'
        normal_const = np.sqrt((newVec*newVec.conj()).sum())
        self.Statevec = sparse.Vector(newVec/normal_const)
        
    def setQbits(self, qbits, vals):
        """
        Sets the initial values of the qubits if required,
        although it is preferred to use gates for this step.
        Automatically normalizes the Qbit

        Parameters
        ----------
        qbits : array_like
            qubits to be set
        vals : array_like, each entry containing two values
            The values that the qubits should be set to.

        Returns
        -------
        None.

        """
        
        for qbit in qbits:
            self.Qbits[qbit].vals = sparse.Vector(np.array(vals[qbit]) / np.linalg.norm(vals[qbit]))
        self.initialize()

    def measure(self):
        """
        Attempts to measure the current statevector in terms of individual qubits
        Pretty sure it's impossible. Not because it's difficult, but because of entanglement
        and stupid imaginary numbers.

        Returns
        -------
        None.

        """
        for qbit in self.Qbits:
            qbit.vals.Elements[1] = 0+0j
        for i, value in enumerate(self.Statevec.Elements):
            for j, qbit in enumerate(self.Qbits):
                if ((i>>(j)) & 1) == 1:
                    #print(i,j,value)
                    qbit.vals.Elements[1] += value*value.conj()
        for qbit in self.Qbits:
            qbit.vals.Elements[0] = complex(1 - qbit.vals.Elements[1])
            qbit.normalize()
            #print(qbit)
            
class Qubit:
    def __init__(self):
        self.vals = sparse.Vector(np.array([1.+0.j, 0.+0.j]))
    
    def normalize(self):
        #print(self.vals.Elements)
        self.vals.Elements = self.vals.Elements / np.sqrt((self.vals.Elements*self.vals.Elements.conj()).sum())
    
    def get0(self):
        return self.vals.Elements[0]
    
    def get1(self):
        return self.vals.Elements[1]
    
    def __str__(self):
        toPrint = ''
        toPrint += f'|0> = {self.vals.Elements[0]} \n'
        toPrint += f'|1> = {self.vals.Elements[1]} \n'
        
        return toPrint
        

if __name__ == '__main__':
    qr = QuantumRegister(3)
    qr.setQbits([0], [[0,1]])
    print(qr.Qbits[0])
    print(qr.Statevec)
    qr.measure()
    
    #cr = ClassicalRegister(3)
    