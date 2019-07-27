'''
Kaden Archibald

Created: Oct 23, 2018
Revised: Jul 27, 2019
Version: IPython 7.2.0 (Anaconda distribution) with Python 3.7.1

Module for numerically solving arbitrary real-valued
functions in a single vairable.
'''

def integrator(integrand, lowerBound, upperBound, evenStepSize = True, delta = None):
    ''' 
    Driver function to hide object instantiation from end programmer.
    '''
    
    integral = Integrator(integrand, lowerBound, upperBound, evenStepSize, delta)
    integral.findIntegral()
    return integral.area


class Integrator:
    def __init__(self, integrand, lowerBound, upperBound, evenStepSize = True, delta = None):
        
        # General Data
        self.f = integrand
        self.lowerBound = lowerBound
        self.upperBound = upperBound
        
        # Meta Data
        self.area = None                       # Final result (area under a curve).
        
        if delta is None:
            self.partition = int(10e4)
        else:
            self.partition = delta
        self.maxError = 10e-3
        
        self.evenStepSize = evenStepSize       # If false, a changing deltaX must be accounted for.
        self.willVerify = True                 # If true, apply more than one integration algorithm.
        self.opLog = []                        # Operation log.
        
        
        
    def findIntegral(self):
        # Apply each method included in the algorithm. Results from each algorithm will be logged and
        # compared for verification. 
        integratingMethods = [self.simpsonsRule, self.trapezoidalRule]
        self.areaLog = {}
        
        for method in integratingMethods:
            # If the method succeeded, write the area to memory; else, write None. 
            # Keep track of which method did what.
            self.areaLog[method.__name__] = method()
        
        if self.willVerify:
            # Make sure multiple algorithms agree on the solution and return their average
            if self.verifyIntegral():
                self.opLog.append('Updating area')
                self.area = self.avgArea
                
        else:
            # Or just return the first non null value
            for (key, value) in self.areaLog.items():
                if not value is None:
                    self.opLog.append('Updating area')
                    self.area = self.avgArea
                    break
        
                
            
    def verifyIntegral(self):
        # Begin verification
        results = []
        isConsistent = True
        
        for (key, value) in self.areaLog.items():
            # Ignore methods that failed
            if not value is None:
                results.append(value)
                
        self.avgArea = sum(results) / len(results)
        
        for possibleArea in results:
            if not abs((possibleArea - self.avgArea)/possibleArea) < self.maxError:
                self.opLog.append('Integrating methods do not agree')
                isConsistent = False
                break
        
        self.opLog.append('Integrating methods agree')
        return isConsistent
                
                
    '''
    Apply Simpson's Multi-application 1/3 Rule. Simpson's Rule involves approximating the
    area under the curve using a second order Lagrange polynomial. 
    '''
    def simpsonsRule(self):

        
        # Make sure step size is even. If not, make it even.
        if self.partition % 2 != 0:
            self.partition += 1
        
        # Initialize step size
        stepSize = (self.upperBound - self.lowerBound) / self.partition
        
        # Initialize output
        result = self.f(self.lowerBound) + self.f(self.upperBound)
        
        # Begin summation. One for loop is used for the odd indices and another for loop 
        # is used to the even indices because these two loops use different coefficients.
        firstSum = 0
        for i in range(1, self.partition, 2):
            try:
                firstSum += 4*self.f(self.lowerBound + i*stepSize)
            except (ValueError, ZeroDivisionError):
                self.opLog.append('Domain error in simpsons rule')
                return None
            
        secondSum = 0
        for i in range(2, self.partition-1, 2):
            try:    
                secondSum += 2*self.f(self.lowerBound + i*stepSize)
            except (ValueError, ZeroDivisionError):
                self.opLog.append('Domain error in simpsons rule')
                return None
        
        # Collect term, make assignment to self result variable, and return True to 
        # indicate success.
        result += firstSum + secondSum
        result *= (1/3) * stepSize
        
        #self.area = result
        self.opLog.append('simpsons rule returned with area: ' + str(result))
        return result
        
    
    
    '''
    Apply the multi-application trapezoidal rule. This algorithm will break the area 
    into 'self.partition' number of trapezoids, then sum the area of each trapezoid.
    '''      
    def trapezoidalRule(self):

        
        # Initialize step size
        stepSize = (self.upperBound - self.lowerBound) / self.partition
        
        # Initialize output
        result = stepSize/2
        
        # Initialize sum
        try:
            areaSum = self.f(self.lowerBound) + self.f(self.upperBound)
        except (ValueError, ZeroDivisionError):
            self.opLog.append('Domain error in trapezoidal rule initialization')
            return None
        
        # Perform sum
        for i in range(1, self.partition):
            try:
                areaSum += 2*self.f(self.lowerBound + i*stepSize)
            except (ValueError, ZeroDivisionError):
                self.opLog.append('Domain error in trapezoidal rule: Invalid input at' + str(i))
                return None
            
        result *= areaSum    
        
        #self.area = result
        self.opLog.append('trapezoidal rule returned with area: ' + str(result))
        return result




    def toString(self):
        
        thisStr = ''
        
        thisStr += 'Function: ' + self.f.__name__ + '\n'
        thisStr += 'Area:     ' + str(self.area) + '\n'
        thisStr += 'Operation Log: \n'
        for item in self.opLog:
            thisStr += '\t' + item + '\n'
        thisStr += 'Area Log: \n'
        for (key, value) in self.areaLog.items():
            thisStr += '\t' + str(key) + ': ' + str(value) + '\n'
            
        return thisStr
        















	