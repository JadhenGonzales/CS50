greeting = input("Greeting: ")

if greeting.strip().lower().startswith("hello"):
    print("$0")
elif greeting.strip().lower().startswith("h"):
    print("$20")
else:
    print("$100")