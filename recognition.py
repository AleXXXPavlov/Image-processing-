import cv2
import imutils
import numpy as np

from PIL import Image
from pytesseract import pytesseract

from constants import *


def improvement(img: Image) -> Image:
    # magnifying the image can help improve detection results
    new_img = imutils.resize(img, width=M_WIDTH)
    height, weight = img.shape[0], img.shape[1]

    # converting a color image to grayscale for easy processing
    new_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # we achieve an average value less than 127
    if np.mean(new_img) < DARK_BORDER:
        img_gray = np.bitwise_not(new_img)

    # contrast control
    contrast = 1.5
    for h in range(height):
        for w in range(weight):
            new_img[h, w] = np.clip(new_img[h, w] * contrast, 0, 255)

    # Otsu's thresholding after Gaussian filtering
    new_img = cv2.GaussianBlur(new_img, (3, 3), 0)
    _, threshold_img = cv2.threshold(new_img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    return threshold_img


def simple_recognition(input_file: str, output_file: str) -> None:
    input_img = cv2.imread(input_file)

    # initial improvement
    threshold_img = improvement(input_img)

    # simple test
    data = pytesseract.image_to_string(threshold_img, lang="rus", config='--psm 11')
    with open(output_file, mode="w", encoding="utf-8") as res_file:
        res_file.write(data)


def find_bounding_boxes(img: Image) -> list:
    # get image contours
    contours, _ = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # draw an approximate rectangle around the image, use - straight bounding rectangle
    bounding_boxes = []
    for contour in contours:
        bounding_boxes.append(cv2.boundingRect(contour))

    return bounding_boxes


def recognition(input_file: str, output_file: str) -> None:
    input_img = cv2.imread(input_file)
    img_with_markup = input_img.copy()

    # initial improvement
    threshold_img = improvement(input_img)
    # get bounding boxes
    bounding_boxes = find_bounding_boxes(threshold_img)

    # visualize the result
    for box in bounding_boxes:
        x, y, width, height = box

        # draw a rectangle on image
        cv2.rectangle(img_with_markup, (x-1, y-1), (x+width, y+height), GREEN, THICKNESS)

    cv2.imwrite(output_file, img_with_markup)
