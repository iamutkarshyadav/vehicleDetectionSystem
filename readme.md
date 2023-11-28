    # Vehicle Detection Project

## Introduction

This project is a simple vehicle detection system using OpenCV in Python. It utilizes background subtraction to detect vehicles in a video stream, counts the number of vehicles crossing a specified line, and displays the results on the video frame.

## Requirements

Make sure you have the following libraries installed before running the project:

- [OpenCV](https://pypi.org/project/opencv-python/): `pip install opencv-python`
- [NumPy](https://numpy.org/): `pip install numpy`

## How it Works

1. **Video Input:** The project takes a video file (`video.mp4` in this example) as input. You can replace it with your own video file or use a webcam as the video source.

2. **Background Subtraction:** The algorithm uses OpenCV's `createBackgroundSubtractorMOG` to perform background subtraction, highlighting moving objects in the video.

3. **Contour Detection:** Contours are identified in the processed frame, and rectangles are drawn around objects that meet size criteria (presumed to be vehicles).

4. **Vehicle Counting:** The system counts vehicles based on whether their center crosses a specified counting line on the video frame.

5. **Logging:** The project uses Python's `logging` module to provide structured output about detected vehicles and the total count.

## Usage

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/vehicle-detection-project.git
    cd vehicle-detection-project
    ```

2. Install the required libraries:

    ```bash
    pip install -r requirements.txt
    ```

3. Run the project:

    ```bash
    python vehicle.py
    ```

4. Press `Enter` to exit the program.

## Customization

- You can replace the input video file (`video.mp4`) with your own video file.
- Adjust parameters such as the counting line position, contour size criteria, and logging preferences in the `vehicle_detection.py` file.

## License

This project is licensed under the [MIT License](LICENSE).
