#!/usr/bin/env python
#coding=utf-8

from flask import Blueprint

main = Blueprint('webs', __name__)

from . import views