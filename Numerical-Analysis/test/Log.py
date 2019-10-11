


# Should turn all of this into a class (maybe call it Log)



''' Write string to file. '''
def writeStr(fileName, string, writeMode):
    success = True
    
    if not writeMode in ['w', 'a', 'x', 'b']:
        writeMode = 'a'
    
    try:
        file = open(fileName, writeMode)
        
        try:
            file.write(string + '\n')
        
        except TypeError:
            print('Cannot write data to file')
            print('File: ' + str(fileName) + ' not updated')
            success = False
        
    except FileNotFoundError:
        print('Cannot find file')
        print('File: ' + str(fileName) + ' not updated')
        success = False
        
    file.close()            
    return success


''' Write list of strings to file. '''
def writeList(fileName, strings, writeMode):
    
    pass
    
    
    

''' Write 2D array to file. '''
def writeMatrix(fileName, data):
    success = True
    
    with open(fileName, 'w') as file:
        try:
            for row in data:
                for col in row:
                    file.write(str(col) + ' ')
                file.write('\n')
                
        except ValueError:
            print('Cannot convert data to str')
            print('File: ' + str(fileName) + ' not updated')
            success = False
            
        except TypeError:
            print('Cannot write data to file')
            print('File: ' + str(fileName) + ' not updated')
            success = False

    return success



''' Load data from file into 2D array. '''
def loadMatrix(fileName):
    data = []
    
    with open(fileName, 'r') as file:
        for row in file:
            # Break the row (type: string) into an array at every whitespace
            splitRow = row.split()
            
            # Convert the numeric data to type float
            for col in splitRow:
                try:
                    col = float(col)
                except ValueError:
                    print('Cannot convert data to float')
                    print('Data from file: ' + str(fileName) + \
                          ' has non-numeric data')
                    
            
            # Store in the final array
            data.append(splitRow[:])
        
    return data