class User:
    def __init__(self, name, birthday):
        self.name = name
        self.birthday = birthday

    def get_name(self):
        capitalize = self.name = self.name.upper()
        return capitalize
    def age(self, current_year):
        age = current_year - self.birthday
        return age

user = User("john", 1999)

print(f"{user.get_name()}:{user.age(2023)}")


