#!/usr/bin/env python3
import os
import re
import subprocess
import sys
import shutil
import json

made = set()


def consume_makefile(method, *arg, **kwarg):
    if callable(method):
        i = str(method)
        if i not in made:
            made.add(i)
            method(*arg, **kwarg)


# return function in object scope
def sq(obj, attr):
    # raise if not exists
    def __get_object_attr(*_): return getattr(obj, attr)

    return __get_object_attr


# object requirements
def sqs(obj, *attrs): return map(lambda attr: sqs(obj, attr), attrs)


# return function in object scope
def oq(attr):
    # raise if not exists
    def __get_object_attr(obj, *_): return getattr(obj, attr)

    return __get_object_attr


# object requirements
def oqs(*attrs): return map(oq, attrs)


def require(*targets):
    def c(f):
        def wrapper(*args, **kwargs):
            for target in targets:
                target = (getattr(target, '__name__', None) == '__get_object_attr' and target(*args,
                                                                                              **kwargs)) or target
                consume_makefile(target, *args, **kwargs)
            return f(*args, **kwargs)

        return wrapper

    return c


def require_cls(*target): return require(*oqs(*target))


def pipe(cmd, cwd=None):
    p, line, line2 = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                      cwd=cwd), ' ', ' '
    while len(line) != 0 or len(line2) != 0:
        line = p.stdout.readline()
        line2 = p.stderr.readline()
        if len(line) != 0:
            print(line.decode('utf-8').strip())
        if len(line2) != 0:
            print(line2.decode('utf-8').strip())
    code = p.wait()
    if code != 0:
        print('exit with %d' % code)


def entry(self, args):
    getattr(self, args[0])(*args[1:]) if len(args) > 0 else self.all()


