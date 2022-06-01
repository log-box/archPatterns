from wsgiref.simple_server import make_server

from logbox_framework.main import Framework
from views import routes

SERVER_PORT = 8080

application = Framework(routes)


with make_server('', SERVER_PORT, application) as httpd:
    print(f'Server started on {SERVER_PORT}')
    httpd.serve_forever()