import cv2
import numpy as np
import pytesseract

# Load the image
image = cv2.imread('temp.jpg')
pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

# Preprocess the image (adjust based on your specific image)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray, 50, 150, apertureSize=3)  # Adjust the thresholds as needed

# Apply Hough Line Transform
lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=80, minLineLength=50, maxLineGap=10)
# Adjust the parameters as needed (lower threshold, shorter minLineLength)

# Create a blank mask of zeros
mask = np.zeros_like(gray)

# Draw the detected lines on the mask
if lines is not None:
    for line in lines:
        x1, y1, x2, y2 = line[0]
        cv2.line(mask, (x1, y1), (x2, y2), (255, 255, 255), 2)

# Find contours in the mask
contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Find the largest contour
largest_contour = max(contours, key=cv2.contourArea)

# Create a blank mask of zeros
mask = np.zeros_like(gray)

# Draw the largest contour on the mask
cv2.fillPoly(mask, [largest_contour], (255, 255, 255))

# Apply the mask to extract the region of interest
roi = cv2.bitwise_and(gray, mask)

# Use Tesseract to extract text from the region of interest
text = pytesseract.image_to_string(roi)

# Display the extracted text
print(text)