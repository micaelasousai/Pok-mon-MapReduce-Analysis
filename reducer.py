#!/usr/bin/python3
# Shebang line 
# Streaming framework needs this line to invoke the Python code

##############################################################################################
##                                                                                          ##
##      Reducer                                                                             ##
##      Copyright Micaela Sousa, 2025                                                       ##
##                                                                                          ##
##############################################################################################

# Program Description:
# Reducer gets the key-value pairs
# Finds the fiestiest Pokemon for each type
# Outputs a CSV file containing the fields: type1, type2, name, fiestiness

# Import statements
# Python sys library: used to have access to the standard input, output and error streams of the Operating System
import sys

# Initialize variables
currentType = '' # Stores the current type being processed
currentMaxF = 0.0 # Stores the current maximum feistiness of the current type
maxFtype2 = '' # Store the second type for the Pokémon with the highest feistiness
maxFname = '' # Store the name of the Pokémon with the highest feistiness
nextType = '' # Store the type from the current line

# Header Names 
headers = ['type1', 'type2', 'name', 'feistiness']

# Print header for CSV output
print(','.join(headers))

# Read the standard input stream contents line by line
# Keys are passed sorted by key value during shuffle phase
for line in sys.stdin:
    # Remove whitespace
    line = line.strip()

    # Split into key and value (type1 will be the key)
    try:
        nextType, value = line.split("\t", 1)
    except ValueError:
        # Skip lines that do not match expected format
        continue

    # Split value into type2, name and feistiness
    type2, name, feistiness = value.split(",")

    # Convert feistiness to float so it can be compared with current max feistiness
    try:
        feistiness = float(feistiness)
    except ValueError:
        # If there is an error, skip this line 
        continue

    # Compare type
    if currentType == nextType:
        # Compare feistiness to current max feistiness
        if feistiness > currentMaxF:
            currentMaxF = feistiness
            maxFtype2 = type2
            maxFname = name
    else: 
        if currentType != '': 
            # Print result for the previous type (current type) to standard output
            print(f'{currentType},{maxFtype2},{maxFname},{currentMaxF}')
        # Update for the new type
        currentMaxF = feistiness
        maxFtype2 = type2
        maxFname = name
        currentType = nextType

# Print last entry after loop finishes
if (currentType == nextType):
    print(f'{currentType},{maxFtype2},{maxFname},{currentMaxF}')

