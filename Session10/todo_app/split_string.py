feet_inches = input("Enter feet and inches: ")

def convert(feet_inch):
    parts = feet_inch.split(" ")
    feet = float(parts[0])
    inches = float(parts[1])
    return feet * 0.3048 + inches * 0.0254


result = convert(feet_inches)

if result < 1:
    print("Kid is too small.")
else:
    print("Kid can use the slide.")
