-- OVERVIEW --

This program creates a disparity map based on two input images, and converts that a 3D point cloud.

I used OpenCV to generate the disparity map and vertices. I chose not to write my own method for the disparity map generator because OpenCV's method is so fast and accurate. I used pyvista to plot the vertices due to its overall better performance and higher quality appearance.

-- RUNNING THE PROGRAM --

* Run $ python main.py to run the program. (Use python3 if on MacOS)

* The program automatically installs any necessary dependencies.

* The program will then prompt the user for a scene choice.

* Finally, the result is visible.


