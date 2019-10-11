

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