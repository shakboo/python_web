#!/usr/bin/env python
#coding=utf-8
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField,TextAreaField
from wtforms.validators import Required, Length

class PostForm(Form):
    gm = StringField('GM指令', validators=[Required(),Length(1,64)])
    info = TextAreaField('描述',validators = [Required()])
    submit1 = SubmitField('确认')
