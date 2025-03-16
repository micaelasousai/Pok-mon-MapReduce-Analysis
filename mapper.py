#!/usr/bin/python3
# Shebang line 
# Streaming framework needs this line to invoke the Python code

##############################################################################################
##                                                                                          ##
##      Mapper                                                                              ##
##      Copyright Micaela Sousa, 2025                                                       ##
##                                                                                          ##
##############################################################################################

# Program Description:
# The mapper (mapper.py) processes the Pokémon dataset line by line and extracts relevant information. 
# It computes a feistiness score for each Pokémon and outputs it in a structured format for the reducer to process.                                                                                                      

# Import statements
# Python sys library: used to have access to the standard input, output and error streams of the Operating System
import sys
# CSV module
import csv

# Read the standard input stream contents line by line
reader = csv.reader(sys.stdin, delimiter=',')

# Ignore the first line (header)
next(reader, None)

# Process each line in the dataset
for words in reader:
    # Debugging print to check the raw data
    #print("Raw line:", words)S
        
    # Create variable to access relevant columns (type1, type2, name, attack, weight_kg)
    try:
        # Extract relevant fields
        # Deal with missing values by assigning empty string
        type1 = words[36].strip() if len(words) > 36 else ""
        type2 = words[37].strip() if len(words) > 37 else ""
        name = words[30].strip() if len(words) > 30 else ""
    
        # Convert attack and weight_kg to float before division
        attack = float(words[19].strip()) if len(words) > 19 else 0.0
        weight_kg = float(words[38].strip()) if len(words) > 38 else 0.0
        
        # Calculate feistiness (attack per weight)
        # Avoid division by zero
        if weight_kg > 0: 
            feistiness = round(attack/weight_kg, 2)        
            # Create key value pairs
            # Convert values to string and join them with commas
            value = f"{type2},{name},{feistiness}"
            # Print key-value pair
            print(f'{type1}\t{value}') # Using '\t' as a delimeter
        
    except (IndexError, ValueError) as e:
        # Skip malformed lines or incomplete lines and continue processing
        continue
