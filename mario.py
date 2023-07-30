# TODO


def main():
    size = get_int("Height: ")
    print_pyramid(size)


def get_int(text):
    while True:
        try:
            value = int(input(text))
        except ValueError:
            pass
        else:
            if value < 1 or value > 8:
                pass
            else:
                return value


def print_pyramid(size):
    for i in range(1, size + 1):
        print(f" " * (size - i), "#" * i, "  ", "#" * i, sep="")


if __name__ == "__main__":
    main()
