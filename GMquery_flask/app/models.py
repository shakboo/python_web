#!/usr/bin/env python
#coding=utf-8
from werkzeug.security import generate_password_hash, check_password_hash
from flask.ext.login import UserMixin
from . import login_manager,db
from datetime import datetime

#加载用户的回调函数
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    posts = db.relationship('Post', backref = 'author', lazy = 'dynamic')

    def __repr__(self):
        return '<User %r>' % self.username

    #支持密码散列
    @property
    def password(self):
        raise AttributeError('password is not readable attribute')

    @password.setter
    def password(self,password):
        self.password_hash = generate_password_hash(password)
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    #简单设置管理员
    def is_shakboo(self):
        if self.username == "shakboo":
            return True
        return False

    def is_login(self):
        return True

#提交模型
class Post(db.Model):
    __tablename__ = 'posts'
    gm = db.Column(db.String(128), primary_key = True)
    info = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default = datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))

class Post_filter(db.Model):
    __tablename__ = 'posts_filter'
    gm_filter = db.Column(db.String(128), primary_key = True)
    info_filter = db.Column(db.Text)
    #author_id = db.Column(db.Integer, db.ForeignKey('users.id'))