import cs50
import re
import math


def main():

    card_number = cs50.get_int("Number: ")
    card_type = check_type(str(card_number))

    if not valid(card_number):
        card_type = "INVALID"

    print(card_type)


def check_type(card_number):
    # RegEx of the 3 different card types
    amex = re.match('34\d{13,13}|37\d{13,13}', card_number)
    mastercard = re.match('5[1-5]\d{14,14}', card_number)
    visa = re.match('4\d{12,12}|4\d{15,15}', card_number)

    if amex:
        card_type = "AMEX"
    elif mastercard:
        card_type = "MASTERCARD"
    elif visa:
        card_type = "VISA"
    else:
        card_type = "INVALID"

    return card_type


def valid(card_number):
    # Luhn's algorithm
    sum = 0
    for i in range(int(math.log10(card_number) + 1)):
        # get the last digit and multiple by 2 every other digit
        d = card_number % 10
        if i % 2 == 0:
            sum += d
        else:
            if (d * 2) < 10:
                sum += (d * 2)
            else:
                sum += ((d * 2) % 10) + 1
        # iterate to the second to the last digit
        card_number = int(card_number / 10)

    if sum % 10 == 0:
        return True
    else:
        return False

if __name__ == "__main__":
    main()
