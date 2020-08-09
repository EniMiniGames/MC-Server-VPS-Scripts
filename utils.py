import sys
import os


def usage(script_name: str, file_name: str, arg: str, problem: str):
    usage_str = f"{script_name} <path to directory containing {file_name} OR path to {file_name}>"
    print(f"Usage: {usage_str}\nInstead got: {script_name} {arg}")
    print(f"{problem}")
    exit(1)


def validate_file_path(filename: str):
    args = sys.argv
    if (len(args)) <= 1:
        usage(args[0], "", "No argument was given to the utility")

    path = args[1]
    is_dir = os.path.isdir(path)
    is_file = os.path.isfile(path)

    if not (is_dir or is_file):
        usage(args[0], filename, str(path), f"{path} either doesn't exist, or is some special device file")

    if is_dir:
        path += f"/{filename}"

    if not os.path.isfile(path):
        usage(args[0], filename, str(path), f"{path} does not exist.")

    return path
