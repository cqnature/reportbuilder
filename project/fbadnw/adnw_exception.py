class ValidationError(Exception):
    def __init__(self, message, errors=None):
        super(ValidationError, self).__init__(message)
        self.errors = errors
        self.message = message


class HttpResponseError(Exception):
    def __init__(self, message, errors=None):
        super(HttpResponseError, self).__init__(message)
        self.errors = errors
        self.message = message


class InvalidQueryIdError(Exception):
    def __init__(self, message, errors=None):
        super(InvalidQueryIdError, self).__init__(message)
        self.errors = errors
        self.message = message
