import cv2
import imutils

from PIL import Image
from pytesseract import pytesseract


def improvement(img: Image) -> Image:
    # magnifying the image can help improve detection results
    image = imutils.resize(img, width=700)

    # converting a color image to grayscale for easy processing
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Otsu's thresholding after Gaussian filtering
    blur = cv2.GaussianBlur(img_gray, (3, 3), 0)
    _, threshold_img = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    return threshold_img


def simple_recognition(threshold_img: str, output_file: str) -> None:
    # simple test
    data = pytesseract.image_to_string(threshold_img, lang="rus", config='--psm 11')

    with open(output_file, mode="w", encoding="utf-8") as res_file:
        res_file.write(data)


def recognition(input_file: str, output_file: str) -> None:
    input_img = cv2.imread(input_file)

    # initial improvement
    threshold_img = improvement(input_img)

    # ...


