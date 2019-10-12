
import datetime

class Log:
    def __init__(self, fileName, openMode):
        
        self.fileName = fileName
        
        if not openMode in ['w', 'a', 'x', 'b']:
            openMode = 'a'
        
        try:
            self.fd = open(self.fileName, openMode)
            
            
        except FileNotFoundError:
            print('i got here')
            self.fd = open(self.fileName, 'x')
            
        finally:
            self.fd.write('Log Initialized\n')
            self.fd.write(str(datetime.datetime.now()) + '\n')
    


    ''' Write string to file. '''
    def writeStr(self, string) -> bool:
        success = True
         
        try:
            self.fd.write(string + '\n')
        
        except TypeError:
            print('Cannot write data to file')
            print('File: ' + str(self.fileName) + ' not updated')
            success = False
            
        return success
    
    
    ''' Write list of strings to file. '''
    def writeList(self, strArray) -> bool:
        success = True
        
        for string in strArray:
            success = self.writeStr(string)
            
        return success
        
    
    ''' Write 2D array to file. '''
    def writeMatrix(self, data):
        success = True
        
        try:
            for row in data:
                for col in row:
                    self.fd.write(str(col) + ' ')
                self.fd.write('\n')
                
        except ValueError:
            print('Cannot convert data to str')
            print('File: ' + str(self.fileName) + ' not updated')
            success = False
            
        except TypeError:
            print('Cannot write data to file')
            print('File: ' + str(self.fileName) + ' not updated')
            success = False
    
        return success
    
    
    