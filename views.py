from components.decorators import debug, AppRoute
from components.models import CoreEngine
from logbox_framework.templator import render

core = CoreEngine()
routes = {}


@AppRoute(routes=routes, url='/')
class Index:
    def __call__(self, request):
        return '200 OK', render('index.html', objects_list=core.categories)


@AppRoute(routes=routes, url='/about/')
class About:
    def __call__(self, request):
        return '200 OK', render('about.html')


@AppRoute(routes=routes, url='/boards/')
class Boards:
    def __call__(self, request):
        try:
            category = core.find_category(int(request['request_params']['id']))
            return '200 OK', render('boards.html', objects_list=category.boards, name=category.name, id=category.id)
        except KeyError:
            return '200 OK', 'There no any boards yet'


@AppRoute(routes=routes, url='/create-board/')
class CreateBoard:
    category_id = -1

    def __call__(self, request):

        if request['method'] == 'POST':
            print(request)
            type_ = core.decode_value(request['data']['type'])
            name = core.decode_value(request['data']['name'])
            category = None
            if self.category_id != -1:
                category = core.find_category(int(self.category_id))
                board = core.create_board(type_, name, category)
                core.boards.append(board)
            return '200 OK', render('boards.html', objects_list=category.boards, name=category.name, id=category.id)
        else:
            try:
                self.category_id = int(request['request_params']['id'])
                category = core.find_category(int(self.category_id))

                return '200 OK', render('create_board.html', name=category.name, id=category.id)
            except KeyError:
                return '200 Ok', 'There no category and boards added yet'


@AppRoute(routes=routes, url='/create-category/')
class CreateCategory:
    @debug
    def __call__(self, request):
        if request['method'] == 'POST':
            name = core.decode_value(request['data']['name'])
            category_id = request['data'].get('id')
            category = None

            if category_id:
                category = core.find_category(int(category_id))
            new_category = core.create_category(name, category)
            core.categories.append(new_category)

            return '200 OK', render('index.html', objects_list=core.categories)
        else:
            categories = core.categories
            return '200 OK', render('create_category.html', categories=categories)


@AppRoute(routes=routes, url='/category-list/')
class CategoryList:
    def __call__(self, request):
        return '200 OK', render('category_list.html', objects_list=core.categories)
