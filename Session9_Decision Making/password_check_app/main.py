password = input("Enter your password: ")
result = {}

# check the length of the password

if len(password) >= 8:
    result["length"] = True
else:
    result["length"] = False

# check if the password content number

digit= False
for i in password:
    if i.isdigit():
        digit = True
result["digits"] = digit

# check if contain Capitailize
uppercase = False
for c in password:
    if c.isupper():
        upper = True

result["upper-case"] = uppercase

print(result)
if all(result.values()):
    print("Strong Password")
else:
    print("Weak Password")
