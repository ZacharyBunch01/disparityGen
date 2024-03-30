# Disparity Map to 3D Point Cloud Converter

## Overview

This program generates a 3D point cloud from two input images by first creating a disparity map using OpenCV and then converting it into a 3D point cloud. It utilizes OpenCV for generating the disparity map due to its speed and accuracy, and pyvista for plotting the vertices, offering better performance and higher-quality visualization.

## Running the Program

To run the program, follow these steps:

1. Clone the repository to your local machine:
   ```bash
   git clone https://github.com/ZacharyBunch01/disparityGen.git

3. Navigate to the project directory.

4. Run the following command:
   ```bash
   python main.py

Note: If you are using MacOS, use `python3` instead of `python`:
   ```bash
   python3 main.py

4. The program will automatically install any necessary dependencies if not already installed.

5. Follow the prompts to select the scene of interest.

6. Once the processing is complete, the result will be displayed.

## Dependencies

The following dependencies are required to run the program:

- Python 3.x
- OpenCV
- pyvista

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgments

- This project utilizes the power of OpenCV and pyvista for efficient and accurate generation and visualization of 3D point clouds.


