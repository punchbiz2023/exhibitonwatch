# -*- coding: utf-8 -*-
"""
Created on Mon Feb 27 00:12:03 2023

@author: DELL
"""

import subprocess
from PIL import Image
import cv2
import io
import numpy as np
# Load the image in the main script
image ='D:/Python_Codes/frames/frame_0.jpg'

# Define the command to run the sub script with the image path as an argument
command = ['python', 'detect13.py','--source',image ]

# Run the command using the subprocess module
result = subprocess.run(command, capture_output=True)
f = result.stdout
# Convert the string to a numpy array
normal_string = f.decode('utf-8')

print(normal_string) # Output: 'hello'