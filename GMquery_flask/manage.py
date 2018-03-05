#!/usr/bin/env python
#coding=utf-8

import os
from app import create_app,db
from app.models import User, Role, Post
from flask.ext.script import Manager, Shell,Server
from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.moment import Moment

#强制指定为utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)
moment = Moment(app)

def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role, Post=Post)
manager.add_command('shell',Shell(make_context=make_shell_context))
manager.add_command('db',MigrateCommand)
manager.add_command('runserver',Server(host='0.0.0.0',port=5000,use_debugger=True,threaded=True))

if __name__ == '__main__':
    manager.run()