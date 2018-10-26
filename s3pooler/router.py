from functools import reduce

class Router():
    
    routes = {}

    def register(self, url, callback=None, event=None):
        path_dict = {}
        fields = [field for field in url.split('/') if field]
        path_dict['callback'] = callback
        path_dict['event'] = event
        path_dict['params'] = [field[1:-1] for field in fields if self.__isparam(field)]
        path_dict['not_params'] = [field for field in fields if not self.__isparam(field)]
        path_dict['pure_path'] = reduce((lambda x, y: x + '/' + y), path_dict['not_params'], '')
        Router.routes[url] = path_dict

    def get(self, url):
        return self.__add_params_dict(self.__find_first_match(url), url)

    def has(self, url):
        return True if self.__find_first_match(url) != {} else False

    def __isparam(self, field):
        return True if (field[0] == '{' and field[-1] == '}') \
            else False

    def __find_first_match(self, url):
        fields = [field for field in url.split('/') if field]
        for url_dict in Router.routes.values():
            if set(url_dict['not_params']).difference(set(fields)) == set():
                return url_dict
        return {}

    def __add_params_dict(self, url_dict, url):
        if url_dict == {}:
             return {}
        fields = [field for field in url.split('/') if field]
        params = [field for field in fields \
            if field not in url_dict['not_params']]
        url_dict['params_dict'] = {
                param:value for param, value \
                in zip(url_dict['params'],params)}
        return url_dict
