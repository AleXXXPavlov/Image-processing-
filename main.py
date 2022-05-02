import argparse

from correctness import check_correctness
from recognizing import recognizing


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


if __name__ == "__main__":
    # parse args for recognizing
    input_file, output_file, drawer = parse_args()

    # checking the correctness of the entered data
    check_res = check_correctness(input_file, output_file)

    if check_res:
        # recognizing data
        recognizing(drawer, input_file, output_file)
