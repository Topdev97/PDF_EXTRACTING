import cv2
import numpy as np
import pytesseract
import random

def mainF():
    data = []
    image = cv2.imread('temp.jpg')
    pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
    # cv2.imshow('Image with Detected Rectangles', binary)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    # cv2.imwrite("out1.jpg", binary)

    contours, _ = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    text = ""
    rectangles = []
    for i in reversed(contours):
        x, y, w, h = cv2.boundingRect(i)
        if w < 300 or h < 20:
            continue
        rectangles.append(i)
    rectangles = rectangles[:-1]
    # for contour in contours:
    #     perimeter = cv2.arcLength(contour, True)
    #     approx = cv2.approxPolyDP(contour, 0.01 * perimeter, True)
    #     rectangles.append(approx)
    # print(len(rectangles))
    imgCpy = image.copy()

    for index,j in enumerate(rectangles):
        x, y, w, h = cv2.boundingRect(j)
        text_region = gray[y:y+h, x:x+w]
        extracted_text = pytesseract.image_to_string(text_region)
        data.append(extracted_text)
        text += extracted_text
    # cv2.imshow('Image with Detected Rectangles', imgCpy)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    # cv2.imwrite("out.jpg", imgCpy)
    # print(text)
    return data
