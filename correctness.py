from os.path import exists


def check_input(input_file: str) -> str:
    error_message = ""

    # extension check
    if input_file[-4:] != ".png":
        error_message = "ERROR: The input file is not a png image."
    # existence check
    if not error_message and not exists(input_file):
        error_message = "ERROR: No such input file exists."

    return error_message


def check_output(output_file: str) -> str:
    error_message = ""

    try:
        with open(output_file, mode="w", encoding="utf-8") as file:
            pass
    except FileNotFoundError:
        error_message = "ERROR: There is no directory to save the output file."

    return error_message


def check_correctness(input_file: str, output_file: str) -> bool:
    input_error = check_input(input_file)
    if input_error:
        print(input_error)
        return False

    output_error = check_output(output_file)
    if output_error:
        print(output_error)
        return False

    return True
