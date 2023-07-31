# TODO
import cs50
import re


def main():
    text = cs50.get_string("Text: ")
    # Coleman-Liau index
    letters = len(re.findall(r"[a-z]", text, flags=re.I))
    words = len(re.findall(r"[a-z'-]+", text, flags=re.I))
    sentences = len(re.findall(r"[a-z ]+[.?!]", text))

    index = (
        (0.0588 * (letters * 100.0 / words))
        - (0.296 * (sentences * 100.0 / words))
        - 15.8
    )

    if index < 1:
        print("Before Grade 1")
    elif index >= 16:
        print("Grade 16+")
    else:
        index = round(index)
        print(f"Grade {index}")


if __name__ == "__main__":
    main()
