import quopri
from pprint import pprint

from components.decorators import logging
from logbox_framework.rest_methods import GetRequests, PostRequests


class PageNotFound404:
    def __call__(self):
        return '404 ', 'PAGE Not Found 404'


class Framework:
    """
    The base class
    """

    def __init__(self, route_lst):
        self.route_lst = route_lst

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

        # get Controller (function)
        if path in self.route_lst:
            view = self.route_lst[path]
        else:
            view = PageNotFound404()

        # start Controller
        code, body = view(request)
        start_response(code, [('Content-Type', 'text/html')])
        pprint(request)
        return [body.encode('utf-8')]

    @staticmethod
    def decode(data):
        decode_data = {}
        for key, value in data.items():
            temp_val = bytes(value.replace('%', '=').replace('+', ''), 'UTF-8')
            decode_value = quopri.decodestring(temp_val).decode('UTF-8')
            decode_data[key] = decode_value
        # print(decode_data)
        return decode_data
