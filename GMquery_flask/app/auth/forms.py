#!/usr/bin/env python
#coding=utf-8
from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Length,Regexp,EqualTo
from wtforms import ValidationError
from ..models import User

class LoginForm(Form):
    username = StringField('账号', validators=[Required(),Length(1,64)])
    password = PasswordField('密码',validators=[Required()])
    remember_me = BooleanField('记住我')
    submit = SubmitField('登陆')

class RegistrationForm(Form):
    username = StringField('账号',validators=[Required(),Length(1,64),Regexp('^[A-Za-z][A-Za-z0-9]*$',0,'账户名只能是字母和数字')])
    password = PasswordField('密码',validators=[Required(),EqualTo('password2',message='再次输入密码')])
    password2 = PasswordField('确认密码',validators=[Required()])
    submit = SubmitField('提交')

    def validate_username(self,field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('账户名重复')