class Makefile:
    config_file = None
    config_file_target = None
    crt_file = None
    crt_file_target = None
    key_file = None
    key_file_target = None
    current_path = os.path.dirname(os.path.realpath(__file__))
    base_path = os.path.dirname(current_path)
    config_file_name = 'config.yaml'
    context = dict()

    compose_template_file = 'docker-compose.template.yml'
    compose_file = 'docker-compose.yml'
    silent = False

    @classmethod
    def hello(cls, *_):
        print('minimum builder')

    @classmethod
    def pipe(cls, cmd, *_):
        if not cls.silent: print(cmd)
        pipe(cmd)

    @classmethod
    def generate(cls, path='./', match=None, *_):
        match = cls._gen_match(match)
        for file in os.listdir(path):
            file = os.path.join(path, file)
            if os.path.isdir(file):
                cls.generate(file, match)
            if os.path.isfile(file) and match.match(file):
                cls.pipe('go generate %s' % file)


    @classmethod
    @require_cls('read_context')
    def image(cls, *_):
        cls.pipe('docker build --tag %s .' % cls.context['node-name'])


    @staticmethod
    def _gen_match(match):
        if match is None:
            match = re.compile(r'^.*\.go$')
        if isinstance(match, str):
            match = re.compile(match)
        return match

    @classmethod
    @require_cls('template')
    def up(cls, *_):
        pipe('docker-compose -f %s up' % (cls.compose_file))

    @classmethod
    @require_cls('template')
    def down(cls, *_):
        pipe('docker-compose -f %s down' % (cls.compose_file))

    @classmethod
    @require_cls('template')
    def start(cls, *_):
        pipe('docker-compose -f %s start' % (cls.compose_file))

    @classmethod
    @require_cls('template')
    def stop(cls, *_):
        pipe('docker-compose -f %s stop' % (cls.compose_file))

    @classmethod
    @require_cls('read_context')
    def ping(cls, *_):
        pipe('curl localhost:%s/ping' % (str(cls.context['target-port'])))


    @classmethod
    @require_cls('read_context')
    def template(cls, *_):
        with open(cls.compose_template_file) as f:
            s = f.read().replace('{{redis-root-password}}', cls.context['redis-root-password'])
            s = s.replace('{{mysql-root-password}}', cls.context['mysql-root-password'])
            s = s.replace('{{conf-path}}', cls.context['conf-path'])
            s = s.replace('{{logs-path}}', cls.context['logs-path'])
            s = s.replace('{{data-path}}', cls.context['data-path'])
            s = s.replace('{{node-name}}', cls.context['node-name'])
            s = s.replace('{{instance-name}}', cls.context['instance-name'])
            s = s.replace('{{target-port}}', str(cls.context['target-port']))
            s = s.replace('{{enable-https}}', str(cls.context['enable-https']))

            s = s.replace('{{config-file}}', cls.config_file)
            s = s.replace('{{config-file-target}}', cls.config_file_target)
            s = s.replace('{{crt-file}}', cls.crt_file)
            s = s.replace('{{crt-file-target}}', cls.crt_file_target)
            s = s.replace('{{key-file}}', cls.key_file)
            s = s.replace('{{key-file-target}}', cls.key_file_target)

            s = s.replace('{{mysql-norm-password}}', cls.context['mysql-norm-password'])
            with open(cls.compose_file, 'w') as o:
                o.write(s)

    @classmethod
    def read_context(cls, *_):
        with open(os.path.abspath('.minimum-lib-env.json'), 'r', encoding='utf-8') as f:
            c = f.read().encode('utf-8')
            cls.context = json.loads('{}' if len(c) == 0 else c)
            cls.context['node-name'] = cls.context.get('node-name', 'myriaddreamin/air-backend:alpine')
            cls.context['instance-name'] = cls.context.get('instance-name', 'backend')

            cls.context['redis-root-password'] = cls.context.get('redis-root-password', '12345678')
            cls.context['mysql-root-password'] = cls.context.get('mysql-root-password', '12345678')
            cls.context['mysql-norm-password'] = cls.context.get('mysql-norm-password', '12345678')

            cls.context['conf-path'] = os.path.join(cls.current_path, cls.context.get('conf-path', f'{Makefile.base_path}/data/testdb/conf'))
            cls.context['logs-path'] = os.path.join(cls.current_path, cls.context.get('logs-path', f'{Makefile.base_path}/data/testdb/logs'))
            cls.context['data-path'] = os.path.join(cls.current_path, cls.context.get('data-path', f'{Makefile.base_path}/data/testdb/data'))

            cls.context['target-port'] = cls.context.get('target-port', 2022)
            cls.context['enable-https'] = cls.context.get('enable-https', False)

            cls.context['config-file-name'] = cls.context.get('config-file-name', 'config.yaml')
            cls.config_file = os.path.abspath(cls.context['config-file-name'])
            cls.config_file_target = os.path.join('/', cls.context['config-file-name'])

            cls.context['crt-file-name'] = cls.context.get('crt-file-name', 'air.crt')
            cls.crt_file = os.path.abspath(cls.context['crt-file-name'])
            cls.crt_file_target = os.path.join('/', cls.context['crt-file-name'])

            cls.context['key-file-name'] = cls.context.get('key-file-name', 'air.pri')
            cls.key_file = os.path.abspath(cls.context['key-file-name'])
            cls.key_file_target = os.path.join('/', cls.context['key-file-name'])

    @classmethod
    @require_cls('read_context')
    def context(cls, *_):
        print('key            ', 'value')
        print('conf-path      ', cls.context['conf-path'])
        print('logs-path      ', cls.context['logs-path'])
        print('data-path      ', cls.context['data-path'])
        print('config         ', cls.context['config-file-name'])
        print('               ', '%s => %s' % (cls.config_file, cls.config_file_target))
        print('crt            ', cls.context['crt-file-name'])
        print('               ', '%s => %s' % (cls.crt_file, cls.crt_file_target))
        print('key            ', cls.context['key-file-name'])
        print('               ', '%s => %s' % (cls.key_file, cls.key_file_target))
        print('node-name      ', cls.context['node-name'])
        print('instance-name  ', cls.context['instance-name'])
        print('target-port    ', cls.context['target-port'])
        print('enable-https   ', cls.context['enable-https'])

    @classmethod
    @require_cls('read_context')
    def clean(cls, *_):
        shutil.rmtree('testdb')

    @classmethod
    @require_cls('up')
    def all(cls, *_):
        pass



if __name__ == '__main__':
    entry(Makefile, sys.argv[1:])
