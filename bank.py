greeting = input("Greeting: ")

if greeting.lower().startswith("hello"):
    print("$0")
elif greeting[0].lower() == "h":
    print("$20")
else:
    print("$100")