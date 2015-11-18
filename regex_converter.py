from werkzeug.routing import BaseConverter

class RegexConverter(BaseConverter):
    """
    Need this for flask to parse regex.
    """
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]
