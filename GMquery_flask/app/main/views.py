#!/usr/bin/env python
#coding=utf-8

from flask import url_for, redirect, render_template, request,flash
from . import main
from .forms import PostForm
from ..models import Post
from .. import db
from flask.ext.login import current_user

@main.route('/', methods = ['GET','POST'])
def index():
    try:
        if current_user.is_login():
            pass
    except:
            return redirect(url_for('auth.login'))
    form1 = PostForm()
    if form1.validate_on_submit():

        post = Post(gm=form1.gm.data, info=form1.info.data)
        db.session.add(post)

        return redirect(url_for('.index'))


    if request.method == 'POST':
        delete_gm = request.form['for_query']
        delete_gm_find = Post.query.filter_by(gm=delete_gm).first()
        db.session.delete(delete_gm_find)
        return redirect(url_for('.index'))

    posts = Post.query.order_by('gm').all()
    return render_template('index.html', form=form1,posts = posts)







