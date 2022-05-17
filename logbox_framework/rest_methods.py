class GetRequests:

    @staticmethod
    def parse_data(data):
        result = {}
        if data:
            split_string = data.split('&')
            for item in split_string:
                key, value = item.split('=')
                result[key] = value
        return result

    @staticmethod
    def get_request_params(environ):
        query_string = environ['QUERY_STRING']
        request_params = GetRequests.parse_data(query_string)
        return request_params


class PostRequests:

    @staticmethod
    def pars_data(data):
        result = {}
        if data:
            split_string = data.split('&')
            for item in split_string:
                key, value = item.split('=')
                result[key] = value
        return result

    @staticmethod
    def get_wsgi_data(environ):
        content_length = int(environ['CONTENT_LENGTH'])
        if content_length > 0:
            data = environ['wsgi.input'].read(content_length).decode(encoding='utf-8')
            # data = data
            return data
        else:
            return ''

    @staticmethod
    def get_request_data(environ):
        data = PostRequests.get_wsgi_data(environ)
        data = PostRequests.pars_data(data)
        return data

