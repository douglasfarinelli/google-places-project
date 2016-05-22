# coding=utf-8

from logging.config import dictConfig

CONSOLE_HANDLER = dict(handlers=['console'], propagate=True)
CONSOLE_HANDLER_N_PROPAGATE = dict(handlers=['console'], propagate=False)


def configure_loggers():
    dictConfig({
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'default': {
                'format': '[%(levelname)s %(asctime)s] %(message)s'
            },
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'level': 'DEBUG',
                'formatter': 'default',
            },
        },
        'loggers': {
            'root': CONSOLE_HANDLER,
            'tornado.access': CONSOLE_HANDLER_N_PROPAGATE,
            'tornado.application': CONSOLE_HANDLER_N_PROPAGATE,
            'tornado.general': CONSOLE_HANDLER_N_PROPAGATE,
            'googleplaces.ops': CONSOLE_HANDLER_N_PROPAGATE,
        }
    })
