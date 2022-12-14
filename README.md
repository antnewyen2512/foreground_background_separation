# Foreground-background Separation

## Overview
- This program was built and run on windows using VSCode IDE, using its powershell is recommended (it worked well on my computer)

## Requirements: python/python3, pip, numpy, opencv-python to be able to run the code
- Additionally, install project dependencies (numpy 1.20.2 or above):
`pip install -r requirements.txt`

## Run the program
- run the program with the following command:
`pythom src/main.py`
- then a shell cursor will appear in the terminal such as `>>`

- Train the model (# = numbers):
`train --source Video1.MOV --name model(#)`

- Perform the background subtraction (# = numbers):
`separate --source Video2.MOV --model model(#).json --out Output(#)`

## Models and output files
- Models are located in the model folder and in json format.
- Output files are located in the output folder.

# Note: I left a trained model and an output in the repo, just in case we need it. Otherwise, feel free to train a new model and separate it using the provided command above (change # to avoid duplication). 
