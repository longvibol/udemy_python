import csv

with open("weather.csv",'r') as file:
    data = list(csv.reader(file))

city = input("Enter City: ")
# print(data)
for row in data[1:]:
    # dat[1:] = we skip the header
    if row[0] == city:
        print(f"{row[1]} - {row[2]}")