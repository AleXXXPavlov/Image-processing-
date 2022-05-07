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
    if np.mean(new_img) > DARK_BORDER:
        new_img = np.bitwise_not(new_img)

    # contrast control
    contrast = 1.5
    for h in range(height):
        for w in range(weight):
            new_img[h, w] = np.clip(new_img[h, w] * contrast, 0, 255)

    # Otsu's thresholding after Gaussian filtering
    # new_img = cv2.GaussianBlur(new_img, (3, 3), 0)
    _, threshold_img = cv2.threshold(new_img, 250, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # dilate the text to make it solid spot
    cpy = threshold_img.copy()
    struct = cv2.getStructuringElement(cv2.MORPH_RECT, (10, 10))
    cpy = cv2.dilate(~cpy, struct, iterations=3)
    threshold_img = ~cpy

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


def find_lines(boxes: list) -> tuple:
    cols, rows = dict(), dict()
    # group the bounding boxes by their positions
    for box in boxes:
        y = box[1]
        row = y // THRESHOLD_CELL
        rows[row] = rows[row] + [box] if row in rows else [box, ]

    # create horizontal lines
    horizontal_lines = []

    rows = rows.values()
    # sort by x-coord
    rows = [sorted(row) for row in rows]
    # sort by y-coord
    rows = sorted(rows, key=lambda r: r[0][1])

    for row in rows:
        bottom = max([letter[3] + letter[1] for letter in row])
        top = min([letter[1] for letter in row])

        left, right = row[0][0], row[-1][0] + row[-1][2]
        horizontal_lines.append((left, top, right, top))
        horizontal_lines.append((left, bottom, right, bottom))

    return horizontal_lines, []


def recognition(input_file: str, output_file: str) -> None:
    input_img = cv2.imread(input_file)
    # img_with_markup = input_img.copy()

    # initial improvement
    threshold_img = improvement(input_img)
    cv2.imwrite(output_file, threshold_img)
    exit()
    # get bounding boxes
    bounding_boxes = find_bounding_boxes(threshold_img)

    # create vertical and horizontal lines
    lines = find_lines(bounding_boxes)

    # visualize the result
    for same_lines in lines:
        for line in same_lines:
            x_l, y_l, x_r, y_r = line
            cv2.line(img_with_markup, (x_l, y_l), (x_r, y_r), GREEN, THICKNESS)

    # visualize the result
    #for box in bounding_boxes:
    #    x, y, width, height = box

        # draw a rectangle on image
    #    cv2.rectangle(img_with_markup, (x - 1, y - 1), (x + width, y + height), GREEN, THICKNESS)

    cv2.imwrite(output_file, img_with_markup)
