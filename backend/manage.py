# -*- coding: utf-8 -*-
from flask_script import Manager, Server
from girls.core.main import app_factory

manager = Manager(app_factory)

if __name__ == '__main__':
    server = Server(host="0.0.0.0", port=8888)
    manager.add_option('-c', '--config', dest='config', required=False, default='dev',
                       choices=('dev', 'prod', 'test'))
    manager.add_command("runserver", server)
    manager.run()
