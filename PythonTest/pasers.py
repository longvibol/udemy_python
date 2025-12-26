def parse(feetinches):
    parts = feetinches.split(" ")
    feet = float(parts[0])
    inches = float(parts[1])
    return feet, inches
