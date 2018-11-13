from bottle import Bottle, request
from gevent.pywsgi import WSGIServer
from geventwebsocket import WebSocketError
from geventwebsocket.handler import WebSocketHandler


router = Bottle()
app    = WSGIServer(('0.0.0.0', 80), router, handler_class=WebSocketHandler)


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


app.serve_forever()
