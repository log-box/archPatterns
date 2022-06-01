import datetime


def debug(func):
    def wrapper(*args, **kwargs):
        name = func.__name__
        time_start = datetime.datetime.now()
        res = func(*args, **kwargs)
        time_end = datetime.datetime.now()
        print(f'Function "{name}" has worked {time_end - time_start} sec')
        return res

    return wrapper


def logging(func):
    def wrapper(*args, **kwargs):
        res = func(*args, **kwargs)
        print(func.__name__, args, kwargs)
        return res

    return wrapper


class AppRoute:
    def __init__(self, routes, url):
        self.routes = routes
        self.url = url

    def __call__(self, cls):
        self.routes[self.url] = cls()
