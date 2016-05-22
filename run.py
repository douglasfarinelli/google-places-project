# coding=utf-8

from tornado.ioloop import IOLoop
from tornado.options import options
from tornado.httpserver import HTTPServer
from googleplaces.log import configure_loggers

options.define(
    'port', help='Ex.: 8000', type=int, default=8000)

options.define(
    'host', help='Ex.: 127.0.0.1', default='localhost')


def main():
    options.parse_command_line()
    configure_loggers()
    from googleplaces.app import app
    server = HTTPServer(app)
    io_loop = IOLoop.instance()
    server.listen(
        address=options.host, port=int(options.port or 8000))
    print('Starting server at http://{0.host}:{0.port}.'.format(options))
    try:
        io_loop.start()
    except KeyboardInterrupt:
        server.stop()
        io_loop.stop()
    print('Server stopped.')


if __name__ == '__main__':
    main()
