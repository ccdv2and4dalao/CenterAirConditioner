import json
import os
import re
import subprocess
from collections import namedtuple

import fire


def to_camel_case(snake_str):
    components = snake_str.split('_')
    return components[0] + ''.join(x.title() for x in components[1:])

def cmd(cmd_str, cwd=None):
    return subprocess.Popen(cmd_str, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                            cwd=cwd).stdout.read()

def cmds(cmd_str, cwd=None):
    print(cmd_str)
    return cmd(cmd_str, cwd)


def pcmds(cmd_str, cwd=None, encoding='utf-8'):
    print(cmds(cmd_str, cwd).decode(encoding))


dependencies = namedtuple('Dependencies',[])(*[])


class MinimumCli:
    python_interpreter = 'python3'
    current_path = os.path.dirname(os.path.realpath(__file__))

    def __init__(self):
        self.qut_object_name = None
        self.object_name = None
        self.m_snake_name = None
        self.camel = None
        self.up_camel = None
        self.placeholder = None

    def apply_context(self, *key_values, f=None, c=False):
        key_values = map(lambda x: x if x[1] else x, map(lambda x: x.split('=', 2), key_values))
        with open('.minimum-lib-env.json', 'r+') as f1:
            content = f1.read()
            context = json.loads('{}' if len(content) == 0 or c else content)
            if f is not None:
                with open(f, 'r+') as f2:
                    content = f2.read()
                    context.update(json.loads('{}' if len(content) == 0 else content))
            for key_value in key_values: context[key_value[0]] = key_value[1]
            f1.seek(0)
            f1.truncate()
            json.dump(context, f1, indent=4)

    def hello(self):
        print('minimum-cli v0.4')

    def help(self):
        """show help for xminimum"""

        print("""minimum-cli v0.4
xminimum == bin/cli.py

xmake == bin/makefile.py
use command xmake --help to learn more

""")

    def redeploy(self):
        pcmds("git pull")
        pcmds(f'{MinimumCli.python_interpreter} {MinimumCli.current_path}/cli.py make image')
        pcmds(f'{MinimumCli.python_interpreter} {MinimumCli.current_path}/cli.py make down')
        pcmds(f'{MinimumCli.python_interpreter} {MinimumCli.current_path}/cli.py make up')

    def install(self):
        pass

    def make(self, target):
        pcmds(f'{MinimumCli.python_interpreter} {MinimumCli.current_path}/makefile.py {target}')

    def fmt(self):
        pass

    def test(self):
        pass

    def replace(self, file_name, old_str, new_str):
        with open(file_name, 'r+') as f:
            source = f.read()
            f.seek(0)
            f.truncate()
            f.write(source.replace(old_str, new_str))

minimum = MinimumCli()

if __name__ == '__main__':
    fire.Fire(MinimumCli)
