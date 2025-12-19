feet_inches = input("Enter feet and inches: ")

def parse(feetinches):
    parts = feetinches.split(" ")
    feet = float(parts[0])
    inches = float(parts[1])
    return feet, inches

def convert(feet, inches):
    return feet * 0.3048 + inches * 0.0254

# feet_inches_tuple = parse(feet_inches)
f,i = parse(feet_inches)
# print(feet_inches_tuple)

# result = convert(feet_inches_tuple[0], feet_inches_tuple[1])
result = convert(f, i)

if result < 1:
    print("Kid is too small.")
else:
    print("Kid can use the slide.")