import os

from bottle import Bottle, request
from gevent.pywsgi import WSGIServer
from geventwebsocket import WebSocketError
from geventwebsocket.handler import WebSocketHandler


router = Bottle()
server = WSGIServer(('0.0.0.0', int(os.environ.get('PORT', 5000))), router, handler_class=WebSocketHandler)


@router.route('/')
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


server.serve_forever()
