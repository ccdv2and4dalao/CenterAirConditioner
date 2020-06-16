
from flask import Flask, request
from flask_socketio import SocketIO

from abstract.component import ConnectionPool, Logger
from abstract.component.websocket_conn import WebsocketConn


def functional_flask_socket_io_connection_impl(inj):
    app = inj.require(Flask)  # type: Flask
    sio = SocketIO(app, async_mode='threading', cors_allowed_origins='*')

    class FunctionalSocketIOConnectionImpl(WebsocketConn):
        def __init__(self):
            self.connection_pool = inj.require(ConnectionPool)  # type: ConnectionPool
            self.sio = sio
            self.app = app
            self.session_id_rev_mapping = dict()
            self.logger = inj.require(Logger)  # type: Logger

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
                self.logger.warn('put_event to a not connected room', args={'room_id': room_id})
                return None
            session_id = room_info.session_id
            if session_id is None:
                self.logger.warn('put_event to a room without socket connected', args={'room_id': room_id})
                return None

            sio.emit(event_name, data, room=room_info.session_id)

    return FunctionalSocketIOConnectionImpl()
