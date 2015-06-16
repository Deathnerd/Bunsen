# -*- coding: utf-8 -*-

class TableGenerationError(BaseException):

    def __init__(self, message, errors):
        super(TableGenerationError, self).__init__(message)
        self.errors = errors

class FormNotFound(BaseException):

    def __init__(self, message, errors):
        super(FormNotFound, self).__init__(message)
        self.errors = errors