from components.decorators import debug, AppRoute
from components.models import CoreEngine
from components.viewclasses import ListView, CreateView
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


# Controller list of guests
@AppRoute(routes=routes, url='/guests-list/')
class GuestsListView(ListView):
    queryset = core.guests
    template_name = 'guests_list.html'


# Controller guest create
@AppRoute(routes=routes, url='/create-guest/')
class GuestCreateView(CreateView):
    template_name = 'create_guest.html'

    def create_obj(self, data: dict):
        name = data['name']
        name = core.decode_value(name)
        # пока хардкодим и создаем только гостей
        new_obj = core.create_user('guest', name)
        core.guests.append(new_obj)


# Controller guest add
@AppRoute(routes=routes, url='/add-guest/')
class AddGuestToBoardCreateView(CreateView):
    template_name = 'add_guest.html'

    def get_context_data(self):
        context = super().get_context_data()
        context['boards'] = core.boards
        context['guests'] = core.guests
        return context

    def create_obj(self, data: dict):
        board_name = data['board_name']
        board_name = core.decode_value(board_name)
        board = core.get_board(board_name)
        guest_name = data['guest_name']
        guest_name = core.decode_value(guest_name)
        guest = core.get_guest(guest_name)
        board.add_guest_to_board(guest)
