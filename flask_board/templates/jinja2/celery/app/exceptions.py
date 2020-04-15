class APIException(Exception):
    status_code = 400
    default_message = ''

    def __init__(self, message=None, status_code=None, payload=None):
        self.message = message or self.default_message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        rv['code'] = self.status_code
        return rv
