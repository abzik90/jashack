class User:
    #A user object
    def __init__(self, email, name, surname):
        self.email = email
        self.name = name
        self.surname = surname
    def __repr__(self):
        return f"({self.email},'{self.name}','{self.surname}')"

    def __str__(self):
        return f"({self.email},'{self.name}','{self.surname}')"
