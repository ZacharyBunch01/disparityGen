import subprocess

'''
# List of required packages
required_packages = ['numpy', 'pillow', 'pyvista', 'opencv-python', 'opencv-python-headless', 'matplotlib']

# Function to check if a package is installed
def is_package_installed(package_name):
    try:
        subprocess.check_output(['pip', 'show', package_name])
        return True
    except subprocess.CalledProcessError:
        return False

# Function to install a package using pip
def install_package(package_name):
    subprocess.call(['pip', 'install', package_name])

# Check and install required packages
print("Checking for required packages...")
for package in required_packages:
    if not is_package_installed(package):
        print(f"{package} is not installed. Installing...")
        install_package(package)
        print(f"{package} installed successfully.")
    else:
        print(f"{package} is already installed.")

print("All required packages are installed.")
'''

import os
from PIL import Image
import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt

# Prompts the user for the scene value
def init():
    scene = input("Which scene would you like to see? (Choose 1-3): ")
    
    try:
        scene = int(scene)
        if scene not in [1, 2, 3]:
            print("Invalid input. Please choose 1, 2, or 3.")
            return init()
    except ValueError:
        print("Invalid input. Please enter a number.")
        return init()

    return scene
    
# Read and pass values from the camParam file
def read_cam_params(filepath):
    params = {}
    with open(filepath, 'r') as file:
        for line in file:
            key, value = line.split('=')
            key = key.strip()
            value = value.strip()
            
            # Skip conversion for string values
            if value.startswith('"') and value.endswith('"'):
                params[key] = value.strip('"')
            # Handle matrix values
            elif key in ['cam0', 'cam1']:
                params[key] = [list(map(float, row.split())) for row in value.strip('[]').split(';')]
            # Handle single float or int values
            elif '.' in value:
                params[key] = float(value)
            else:
                params[key] = int(value)
                
    return params

# Generate disparity map
def get_disparity(leftImagePath, rightImagePath, nDisp):

    # Read the images
    leftImage = cv.imread(leftImagePath)
    rightImage = cv.imread(rightImagePath)
    
    # Store color value
    colors = cv.cvtColor(leftImage, cv.COLOR_BGR2RGB)

    # Grayscale the images
    leftImage = cv.cvtColor(leftImage, cv.COLOR_BGR2GRAY)
    rightImage = cv.cvtColor(rightImage, cv.COLOR_BGR2GRAY)
    
    # Stereo params
    blockSize = 5
    
    stereo = cv.StereoSGBM_create(blockSize=blockSize, numDisparities=nDisp)
    
    # Compute the disparity map
    disparity = stereo.compute(leftImage, rightImage)
    
    disparity = cv.medianBlur(disparity, 5)

    # Normalize results
    disp_display = cv.normalize(disparity, None, alpha=0, beta=255, norm_type=cv.NORM_MINMAX, dtype=cv.CV_8U)

    # Display disparity map
    plt.imshow(disparity, 'gray')
    plt.show()

    return disparity, colors

# Disparity map to depth using d = (f * B)/disparity
def get_depth(disparity, focalLength, baseLine):
    # Set minimum disparity to avoid division by zero
    min_disparity = 0.01
    
    disparity = np.maximum(disparity, min_disparity)

    # Depth formula
    depth = (focalLength * baseLine) / disparity
    
    return depth
    
# Calculate 3D point cloud vertices
def depth_to_3d(disparity, colors, cam_params):
    focalLength = cam_params['focal_length']
    baseLine = (cam_params['baseline'])
    cx, cy = cam_params['cx'], cam_params['cy']
    leftImagePath = cam_params['leftImagePath']
    rightImagePath = cam_params['rightImagePath']
    cam0 = cam_params['cam0']
    cam1 = cam_params['cam1']
    doffs = cam_params['doffs']
    ndisp = cam_params['ndisp']
    vmin = cam_params['vmin']
    vmax = cam_params['vmax']
    width = cam_params['width']
    height = cam_params['height']

    # Calculate Z values
    depth = get_depth(disparity, focalLength, baseLine)
    
    # Compute perspective matrix
    Q = np.array([
              [1, 0, 0, -cx],
              [0, 1, 0, -cy],
              [0, 0, 0, focalLength],
              [0, 0, 1 / baseLine, doffs]])
              
    points_3D = cv.reprojectImageTo3D(disparity, Q)
    
    # Filter out points outside of these boundaries
    mask = (depth > vmin) & (depth < vmax)

    # Filter out points using the mask
    points_3D = points_3D[mask]
    colors = colors[mask]
    
    return points_3D, colors
