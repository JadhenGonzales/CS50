def main():
    menu = {
        "Baja Taco": 4.00,
        "Burrito": 7.50,
        "Bowl": 8.50,
        "Nachos": 11.00,
        "Quesadilla": 8.50,
        "Super Burrito": 8.50,
        "Super Quesadilla": 9.50,
        "Taco": 3.00,
        "Tortilla Salad": 8.00
    }

    total_cost = 0

    while True:
        try:
            total_cost += menu[input("Item: ").title()]
        except EOFError:
            print("")
            break
        except KeyError:
            pass
        else:
            print(f"Total: ${total_cost:.2f}")


main()



