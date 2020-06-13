from socket import SocketIO

from flask import Flask, request

from abstract.component import ConnectionPool
from abstract.component.websocket_conn import WebsocketConn


def functional_flask_socket_io_connection_impl(inj):
    app = inj.Require(Flask)  # type: Flask
    sio = SocketIO(app, cors_allowed_origins='*')

    class FunctionalSocketIOConnectionImpl(WebsocketConn):
        def __init__(self):
            self.connection_pool = inj.require(ConnectionPool)  # type: ConnectionPool
            self.sio = sio
            self.session_id_rev_mapping = dict()

            @sio.on('connect')
            def connect():
                room_id = int(request.args['room_id'])
                self.connection_pool.put_session_id(room_id, request.sid)
                self.session_id_rev_mapping[request.sid] = room_id

            @sio.on('disconnect')
            def disconnect():
                self.connection_pool.close_session_connection(self.session_id_rev_mapping[request.sid])

        def put_event(self, room_id, event_name, data):
            room_info = self.connection_pool.get(room_id)
            if room_info is None:
                return None

            sio.emit(event_name, data, room=room_info.session_id)

    return FunctionalSocketIOConnectionImpl()
