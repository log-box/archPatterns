from pprint import pprint

from logbox_framework.rest_methods import GetRequests, PostRequests


class PageNotFound404:
    def __call__(self):
        return '404 ', 'PAGE Not Found 404'


class Framework:
    """
    The base class witch need to be use first
    """

    def __init__(self, route_lst):
        self.route_lst = route_lst

    def __call__(self, environ, start_response):
        pprint(environ)

        path = environ['PATH_INFO']
        if not path.endswith('/'):
            path = f'{path}/'

        request = {'method': environ['REQUEST_METHOD']}

        # get request params or/and data
        if request['method'] == 'GET':
            pprint('GET_METHOD')
            request['request_params'] = GetRequests().get_request_params(environ)
        if request['method'] == 'POST':
            pprint('POST_METHOD')
            request['request_params'] = PostRequests.get_request_data(environ)

        # get Controller (function)
        if path in self.route_lst:
            view = self.route_lst[path]
        else:
            view = PageNotFound404()

        # start Controller
        code, body = view()
        start_response(code, [('Content-Type', 'text/html')])
        return [body.encode('utf-8')]

