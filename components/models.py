import quopri


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

    @classmethod
    def create(cls, type_):
        return cls.types[type_]


class Board:
    def __init__(self, name, category):
        self.name = name
        self.category = category
        self.category.boards.append(self)


class Category:
    category_id = 0

    def __init__(self, name, category):
        self.name = name
        self.id = Category.category_id
        Category.category_id += 1
        self.category = category
        self.boards = []


class PublicBoard(Board):
    pass


class PrivateBoard(Board):
    pass


class BoardFactory:
    types = {
        'public': PublicBoard,
        'private': PrivateBoard,
    }

    @classmethod
    def create(cls, type_, name, category):
        return cls.types[type_](name, category)


class CoreEngine:
    def __init__(self):
        self.guest = []
        self.register = []
        self.admin = []
        self.boards = []
        self.categories = []

    @staticmethod
    def create_user(type_):
        return UserFactory.create(type_)

    @staticmethod
    def create_category(name, category=None):
        return Category(name, category)

    def find_category(self, id):
        for item in self.categories:
            if item.id == id:
                return item

    @staticmethod
    def create_board(type_, name, category):
        return BoardFactory.create(type_, name, category)

    def get_board(self, name):
        for item in self.boards:
            if item.name == name:
                return item
        return None

    @staticmethod
    def decode_value(value):
        value_b = bytes(value.replace('%', '=').replace('+', ''), 'UTF-8')
        value_decode_str = quopri.decodestring(value_b)
        return value_decode_str.decode('UTF-8')
