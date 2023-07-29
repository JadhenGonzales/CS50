from pyfiglet import Figlet
import sys
import random

def main():
    figlet = Figlet()

    if len(sys.argv) != 1 and len(sys.argv) != 3:
        print("Usage: python figlet.py (-f or --font) (font name) or no arguments for random font")
        sys.exit(1)

    if len(sys.argv) == 3:
        if sys.argv[1] != "-f" and sys.argv[1] != "--font":
            print("Usage: python figlet.py (-f or --font) (font name) or no arguments for random font")
            sys.exit(1)
        font_choice = sys.argv[2]

    if len(sys.argv) == 1:
        font_choice = random.choice(figlet.getFonts())

    word = input("word: ")
    figlet.setFont(font=font_choice)
    print(figlet.renderText(word))


main()



