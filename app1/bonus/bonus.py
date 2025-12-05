country = "USAs"
while True:
    match country:
        case "USA" | "United States":
            print("Hello")
            break
        case "Italy":
            print("Ciao")
        case "Germany":
            print("Hallo")
