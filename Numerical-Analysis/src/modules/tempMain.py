'''
Driver for Numerical Method Module Testing
'''

from math import pi, sin, sqrt, log
import datetime


import RealSolver
import ComplexSolver
import Integrator
#import Differentiator

# Initialize Testing Functions

def f1(x):
    # Root: 0, 3.141592653589793, etc.
    return sin(x)

def f2(x):
    # Root: 0.9958555221487722
    return 0.2 + 25*x - 200*x**2 + 675*x**3 - 900*x**4 + 400*x**5

def f3(x):
    # Root: 0.0
    return sqrt(x**2 + x)

def f4(x):
    # Root: 1.0
    return log(x, 2)

def f5(x):
    # Root: +j & -j
    return x**2 + 1


def main():
    
    # Initialize log
    try:
        logFile = open('log.txt', 'w')
    except FileNotFoundError:
        logFile = open('log.txt', 'x')
    finally:
        logFile.write('Test Log for Numerical-Analysis \n')
        logFile.write(str(datetime.datetime.now()) + '\n')
    
    
    
    # Root Finding
    print('Root Finding')
    print('Test 1:', RealSolver.realSolver(f1, 1))
    print('Test 2:', RealSolver.realSolver(f2, 10))
    print('Test 3:', RealSolver.realSolver(f3, -2, 2))
    print('Test 4:', RealSolver.realSolver(f4, 1))
    print()
    
    # Integration
    print('Integration')
    print('Test 1:', Integrator.integrator(f1, 0, pi/4))
    print('Test 2:', Integrator.integrator(f2, 0, 0.8))
    print('Test 3:', Integrator.integrator(f3, 1, 10))
    print('Test 4:', Integrator.integrator(f4, 10, 20))
    print()
#    
#    # Differentiation
#    print('Differentiation')
#    print('Test 1:', Differentiator.diff(f1, pi/2))
#    print('Test 2:', Differentiator.diff(f2, 1))
#    print('Test 3:', Differentiator.diff(f3, 0))
#    print('Test 4:', Differentiator.diff(f4, 0))
#    print()


    temp = Integrator.Integrator(f1, 0, pi)
    temp.findIntegral()
    print(temp.toString())
    
    
    
    return None

if __name__ == '__main__':
    main()

