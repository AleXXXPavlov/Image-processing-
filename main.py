import cv2
import argparse

from PIL import Image
from pytesseract import pytesseract

from correctness import check_correctness


def parse_args() -> tuple:
    parser = argparse.ArgumentParser(description="Recognize text in image.")
    parser.add_argument(
        "text_line_drawer",
        choices={"opencv", "tesseract"},
        help="Image Processing Library"
    )
    parser.add_argument(
        "input_file",
        type=str,
        help="Path to input document",
    )
    parser.add_argument(
        "output_file",
        type=str,
        help="Path to output document"
    )

    args = parser.parse_args()
    return args.input_file, args.output_file, args.text_line_drawer


def create_png(input_file: str, output_file: str) -> None:
    input_img = cv2.imread(input_file)


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


if __name__ == "__main__":
    # parse args for recognizing
    input_file, output_file, drawer = parse_args()

    # checking the correctness of the entered data
    check_res = check_correctness(input_file, output_file)

    if check_res:
        # recognizing data
        recognizing(drawer, input_file, output_file)


