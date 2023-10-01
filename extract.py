import cv2
import numpy as np
import pytesseract
def main():
    data = []
    image = cv2.imread('temp.jpg')
    pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 200, 250, cv2.THRESH_BINARY_INV)
    # cv2.imshow('Image with Detected Rectangles', binary)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    # cv2.imwrite("out1.jpg",binary)
    
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    text=""
    rectangles = []
    custom_config = r'--psm 6'
    for contour in contours:
        perimeter = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.01 * perimeter, True)
        # if len(approx) == 4:
        rectangles.append(approx)
    for rectangle in reversed(rectangles):
        x, y, w, h = cv2.boundingRect(rectangle)
        if w < 300:
            continue

        text_region = gray[y:y+h, x:x+w]
        extracted_text = pytesseract.image_to_string(text_region,config=custom_config)
        data.append(extracted_text)
        text+=extracted_text
        cv2.drawContours(image, [rectangle], -1, (0, 255, 0), 2)

    # cv2.imshow('Image with Detected Rectangles', image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    # cv2.imwrite("out.jpg",image)
    return data