# AI Virtual Pen using OpenCV

A real-time Virtual Pen application built using Python and OpenCV that allows users to draw on the screen using a colored object tracked through a webcam.

The system uses HSV color segmentation, contour detection, and centroid tracking to simulate touchless drawing on a digital canvas.

---

## Features

- Real-time webcam-based object tracking
- Multiple color selection (Blue, Green, Red, Yellow)
- Clear button to reset the canvas
- Smooth drawing using deque-based point storage
- Adjustable HSV trackbars for dynamic color tuning
- Split-screen output (Canvas + Live Overlay)

---

## How It Works

1. Captures live video frames from the webcam.
2. Converts frames from BGR to HSV color space.
3. Applies HSV thresholding to isolate a specific colored object.
4. Uses morphological operations (erosion, dilation, opening) to remove noise.
5. Detects contours and selects the largest contour.
6. Calculates the centroid using image moments.
7. Stores centroid points using deque for smooth drawing.
8. Draws continuous lines between tracked points on a black canvas.
9. Displays final output with both drawing canvas and live feed overlay.

---

## Technologies Used

- Python
- OpenCV
- NumPy
- Collections (deque)

---

## Requirements

Create a `requirements.txt` file with the following content:

numpy
opencv-python

Install dependencies using:

pip install -r requirements.txt

---

## How to Run

1. Clone the repository:

git clone https://https://github.com/SaiPrabhathDevalla/Virtual-Pen.git
cd your-repo-name

2. Run the program:

python virtual_pen.py

3. Press `q` to exit the application.

---

## Controls

| Action | Description |
|--------|-------------|
| Move colored object | Draw on canvas |
| Move to CLEAR button | Clears the canvas |
| Move to color button | Changes drawing color |
| Press `q` | Exit application |

---

## HSV Tuning

The application includes adjustable HSV trackbars to adapt to different lighting conditions:

- Upper Hue
- Upper Saturation
- Upper Value
- Lower Hue
- Lower Saturation
- Lower Value

Adjust these values until the colored object is properly detected.

---

## Future Enhancements

- Hand gesture tracking (without colored marker)
- Save drawings as image or PDF
- Undo/Redo functionality
- AI-based object detection for improved robustness
- Integration with presentation tools

---

## Use Cases

- Online teaching
- Touchless whiteboard
- Interactive presentations
- Computer vision learning project
- Human-computer interaction research

---

## Learning Outcomes

- Real-time computer vision implementation
- HSV color segmentation
- Contour detection and centroid tracking
- Morphological image processing
- Use of deque data structure for smoothing
- UI element creation using OpenCV
