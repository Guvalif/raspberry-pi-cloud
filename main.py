# -*- coding: utf-8 -*-

__author__    = 'Kazuyuki TAKASE'
__copyright__ = 'PLEN Project Company Inc, and all authors.'
__license__   = 'The MIT License (http://opensource.org/licenses/mit-license.php)'


import os

from bottle import Bottle, request
from gevent.pywsgi import WSGIServer
from geventwebsocket import WebSocketError
from geventwebsocket.handler import WebSocketHandler


router = Bottle()
server = WSGIServer(('0.0.0.0', int(os.environ.get('PORT', 5000))), router, handler_class=WebSocketHandler)


@router.route('/msg-bridge')
def handle_websocket():
    websocket = request.environ.get('wsgi.websocket')

    while True:
        try:
            handler = websocket.handler
            message = websocket.receive()

            for client in handler.server.clients.values():
                if client.ws.environ:
                    print(client.ws.environ.get('HTTP_SEC_WEBSOCKET_KEY', ''))

                else:
                    print('void')

                client.ws.send(message)

        except WebSocketError:
            break


@router.route('/')
def handle_index():
    return 'HTTP request is not supported on this server.'


server.serve_forever()
