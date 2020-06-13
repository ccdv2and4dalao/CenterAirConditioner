from abc import abstractmethod
from collections import namedtuple

from flask import Flask, make_response
from flask import request

from abstract.consensus import FlowLabel
from abstract.controller import PingController, ConnectController, DaemonAdminController, AdminController, \
    MetricsController, StatisticsController, SlaveStateControlController
from abstract.singleton import option_context, OptionArgument
from lib import Serializer
from lib.injector import Injector

HTTPSpecItem = namedtuple('HTTPSpecItem', ['ctl_prop', 'path', 'methods', 'label'])
MasterServerHTTPSpec = namedtuple(
    'MasterServerHTTPSpec',
    ['ping', 'connect', 'admin', 'metrics', 'slave_state_control', 'statistics'])
DaemonServerHTTPSpec = namedtuple('DaemonServerHTTPSpec', ['ping', 'admin'])
master_http_spec = MasterServerHTTPSpec(
    [
        HTTPSpecItem('ping', '/ping', ['GET'], FlowLabel.Ping),
    ],
    [
        HTTPSpecItem('connect', '/v1/connect', ['POST'], FlowLabel.Connect),
    ],
    [
        HTTPSpecItem('set_mode', '/v1/admin/mode', ['POST'], FlowLabel.AdminSetMode),
        HTTPSpecItem('set_current_temperature', '/v1/admin/current-temp', ['POST'],
                     FlowLabel.AdminSetCurrentTemperature),
        HTTPSpecItem('get_server_status', '/v1/admin/status', ['GET'], FlowLabel.GetServerStatus),
    ],
    [
        HTTPSpecItem('update_metrics', '/v1/metrics', ['POST'], FlowLabel.UpdateMetrics),
    ],
    [
        HTTPSpecItem('start_state_control', '/v1/state_control/start', ['POST'], FlowLabel.StartStateControl),
        HTTPSpecItem('stop_state_control', '/v1/state_control/stop', ['POST'], FlowLabel.StopStateControl),
    ],
    [
        HTTPSpecItem('generate_statistics', '/v1/statistics', ['GET'], FlowLabel.GenerateStatistics),
    ],
)
daemon_http_spec = DaemonServerHTTPSpec(
    [
        HTTPSpecItem('ping', '/ping', ['GET'], FlowLabel.Ping)
    ],
    [
        HTTPSpecItem('login', '/v1/admin/login', ['POST'], FlowLabel.AdminLogin),
        HTTPSpecItem('boot', '/v1/admin/boot', ['POST'], FlowLabel.AdminBoot),
        HTTPSpecItem('shutdown', '/v1/admin/shutdown', ['POST'], FlowLabel.AdminShutdown),
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

    @abstractmethod
    def bind(self, req_type):
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

    def bind(self, req_type):
        req = req_type()
        req.bind_dict(request.get_json())
        req.bind_header(request.headers)
        return req


option_context.arguments.append(OptionArgument(
    long_opt='host', help_msg='host_name', default_value='127.0.0.1'))
option_context.arguments.append(OptionArgument(
    long_opt='port', help_msg='the port run on', default_value='8080'))


class FlaskRouter(object):
    def __init__(self, name):
        self.app = Flask(name)

    def run(self, host: str, port: str, debug: bool = True):
        self.app.run(host, port, debug=debug)

    def apply_ctl(self, ctl, specs):
        for spec in specs:
            def label_middleware(*args, capture_serve_func=getattr(ctl, spec.ctl_prop), flow_label=spec.label,
                                 **kwargs):
                request.environ['_m_lbl'] = flow_label
                return capture_serve_func(*args, **kwargs)

            label_middleware.__name__ = type(ctl).__name__ + '.' + spec.ctl_prop

            self.app.add_url_rule(spec.path, None,
                                  label_middleware,
                                  methods=spec.methods)


class MasterFlaskRouter(FlaskRouter):
    def __init__(self, injector: Injector):
        super().__init__('center-air-conditioner-server')
        self.apply_ctl(injector.require(PingController), master_http_spec.ping)
        self.apply_ctl(injector.require(AdminController), master_http_spec.admin)
        self.apply_ctl(injector.require(ConnectController), master_http_spec.connect)
        self.apply_ctl(injector.require(MetricsController), master_http_spec.metrics)
        self.apply_ctl(injector.require(StatisticsController), master_http_spec.statistics)
        self.apply_ctl(injector.require(SlaveStateControlController), master_http_spec.slave_state_control)


class DaemonFlaskRouter(FlaskRouter):
    def __init__(self, injector: Injector):
        super().__init__('center-air-conditioner-daemon')
        self.apply_ctl(injector.require(PingController), master_http_spec.ping)
        self.apply_ctl(injector.require(DaemonAdminController), daemon_http_spec.admin)
