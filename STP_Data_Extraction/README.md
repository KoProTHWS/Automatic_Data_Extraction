# STP Data Extraction

This Python module provides a suite of tools for extracting useful data from STP (STEP) files. It includes tools for:

1. Extracting color values for each component in the assembly.
2. Extracting geometric dimensions, physical properties, and origin locations of each component.
3. Generating and saving PNG images of the assembly and individual components.
4. Exporting individual components of the assembly as separate STP files.
5. Analyzing the topology of the assembly.
6. Generating a relationship matrix of the assembly structure.

## Requirements

- Python
- PythonOCC 
- Pandas


## Usage

Run the main Python script (`main.py`) with the desired STEP file as input. The script will perform the data extraction, image generation, component export, topology analysis, and relationship matrix generation, printing the results to the console and saving images and individual component STP files to new folders.

All the tabular outputs are dataframes, so can be easily exported to CSV or excel, or even loaded into MongoDB with little preprocessing.


