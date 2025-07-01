#!/usr/bin/env python3
import sys
import subprocess
import platform
import re


def print_usage():
    """Print usage instructions."""
    script_name = sys.argv[0]
    print(f"Usage: {script_name} <quote type> [no-brackets]")
    print("Example: y 0 -> [1, 2, 3, 4, a, b, c]")
    print("Example: y 1 -> ['1', '2', '3', '4', 'a', 'b', 'c']")
    print('Example: y 2 -> ["1", "2", "3", "4", "a", "b", "c"]')
    print("Example: y 0 no-brackets -> 1, 2, 3, 4, a, b, c")


def get_clipboard_content():
    """Read content from clipboard based on the operating system."""
    system = platform.system()

    if system == "Darwin":  # macOS
        try:
            return subprocess.check_output(["pbpaste"]).decode("utf-8").strip()
        except subprocess.CalledProcessError:
            print("Failed to get clipboard content using pbpaste.")
            sys.exit(1)
    elif system == "Linux":
        try:
            return (
                subprocess.check_output(["xclip", "-o", "-selection", "clipboard"])
                .decode("utf-8")
                .strip()
            )
        except subprocess.CalledProcessError:
            print("Failed to get clipboard content using xclip.")
            sys.exit(1)
        except FileNotFoundError:
            print(
                "xclip is not installed. Please install it to use this script on Linux."
            )
            sys.exit(1)
    elif system == "Windows":
        try:
            import pyperclip

            return pyperclip.paste()
        except ImportError:
            print("pyperclip module not found. Install it with: pip install pyperclip")
            sys.exit(1)

    print(f"Clipboard operations not supported on {system}.")
    sys.exit(1)


def set_clipboard_content(text):
    """Write content to clipboard based on the operating system."""
    system = platform.system()

    if system == "Darwin":  # macOS
        try:
            process = subprocess.Popen(["pbcopy"], stdin=subprocess.PIPE)
            process.communicate(text.encode("utf-8"))
        except subprocess.CalledProcessError:
            print("Failed to set clipboard content using pbcopy.")
            return False
    elif system == "Linux":
        try:
            process = subprocess.Popen(
                ["xclip", "-selection", "clipboard"], stdin=subprocess.PIPE
            )
            process.communicate(text.encode("utf-8"))
        except subprocess.CalledProcessError:
            print("Failed to set clipboard content using xclip.")
            return False
        except FileNotFoundError:
            print(
                "xclip is not installed. Please install it to use this script on Linux."
            )
            return False
    elif system == "Windows":
        try:
            import pyperclip

            pyperclip.copy(text)
        except ImportError:
            print("pyperclip module not found. Install it with: pip install pyperclip")
            return False
    else:
        print(f"Clipboard operations not supported on {system}.")
        return False

    return True


def main():
    # Check if correct number of arguments
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print_usage()
        sys.exit(1)

    # Parse and validate the quote type
    quote_type = sys.argv[1]
    if not re.match(r"^[0-2]$", quote_type):
        print("Please provide quote as 0, 1, or 2.")
        sys.exit(1)

    quote_type = int(quote_type)

    # Check if no-brackets option is specified

    # Set the quote character based on the quote type
    quote_chars = {0: "", 1: "'", 2: '"'}
    quote = quote_chars[quote_type]

    # Get clipboard content
    input_text = get_clipboard_content()

    elements = [item.strip() for item in input_text.split("\n") if item.strip()]

    processed_elements = [f"{quote}{element}{quote}" for element in elements]

    # Get unique elements
    unique_elements = set(processed_elements)

    # Print the results
    print(f"\nelements: {len(processed_elements)}")
    print(f"unique elements: {len(unique_elements)}")

    result_string = ", ".join(processed_elements)

    print(result_string)

    # Copy the result string back to clipboard
    if set_clipboard_content(result_string):
        print("\nResult copied to clipboard.")


if __name__ == "__main__":
    main()
