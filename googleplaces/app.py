# coding=utf-8

from tornado.web import (
    access_log, Application, StaticFileHandler, URLSpec)
from tornado.httputil import responses
from googleplaces.views import PlacesView

HTTP_LOG = '{method} {uri} {version} {status} {status_phrase} - {time:.2f} ms'


class Api(Application):

    def log_request(self, handler):
        status = handler.get_status()

        if status == 304 or (
            (status < 300 and isinstance(handler, StaticFileHandler)) or
            (status < 300 and handler.request.uri == '/')
        ):
            # static-file successes or any 304 FOUND are debug-level
            log_method = access_log.debug

        elif status < 400:
            log_method = access_log.info
        elif status < 500:
            log_method = access_log.warning
        else:
            log_method = access_log.error

        log_method(HTTP_LOG.format(
            method=handler.request.method.upper(),
            status=status,
            status_phrase=responses.get(int(status)),
            time=handler.request.request_time() * 1e3,
            uri=handler.request.uri,
            version=handler.request.version
        ))

app = Api([
    URLSpec(handler=PlacesView, pattern=r'^/places/?$'),
    URLSpec(handler=PlacesView, pattern=r'^/places/(?P<pk>[^/]+)/?$')
], debug=True)

