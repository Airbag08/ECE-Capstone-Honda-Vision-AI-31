while True:
    path = input('Enter a Windows path (or type "quit" to exit): ').strip().strip('"')

    if path.lower() == "quit":
        break

    converted = "file:///" + path.replace("\\", "/")
    print("Converted path (Ctrl + Shift + C):", converted)
    print()