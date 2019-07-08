'''
Kaden Archibald
Created: Jun 30, 2019
Revised: , 2019
Version: IPython 7.2.0 (Anaconda distribution) with Python 3.7.1

Module for numerically solving arbitrary complex-valued
functions in a single vairable.
'''

from RealSolver import RealSolver



class ComplexSolver(RealSolver):
    def __init__(self, function, firstGuess, secondGuess):
        
        RealSolver.__init__(self, function, firstGuess, secondGuess)
        
        
        
        

        