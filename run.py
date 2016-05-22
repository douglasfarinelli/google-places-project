# coding=utf-8

from tornado.ioloop import IOLoop
from tornado.options import options
from tornado.httpserver import HTTPServer
from googleplaces.app import app

options.define(
    'port', help='Ex.: 8000', type=int, default=8000)

options.define(
    'host', help='Ex.: 127.0.0.1', default='localhost')


def main():
    options.parse_command_line()
    server = HTTPServer(app)
    io_loop = IOLoop.instance()
    server.listen(
        address=options.host, port=int(options.port or 8000))
    print('Webservice started in http://{0.host}:{0.port}.'.format(options))
    try:
        io_loop.start()
    except KeyboardInterrupt:
        server.stop()
        io_loop.stop()
    print('Webservice stopped.')


if __name__ == '__main__':
    main()
