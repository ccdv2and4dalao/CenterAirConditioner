from abc import abstractmethod


class WebsocketConn(object):

    @abstractmethod
    def put_event(self, room_id, event_name, data):
        pass
