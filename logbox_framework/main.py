import logging
import quopri
from os import path

from components.content_types import CONTENT_TYPES_MAP
from components.decorators import logging
from logbox_framework.rest_methods import GetRequests, PostRequests


class PageNotFound404:
    def __call__(self):
        return '404 ', 'PAGE Not Found 404'


class Framework:
    """
    The base class
    """

    def __init__(self, settings, route_lst):
        self.settings = settings
        self.route_lst = route_lst
        # self.logger = logging.getLogger(__name__)
        # self.logger.setLevel(logging.WARNING)
        # logger_handler = logging.FileHandler('framework.log')
        # logger_handler.setLevel(logging.WARNING)
        # logger_formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
        # logger_handler.setFormatter(logger_formatter)
        # self.logger.addHandler(logger_handler)
        # self.logger.info('Настройка логгирования окончена!')


    @logging
    def __call__(self, environ, start_response):
        # pprint(environ)

        path = environ['PATH_INFO']
        if not path.endswith('/'):
            path = f'{path}/'

        request = {'method': environ['REQUEST_METHOD']}

        # get request params or/and data
        if request['method'] == 'GET':
            request['request_params'] = GetRequests().get_request_params(environ)
        if request['method'] == 'POST':
            request['data'] = Framework.decode(PostRequests.get_request_data(environ))


        # Находим нужный контроллер
        if path in self.route_lst:
            view = self.route_lst[path]
            content_type = self.get_content_type(path)
            code, body = view(request)
            body = body.encode('utf-8')

        elif path.startswith(self.settings.STATIC_URL):
            # /static/images/logo.jpg/ -> images/logo.jpg
            file_path = path[len(self.settings.STATIC_URL):len(path)-1]
            print(file_path)
            content_type = self.get_content_type(file_path)
            print(content_type)
            code, body = self.get_static(self.settings.STATIC_FILES_DIR,
                                         file_path)

        else:
            view = PageNotFound404()
            content_type = self.get_content_type(path)
            code, body = view(request)
            body = body.encode('utf-8')
        start_response(code, [('Content-Type', content_type)])

        return [body]


    @staticmethod
    def decode(data):
        decode_data = {}
        for key, value in data.items():
            temp_val = bytes(value.replace('%', '=').replace('+', ''), 'UTF-8')
            decode_value = quopri.decodestring(temp_val).decode('UTF-8')
            decode_data[key] = decode_value
        # print(decode_data)
        return decode_data

    @staticmethod
    def get_content_type(file_path, content_types_map=CONTENT_TYPES_MAP):
        file_name = path.basename(file_path).lower() # styles.css
        extension = path.splitext(file_name)[1] # .css
        print(extension)
        return content_types_map.get(extension, "text/html")

    @staticmethod
    def get_static(static_dir, file_path):
        path_to_file = path.join(static_dir, file_path)
        with open(path_to_file, 'rb') as f:
            file_content = f.read()
        status_code = '200 OK'
        return status_code, file_content

    @staticmethod
    def decode_value(data):
        new_data = {}
        for k, v in data.items():
            val = bytes(v.replace('%', '=').replace("+", " "), 'UTF-8')
            val_decode_str = quopri.decodestring(val).decode('UTF-8')
            new_data[k] = val_decode_str
        return new_data