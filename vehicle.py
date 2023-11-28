import cv2
import numpy as np
import logging

# Configure the logging module
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Open video file
cap = cv2.VideoCapture('video.mp4')

# Set the position of the counting line
count_line_position = 550

# Initialize the background subtractor
algo = cv2.bgsegm.createBackgroundSubtractorMOG()

# Function to calculate the center of a rectangle
def calculate_center(x, y, w, h):
    x1 = int(w / 2)
    y1 = int(h / 2)
    cx = x + x1
    cy = y + y1
    return cx, cy

# Lists to store the centers of detected objects
detected_centers = []

# Offset to allow the car to be over the line a little bit
offset = 6

# Counter to keep track of the number of vehicles
vehicle_counter = 0

# Main loop
while True:
    # Read a frame from the video
    ret, frame = cap.read()

    # Convert the frame to grayscale
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur to the grayscale frame
    blurred_frame = cv2.GaussianBlur(gray_frame, (3, 3), 5)

    # Apply the background subtractor algorithm on the blurred frame
    subtracted_frame = algo.apply(blurred_frame)

    # Dilate the resulting image to fill gaps in between object contours
    dilated_frame = cv2.dilate(subtracted_frame, np.ones((5, 5)))

    # Define a kernel for morphological operations
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))

    # Apply morphological operations to further process the image
    processed_frame = cv2.morphologyEx(dilated_frame, cv2.MORPH_CLOSE, kernel)
    processed_frame = cv2.morphologyEx(processed_frame, cv2.MORPH_CLOSE, kernel)

    # Find contours in the processed image
    contours, hierarchy = cv2.findContours(processed_frame, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Draw the counting line on the frame
    cv2.line(frame, (25, count_line_position), (1200, count_line_position), (255, 127, 0), 3)

    # Loop through each detected contour
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)

        # Check if the contour satisfies the size criteria
        valid_contour = w >= 80 and h >= 80
        if not valid_contour:
            continue

        # Draw a rectangle around the detected object
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Display the vehicle count above each detected object
        cv2.putText(frame, f"VEHICLE COUNT: {vehicle_counter}", (x, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 244, 0), 2)

        # Calculate and store the center of the rectangle
        center = calculate_center(x, y, w, h)
        detected_centers.append(center)
        cv2.circle(frame, center, 4, (0, 0, 255), -1)

        # Check if the center of the object crosses the counting line
        for center_point in detected_centers:
            cx, cy = center_point
            if count_line_position - offset < cy < count_line_position + offset:
                # Increment the counter and log the event
                vehicle_counter += 1
                logger.info(f"Vehicle detected. Total count: {vehicle_counter}")

                # Remove the detected center to avoid double counting
                detected_centers.remove(center_point)

    # Display the total vehicle count on the frame
    cv2.putText(frame, f"VEHICLE COUNT: {vehicle_counter}", (450, 70), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 5)

    # Display the original video frame
    cv2.imshow('Video Original', frame)

    # Break the loop if 'Enter' key is pressed
    if cv2.waitKey(1) == 13:
        break

# Close all windows and release the video capture object
cv2.destroyAllWindows()
cap.release()

