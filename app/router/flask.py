from abc import abstractmethod
from collections import namedtuple

from flask import Flask, make_response
from flask import request

from abstract.consensus import FlowLabel
from abstract.controller import PingController
from abstract.controller.connect import ConnectController
from abstract.singleton import option_context, OptionArgument
from lib import Serializer
from lib.injector import Injector

HTTPSpecItem = namedtuple('HTTPSpecItem', ['ctl_prop', 'path', 'methods', 'label'])
http_spec = namedtuple('HTTPSpec', ['ping', 'connect'])(
    [
        HTTPSpecItem('ping', '/ping', ['GET'], FlowLabel.Ping)
    ],
    [
        HTTPSpecItem('connect', '/connect', ['POST'], FlowLabel.Connect)
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


option_context.arguments.append(OptionArgument(
    long_opt='host', help_msg='host_name', default_value='127.0.0.1'))
option_context.arguments.append(OptionArgument(
    long_opt='port', help_msg='the port run on', default_value='8080'))


class FlaskRouter(object):
    def __init__(self, injector: Injector):
        self.app = Flask('center-air-conditioner')
        self.apply_ctl(injector.require(PingController), http_spec.ping)
        self.apply_ctl(injector.require(ConnectController), http_spec.connect)

    def run(self, host: str, port: str, debug: bool = True):
        self.app.run(host, port, debug=debug)

    def apply_ctl(self, ctl, specs):
        for spec in specs:
            serve_func = getattr(ctl, spec.ctl_prop)
            flow_label = spec.label

            def label_middleware(*args, **kwargs):
                request.environ['_m_lbl'] = flow_label
                serve_func(*args, **kwargs)

            label_middleware.__name__ = type(ctl).__name__ + '.' + spec.ctl_prop

            self.app.add_url_rule(spec.path, None,
                                  label_middleware,
                                  methods=spec.methods)
