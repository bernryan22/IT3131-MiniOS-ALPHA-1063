import os


def clear_screen():
    """Clear the terminal screen on Windows (CMD) or other terminals."""
    os.system("cls" if os.name == "nt" else "clear")


def print_title(title: str, width: int = 48):
    """Print a simple boxed section title."""
    print("=" * width)
    print(title.center(width))
    print("=" * width)


def print_error(message: str):
    print(f"Error: {message}")


def print_success(message: str):
    print(message)
