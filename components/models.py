import quopri
import sqlite3


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


class GuestMapper:
    def __init__(self, connection, table_name='guests'):
        self.connection = connection
        self.cursor = connection.cursor()
        self.table_name = table_name

    def all(self):
        statement = f'SELECT * from {self.table_name}'
        self.cursor.execute(statement)
        result = []
        for item in self.cursor.fetchall():
            id, name = item
            guest = Guest(name)
            guest.id = id
            result.append(guest)
        return result

    def find_by_id(self, id):
        statement = f"SELECT id, name FROM {self.table_name} WHERE id=?"
        self.cursor.execute(statement, (id,))
        result = self.cursor.fetchone()
        if result:
            return Guest(*result)
        else:
            raise ItemNotFoundException(f'record with id={id} not found')

    def insert(self, obj):
        statement = f"INSERT INTO {self.table_name} (name) VALUES (?)"
        self.cursor.execute(statement, (obj.name,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbCommitException(e.args)

    def update(self, obj):
        statement = f"UPDATE {self.table_name} SET name=? WHERE id=?"
        self.cursor.execute(statement, (obj.name, obj.id))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbUpdateException(e.args)

    def delete(self, obj):
        statement = f"DELETE FROM {self.table_name} WHERE id=?"
        self.cursor.execute(statement, (obj.id,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbDeleteException(e.args)


connection = sqlite3.connect('framework_board.sqlite')


class MapperRegistry:
    mappers = {
        'guest': GuestMapper,
    }

    @staticmethod
    def get_mapper(obj):
        if isinstance(obj, Guest):
            return GuestMapper(connection)

    @staticmethod
    def get_current_mapper(name):
        return MapperRegistry.mappers[name](connection)


class DbCommitException(Exception):
    def __init__(self, message):
        super().__init__(f'Db commit error: {message}')


class DbUpdateException(Exception):
    def __init__(self, message):
        super().__init__(f'Db update error: {message}')


class DbDeleteException(Exception):
    def __init__(self, message):
        super().__init__(f'Db delete error: {message}')


class ItemNotFoundException(Exception):
    def __init__(self, message):
        super().__init__(f'Record not found: {message}')


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
