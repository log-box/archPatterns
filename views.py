from components.models import CoreEngine
from logbox_framework.templator import render

core = CoreEngine()


class Index:
    def __call__(self):
        return '200 OK', render('index.html', objects_list=core.categories)


class About:
    def __call__(self):
        return '200 OK', render('about.html')


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
            return '200 OK', render('index.html', categories=categories)
