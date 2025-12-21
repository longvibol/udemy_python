import glob

keyfile = glob.glob("files/*.txt")

for filepath in keyfile:
    with open(filepath,'r') as file:
        print(file.read().upper())

