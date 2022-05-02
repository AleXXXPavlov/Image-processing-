import cv2

from PIL import Image
from pytesseract import pytesseract


def create_png(input_file: str, output_file: str) -> None:
    input_img = cv2.imread(input_file)

    # converting a color image to grayscale for easy processing
    img_gray = cv2.cvtColor(input_img, cv2.COLOR_BGR2GRAY)

    # Otsu's thresholding after Gaussian filtering
    blur = cv2.GaussianBlur(img_gray, (5, 5), 0)
    _, threshold_img = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # structural elements method in OpenCV with kernel frequency depending on text area
    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (12, 12))

    # getting text borders
    dilation = cv2.dilate(threshold_img, rect_kernel, iterations=3)

    # getting the area of white pixels
    contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL,
                                           cv2.CHAIN_APPROX_NONE)

    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        # draw a bounding box on the text area
        rect = cv2.rectangle(input_img, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # save changes
        cv2.imwrite(output_file, rect)


def create_txt(input_file: str, output_file: str) -> None:
    input_img = Image.open(input_file)
    text = pytesseract.image_to_string(input_img)

    with open(output_file, mode="w", encoding="utf-8") as res_file:
        res_file.write(text)


def recognizing(drawer: str, input_file: str, output_file: str) -> None:
    if drawer == "opencv":
        create_png(input_file, output_file)
    elif drawer == "tesseract":
        create_txt(input_file, output_file)
