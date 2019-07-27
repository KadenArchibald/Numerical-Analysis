'''
Kaden Archibald

Created: Oct 11, 2018
Revised: Jul 13, 2019
Version: IPython 7.2.0 (Anaconda distribution) with Python 3.7.1

Module for numerically solving arbitrary real-valued
functions in a single vairable.
'''

import const

''' Driver function to hide object intialization from end programmer. '''
def realSolver(function, firstGuess, secondGuess = None, fPrime = None):
    
    temp = RealSolver(function, firstGuess, secondGuess, fPrime)
    temp.findRoot()
    return temp.root


class RealSolver:
    
    '''
    <summary>
    Create an object that contains a function to be solved, one (or two) initial
    guesses, a function for the derivative, auxiliary precalculated arguements for a function,
    and data about the root solving problem itself: a maximum error, a maximum number of
    iterations, and a string array to log major operations.
    </summary>
    <input>self, function, firstGuess, secondGuess, fPrime</input>
    <output>None</output>
    '''
    def __init__(self, function, firstGuess, secondGuess = None, fPrime = None):

        # General Data
        self.f = function                           # Function to be solved numerically
        self.firstGuess = firstGuess                # First initial estimate of the root
        self.secondGuess = secondGuess              # Second initial guess of the root

        if not secondGuess is None:
            self.isBracketed = True                 # True if initialized with two estimates...
        else:
            self.isBracketed = False                # ...False otherwise

        self.fPrime = fPrime                        # First derivative of the function


        # Meta Data
        self.root = None                            # Store the final result
        self.isCorrect = False                      # True if the root if verified to be correct
        self.opLog = []                             # Log major operations of the algorithm
        

        # Begin the Root Finding Procedure
        self.realMethods = [self.newtonRaphson, self.onePointIteration, self.bisection]
        self.opLog.append('Initialization Succesful\n')
        
    
    '''
    <summary>
    Apply the first root finding algorithm and then reevaluate the function at the
    returned root. If the functions returns (close enough to) zero, terminate the
    loop and return that value.

    If the algorithm diverges, or if the algorithm returns a value that is not
    the root, continue to the next algorithm.

    For general functions, algorithms such as Newton's Method and the Bisection Method
    usually converge, so all alogrithms failing will usually mean that the
    function has no real roots.
    </summary>
    <input>self, list</input>
    <output>None</output>
    '''
    def findRoot(self, methodList = []):
        
        # Every algorithm will return an estimate of the root.
        # Keep a dictionary of which method returned which estimate.
        self.rootLog = {}
        
        # Find the root from every method
        if not methodList:
            methodList = self.realMethods
        
        for method in methodList:
            
            name = method.__name__
            self.opLog.append(name + ' started')
            
            potentialRoot = method()
            self.rootLog[name] = potentialRoot
            
            if not potentialRoot is None:
                if self.verifyRoot(potentialRoot, name):
                    self.root = potentialRoot
                    #break
            
            else:
                self.opLog.append(name + ' halted\n')

                    
                    
    '''
    <summary>
    Verify that a root really is zero before terminating. This method ensures that no number
    that is not actually a root will ever be returned. This is valuable becuase some
    algorithms can converge to incorrect values, especially if the initial guess was an optima
    or endpoint of a funciton.
    </summary>
    <input>self, double, str</input>
    <output>bool</output>
    '''              
    def verifyRoot(self, potentialRoot, name):
        
        isVerified = False

        try:
            if abs(self.f(potentialRoot)) <= const.maxError:
                self.opLog.append(name + ' verified\n')
                isVerified = True
            else:
                self.opLog.append(name + ' converged to incorrect value\n')
                
        except ValueError:
            self.opLog.append(name + ' returned an undefined value\n')
            
        except TypeError:
            if self.root is None:
                self.opLog.append('root not updated in meta data\n')
            
        return isVerified
        

    
    '''
    <name>newtonRaphson</name>
    <summary>
    Employ Newton's Method of numerically converging on a root using
    a function's derivative:
        X(i+1) = X(i) - f(X(i))/g(X(i))
    Where f is the target function, g is that function's derivative, and i
    is the current iteration.
    </summary>
    <input>self</input>
    <output>bool</output>
    '''
    def newtonRaphson(self):
        
        count = 0                                    # Count Iterations
        root = self.firstGuess                       # Store the result
        actualError = 10 * const.maxError            # Error when comparing iteratons
        deltax = 1e-10                               # Step size for secant line

        while actualError > const.maxError and count < const.maxIterations:

            # Store the last root. 
            lastRoot = root

            # Find the slope of the line secant to the curve at this point by using
            # numerical differentiation. If the parameter fPrime (the functions derivative)
            # was provided, then use that to find the tangent line.
            
            try:
                if self.fPrime is None:
                    # Secant Line 
                    slope = (self.f(lastRoot + deltax) - self.f(lastRoot))/deltax
                else:
                    # Tangent Line
                    slope = self.fPrime(lastRoot)
                
                # Find the new root and the error from the last root
                root = lastRoot - self.f(lastRoot)/slope
                actualError = abs((lastRoot - root)/root)
                
                # Special case for roots that are close to zero because the method used
                # to find the actual error diverges for small root values
                if abs(root) < const.maxError:
                    break
                
            except (ValueError, ZeroDivisionError):
                self.opLog.append('invalid function evaluation')
                return None

            count += 1

        self.opLog.append('converged at ' + str(root))
        return root


    '''
    <name>bisection</name>
    <summary>
    Starting with two initial guesses, conduct a binary search.
    </summary>
    <input>self</input>
    <output>double</output>
    '''
    def bisection(self):
        
        # Do not execute without a second guess
        if not self.isBracketed:
            self.opLog.append('closed method not attempted')
            return None

        count = 0                                    # Count Iterations
        upperBound = self.secondGuess                # Start Here
        lowerBound = self.firstGuess                 # End Here

        while count < const.maxIterations:

            # Assume the root is the average of the two bounds.
            root = (upperBound + lowerBound)/2

            # Check the sign of the new root.
            try:
                signCheck = self.f(root) * self.f(lowerBound)

            except (ValueError, ZeroDivisionError):
                self.opLog.append('invalid function evaluation')
                return None

            # Check where this value lands. If the root is not found, check the sign of the
            # estimated root to decide which bound to discard.
            try:
                if abs(self.f(root)) < const.maxError:
                    break

                else:
                    if signCheck > 0:
                        lowerBound = root
                    if signCheck < 0:
                        upperBound = root

            except (ValueError, ZeroDivisionError):
                self.opLog.append('invalid function evaluation')
                return None

            count += 1

        self.opLog.append('converged at ' + str(root))
        return root


    '''
    <name>onePointIteration</name>
    <summary>
    Transform the root equation into iterator form:
        0 = f(x)  -->  x = g(x)
    Then iterate with the transformed equation:
        X(i+1) = g(X(i))
    </summary>
    <input>self</input>
    <output>None</output>
    '''
    def onePointIteration(self):
        
        count = 0                                    # Count Iterations
        root = self.firstGuess                       # Store the result
        actualError = 10 * const.maxError            # Error when comparing iteratons
        
        while actualError > const.maxError and count < const.maxIterations:
            
            # Store the last root.
            lastRoot = root
            
            # Add the old estimate to each side of the function to find a new estimate.
            try:
                root = self.f(lastRoot) + lastRoot
            
            except (ValueError, ZeroDivisionError):
                self.opLog.append('invalid function evaluation')
                return None
            
            except OverflowError:
                self.opLog.append('overflow')
                return None
            
            actualError = abs((lastRoot - root)/root)
            
            count += 1

        self.opLog.append('One Point Iteration Converged at ' + str(root))
        return root


    '''
    <name>toString</name>
    <summary>
    Return a string representation of the object.
    </summary>
    <input>self</input>
    <output>str</output>
    '''
    def toString(self):
        
        thisStr = ''
        
        thisStr += 'Function: ' + self.f.__name__ + '\n'
        thisStr += 'Root: ' + str(self.root) + '\n'
        thisStr += 'Operation Log: \n'
        for item in self.opLog:
            thisStr += '\t' + item + '\n'
        thisStr += 'Root Log: \n'
        for (key, value) in self.rootLog.items():
            thisStr += '\t' + key + ': ' + str(value) + '\n'
            
        return thisStr
    
    # docstring
    '''
    <name></name>
    <summary>
    
    </summary>
    <input></input>
    <output></output>
    '''
