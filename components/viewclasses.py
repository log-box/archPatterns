from logbox_framework.templator import render


# Base CBV class
class TemplateView:
    template_name = 'template.html'

    def get_contex_data(self):
        return {}

    def get_template(self):
        return self.template_name

    def render_template_with_context(self):
        template_name = self.get_template()
        context = self.get_contex_data()
        return '200 OK', render(template_name, **context)

    def __call__(self, request):
        return self.render_template_with_context()


# CBV List display controller
class ListView(TemplateView):
    queryset = []
    template_name = 'list.html'
    context_object_name = 'objects_list'

    def get_queryset(self):
        print(self.queryset)
        return self.queryset

    def get_contex_object_name(self):
        return self.context_object_name

    def get_contex_data(self):
        queryset = self.get_queryset()
        contex_object_name = self.get_contex_object_name()
        contex = {contex_object_name: queryset}
        return contex


# CBV object create controller
class CreateView(TemplateView):
    template_name = 'create.html'

    @staticmethod
    def get_request_data(request):
        return request['data']

    def create_obj(self, data):
        pass

    def __call__(self, request):
        if request['method'] == 'POST':
            data = self.get_request_data(request)
            self.create_obj(data)

            return self.render_template_with_context()
        else:
            return super().__call__(request)
