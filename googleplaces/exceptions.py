# coding=utf=8

"""Arquivo que contém todas as exceptions personalizadas."""

from tornado.web import HTTPError


class ApiError(HTTPError):
    """Exception base para Api."""


class PlaceDoesNotExistError(ApiError):

    def __init__(self):
        super(PlaceDoesNotExistError, self).__init__(status_code=404)


class OverQueryLimitError(ApiError):
    def __init__(self):
        super(OverQueryLimitError, self).__init__(
            status_code=403,
            log_message='Indica que a cota de solicitações a Google Api foi ultrapassada.'
        )


class RequestDeniedError(ApiError):
    def __init__(self):
        super(RequestDeniedError, self).__init__(
            status_code=403,
            log_message='Indica que a solicitação a Google Api foi negada, devido a key '
                        'inválida.'
        )


class InvalidRequestError(ApiError):
    def __init__(self):
        super(InvalidRequestError, self).__init__(
            status_code=400,
            log_message='Indica que faltou o parâmetro name na query string.'
        )


class InvalidJSONError(ApiError):
    def __init__(self):
        super(ApiError, self).__init__(
            status_code=400,
            log_message='Indica que o corpo do request contém um JSON inválido.'
        )

