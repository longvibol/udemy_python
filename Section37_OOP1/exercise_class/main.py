class User:

    def __init__(self, name, brithyear):
        self.name = name
        self.brithyear = brithyear


    def get_name(self):
        return self.name.upper()

    def age(self, current_year):
        age = current_year - self.brithyear
        return age

jonh = User("Jonh", 1999)

print(jonh.age(2026))
print(jonh.get_name())