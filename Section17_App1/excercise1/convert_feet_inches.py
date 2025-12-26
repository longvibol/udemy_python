def feet_inches_to_meters(feet, inches):
    feet = float(feet)
    inches = float(inches)

    total_inches = (feet * 12) + inches
    meters = total_inches * 0.0254
    return meters


if __name__ == '__main__':
    a=feet_inches_to_meters(3, 4)
    print(a)