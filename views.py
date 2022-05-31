from components.models import CoreEngine
from logbox_framework.templator import render

core = CoreEngine()


class Index:
    def __call__(self):
        return '200 OK', render('index.html', objects_list=core.categories)


class About:
    def __call__(self):
        return '200 OK', render('about.html')


class Boards:
    def __call__(self, request):
        try:
            category = core.find_category(int(request['request_params']['id']))
            return '200 OK', render('boards.html', objects_list=category.boards, name=category.name, id=category.id)
        except KeyError:
            return '200 OK', 'There no any boards yet'


class CreateBoard:
    category_id = -1

    def __call__(self, request):

        if request['method'] == 'POST':
            type_ = core.decode_value(request['data']['type'])
            name = core.decode_value(request['data']['name'])
            category = None
            if self.category_id != -1:
                category = core.find_category(int(self.category_id))
                board = core.create_board(type_, name, category)
                core.boards.append(board)
            return '200 OK', render('boards.html', objects_list=category.boards, name=category.name, id=category.id)


class CreateCategory:
    def __call__(self, request):
        if request['method'] == 'POST':
            name = core.decode_value(request['data']['name'])
            category_id = request['data'].get('id')
            category = None

            if category_id:
                category = core.find_category(int(category_id))
            new_category = core.create_category(name, category)
            core.categories.append(new_category)

            return '200 OK', render('index.html', object_list=core.categories)
        else:
            categories = core.categories
            return '200 OK', render('create_category.html', categories=categories)


class CategoryList:
    def __call__(self, request):
        return '200 OK', render('category_list.html', objects_list=core.categories)
