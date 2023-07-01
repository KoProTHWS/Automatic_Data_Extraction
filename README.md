# CAD Data Extraction Framework

## Description

This repository contains the code for a CAD Data Extraction Framework. 

## Repository Structure

Here's an overview of the repository structure and the purpose of each directory:

- `STP_Data_Extraction/`: Scripts for extracting features from STEP files, including relative positions between components, bounding box dimensions, center of gravity, PNG image generation for every component/sub-assembly, relationship matrix for assembly structure, topology, and more

- `DXF_Data_Extraction/`: A script dedicated to extracting a variety of data from DXF files, such as the variant/parameter table, title block, dimension endpoints, and circular entity radius

- `Instructions_Text_Extraction/`: Scripts designed to extract keywords from assembly instructions

- `NER_Model_Training/`: This directory holds scripts for training a custom NER label using SpaCy. It is particularly useful for tool name extraction from assembly instructions

- `Shape_Manipulate/`: This directory contains a script for generating concept variants using baseline 3D STEP models

## Getting Started

Each directory in the repository contains its own `README` file with specific usage instructions. Please refer to the README within each directory for detailed guidance on how to use each set of scripts.


