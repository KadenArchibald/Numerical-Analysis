'''
Kaden Archibald

Created: Jul 27, 2019
Revised: Jul 27, 2019
Version: IPython 7.2.0 (Anaconda distribution) with Python 3.7.1

Module for numerically solving arbitrary real-valued
functions in a single vairable.
'''


import data
    


class DataIntegrator:
    def __init__(self, fileName):
        
        self.data = data.loadMatrix(fileName)
        
        
        
        


