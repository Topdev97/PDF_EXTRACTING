import cv2
import pytesseract
import numpy as np
# Load the image using OpenCV
image = cv2.imread('output_image_1.jpg')

# Convert the image to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply adaptive thresholding to obtain a binary image
_, binary = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)

# Perform line detection using HoughLinesP
lines = cv2.HoughLinesP(binary, rho=1, theta=1*np.pi/180, threshold=100, minLineLength=100, maxLineGap=10)

# Draw detected lines on the image
if lines is not None:
    for line in lines:
        x1, y1, x2, y2 = line[0]
        cv2.line(image, (x1, y1), (x2, y2), (0, 255, 0), 2)

# Display the result image
cv2.imshow('Image with Detected Lines', image)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Perform OCR on the image using pytesseract
ocr_text = pytesseract.image_to_string(gray)

# Print the extracted text
print(ocr_text)