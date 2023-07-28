greeting = input("Greeting: ")

if "hello" in greeting.lower():
    print("$0")
elif "h" in greeting.lower():
    print("$20")
else:
    print("$100")