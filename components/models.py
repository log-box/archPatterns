class User:
    pass


class Guest(User):
    pass


class Registered(User):
    pass


class Admin(User):
    pass


class UserFactory:
    types = {
        'guest': Guest,
        'registered': Registered,
        'admin': Admin,
    }

