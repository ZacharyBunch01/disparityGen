import utils
import pyvista as pv
import numpy as np
import matplotlib.pyplot as plt

def main():

    # Get user input
    scene = utils.init()

    # The baseline values provided in the
    # dataset were wrong / not clear.
    if scene == 1:
        # Read the param file.
        cam_params_path = 'camParams1.txt'
        cam_params = utils.read_cam_params(cam_params_path)
        
        # Update the baseline param to appear more clearly.
        cam_params['baseline']  = (cam_params['baseline'] * 2)
    elif scene == 2:
        # Read the param file.
        cam_params_path = 'camParams2.txt'
        cam_params = utils.read_cam_params(cam_params_path)
        
        # Update the baseline param to appear more clearly.
        cam_params['baseline']  = (cam_params['baseline'] * 0.2)
    elif scene == 3:
        # Read the param file.
        cam_params_path = 'camParams3.txt'
        
        # Update the baseline param to appear more clearly.
        cam_params = utils.read_cam_params(cam_params_path)
        cam_params['baseline']  = (cam_params['baseline'] * 0.2)
    
    # Pass the values from the param file.
    focalLength = cam_params['cam0'][0][0]
    baseLine = cam_params['baseline']
    cx = cam_params['cam0'][0][2]
    cy = cam_params['cam0'][1][2]
    leftImagePath = cam_params['leftImagePath']
    rightImagePath = cam_params['rightImagePath']
    cam0_matrix = cam_params['cam0']
    cam1_matrix = cam_params['cam1']
    doffs = cam_params['doffs']
    ndisp = cam_params['ndisp']
    vmin = cam_params['vmin']
    vmax = cam_params['vmax']
    width = cam_params['width']
    height = cam_params['height']

    cam_params = {
        'leftImagePath': leftImagePath,
        'rightImagePath': rightImagePath,
        'focal_length': focalLength,
        'baseline': baseLine,
        'cx': cx,
        'cy': cy,
        'cam0': cam0_matrix,
        'cam1': cam1_matrix,
        'doffs': doffs,
        'ndisp': ndisp,
        'vmin': vmin,
        'vmax': vmax,
        'width': width,
        'height': height,
    }

    # Get disparity map and color values
    disparity, colors = utils.get_disparity(leftImagePath, rightImagePath, ndisp)
    
    # Get vertex data
    points_3D, colors_3D = utils.depth_to_3d(disparity, colors, cam_params)

    # Normalize colors to be within the range of 0 to 1 (Otherwise, an error is thrown) 
    colors_3D_normalized = colors_3D / 255.0

    cloud = pv.PolyData(points_3D)
    cloud['colors'] = colors_3D_normalized  # Add colors as point data
    
    # Create a plotter and add the point cloud with colors
    plotter = pv.Plotter()
    plotter.add_points(cloud, rgb=True, point_size=5)
    
    # Configure and show the plot
    plotter.show()

if __name__ == "__main__":
    main()
