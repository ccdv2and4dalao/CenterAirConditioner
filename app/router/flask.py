from abc import abstractmethod

from abstract.controller import PingController

from flask import Flask, make_response
from collections import namedtuple

from abstract.controller.connect import ConnectController
from abstract.singleton import option_context, OptionArgument
from lib import Serializer
from lib.injector import Injector
from flask import request

HTTPSpecItem = namedtuple('HTTPSpecItem', ['ctl_prop', 'path', 'methods'])
http_spec = namedtuple('HTTPSpec', ['ping', 'connect'])(
    [
        HTTPSpecItem('ping', '/ping', ['GET'])
    ],
    [
        HTTPSpecItem('connect', '/connect', ['POST'])
    ]
)


class RouteController(object):
    @abstractmethod
    def ok(self, data: object):
        pass

    @abstractmethod
    def err(self, data: object):
        pass

    @abstractmethod
    def reject_no_auth(self):
        pass

    @abstractmethod
    def reject_not_found(self):
        pass

    @abstractmethod
    def serve_file(self, path):
        pass

    @abstractmethod
    def bind_json(self, req_type):
        pass


option_context.arguments.append(OptionArgument(
    long_opt='host', help_msg='host_name', default_value='127.0.0.1'))


class FlaskRouteController(RouteController):
    def __init__(self, inj: Injector):
        self.s = inj.require(Serializer)  # type: Serializer

    def ok(self, data: object):
        return make_response(self.s.serialize(data), 200)

    def err(self, data: object):
        return make_response(self.s.serialize(data), 200)

    def reject_no_auth(self):
        return make_response('', 403)

    def reject_not_found(self):
        return make_response('', 404)

    def serve_file(self, path):
        pass

    def bind_json(self, req_type):
        req = req_type()
        req.bind_dict(request.get_json())
        return req


class FlaskRouter(object):
    def __init__(self, injector: Injector):
        self.app = Flask('center-air-conditioner')
        self.apply_ctl(injector.require(PingController), http_spec.ping)
        self.apply_ctl(injector.require(ConnectController), http_spec.connect)

    def run(self, host: str, port: str, debug: bool = True):
        self.app.run(host, port, debug=debug)

    def apply_ctl(self, ctl, specs):

        for spec in specs:
            self.app.add_url_rule(spec.path, None,
                                  getattr(ctl, spec.ctl_prop),
                                  methods=spec.methods)

