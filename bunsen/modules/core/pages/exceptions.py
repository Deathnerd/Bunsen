# -*- coding: utf-8 -*-

class BunsenPageBuildError(BaseException):
    def __init__(self, message, errors):
        super(BunsenPageBuildError, self).__init__(message)
        self.errors = errors