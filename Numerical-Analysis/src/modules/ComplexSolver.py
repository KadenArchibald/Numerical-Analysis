'''
Kaden Archibald
Created: Jun 30, 2019
Revised: , 2019
Version: IPython 7.2.0 (Anaconda distribution) with Python 3.7.1

Module for numerically solving arbitrary complex-valued
functions in a single vairable.
'''

import const
from RealSolver import RealSolver


''' Driver function to hide object intialization from end programmer. '''
def complexSolver(function, firstGuess, secondGuess = None):
    
    temp = ComplexSolver(function, firstGuess, secondGuess)
    temp.findRoot(temp.complexMethods)
    return (temp.root, temp.conjugate)


class ComplexSolver(RealSolver):
    def __init__(self, function, firstGuess, secondGuess = None):
        
        super().__init__(function, firstGuess, secondGuess)
        
        self.complexMethods = [self.muller, self.bairstow]
        
        # Specific fields for derived class
        self.scaleFactor = 0.1
        self.conjugate = None
        
    
    def findRoot(self, methodList = []):
        
        if not methodList:
            methodList = self.complexMethods
        
        # Use the real solvers find method with the complex method list
        super().findRoot(methodList)
        
        
        
    '''
    <name>muller</name>
    <summary>
    Interpolate points using a parabola, selecting the new points such that they 
    converge on the root. 
    </summary>
    '''
    def muller(self):
        
        count = 0                                    # Count Iterations            
        actualError = 10 * const.maxError            # Error when comparing iteratons
        
        firstPoint = self.firstGuess
        
        if self.secondGuess is None:
            # If only one guess is provided, bump the initial guess up and down by a scaled
            # amount (10%, or 0.1, by default)
            secondPoint = firstPoint * (1 + self.scaleFactor)
            thirdPoint = firstPoint * (1 + 2*self.scaleFactor)
            
        else:
            # Otherwise, average the two initial guesses. 
            thirdPoint = (firstPoint + secondPoint)/2
            
        while actualError > const.maxError and count < const.maxIterations:
            
            lastRoot = thirdPoint
            
            try:
                # Find the upper and lower differences
                lowerNum = self.f(secondPoint) - self.f(firstPoint)
                lowerDen = secondPoint - firstPoint
                
                upperNum = self.f(thirdPoint) - self.f(secondPoint)
                upperDen = thirdPoint - secondPoint

                lowerDiff = lowerNum/lowerDen
                upperDiff = upperNum/upperDen
                
                # Define the 'a', 'b', and 'c' parameters to apply quadratic interpolation
                quadParamA = (upperDiff - lowerDiff) / (thirdPoint - firstPoint)
                quadParamB = quadParamA * (thirdPoint - secondPoint) + upperDiff
                quadParamC = self.f(thirdPoint)
                
            except ZeroDivisionError:
                self.opLog.append('division by zero')
                return None
        
            except ValueError:
                self.opLog.append('invalid function evaluation')
                return None
            
            # Assume the positive square root is taken, unless B is negative, then use 
            # the negative square root
            signCheck = 1
            if quadParamB.real < 0:
                signCheck = -1
            
            try:
                den = quadParamB + signCheck * pow(quadParamB**2 - 4*quadParamA*quadParamC, 0.5)
                root = thirdPoint + (-2 * quadParamC) / den
                
            except ZeroDivisionError:
                self.opLog.append('division by zero')
                return None
            
            actualError = abs((lastRoot - root)/root)
            
            # Set the new points
            firstPoint = secondPoint
            secondPoint = thirdPoint
            thirdPoint = root
        
            count += 1
             
        self.opLog.append('converged at ' + str(root))
        
        if type(root) == complex:
            self.conjugate = complex(root.real, -root.imag)
            self.opLog.append('conjugate at ' + str(self.conjugate))
            
        return root

            
        
        
    def bairstow(self):
        pass
    
    
    
    def toString(self):
        
        # Get the instance information
        string = super().toString()
        
        # Insert the complex root into the pre-formatted real solver data
        hitFirst = False
        for i in range(len(string)):
            if string[i] == '\n':
                if not hitFirst:
                    hitFirst = True
                else:
                    newString = string[:i] + '\nRoot: ' + str(self.conjugate) + '\n' + string[i:]
                    break
        
        return newString
    
    
        
        
        

        