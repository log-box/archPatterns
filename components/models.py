import quopri


class User:
    def __init__(self, name):
        self.name = name


class Guest(User):
    def __init__(self, name):
        super().__init__(name)
        self.boards = []


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
    def create(cls, type_, name):
        return cls.types[type_](name)


class Board:
    def __init__(self, name, category):
        self.name = name
        self.category = category
        self.category.boards.append(self)
        self.guests = []
        super().__init__()

    def __iter__(self, item):
        return self.guests[item]

    def add_guest_to_board(self, guest: Guest):
        self.guests.append(guest)
        guest.boards.append(self)


class Category:
    category_id = 0

    def __init__(self, name, category, child_category=None):
        self.name = name
        self.id = Category.category_id
        Category.category_id += 1
        self.category = category
        self.boards = []
        self.parent_category = None
        self.child_category = child_category

    def __iter__(self, item):
        return self.category[item]

    def boards_count(self):
        result = len(self.boards)
        if self.category:
            result += self.category.course_count()
        return result


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
        self.guests = []
        self.register = []
        self.admin = []
        self.boards = []
        self.categories = []

    @staticmethod
    def create_user(type_, name):
        return UserFactory.create(type_, name)

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

    def get_guest(self, name):
        for item in self.guests:
            if item.name == name:
                return item
        return None

    @staticmethod
    def decode_value(value):
        value_b = bytes(value.replace('%', '=').replace('+', ''), 'UTF-8')
        value_decode_str = quopri.decodestring(value_b)
        return value_decode_str.decode('UTF-8')
