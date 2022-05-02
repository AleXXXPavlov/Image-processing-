import cv2
import argparse

from PIL import Image
from pytesseract import pytesseract


def parse_args() -> argparse.Namespace:
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

    recognizing_args = parser.parse_args()
    return recognizing_args


def create_png(input_img: Image, output_file: str) -> None:
    pass


def create_txt(input_img: Image, output_file: str) -> None:
    pass


def recognizing() -> None:
    args = parse_args()

    input_img = Image.open(args.input_file)
    output_file = args.output_file

    if args.text_line_drawer == "opencv":
        create_png(input_img, output_file)
    elif args.test_line_drawer == "tesseract":
        create_txt(input_img, output_file)


if __name__ == "__main__":
    recognizing()


