#!/usr/bin/env python
#coding=utf-8

from flask import url_for, redirect, render_template, request,flash
from . import main
from .forms import PostForm
from ..models import Post
from .. import db
from flask.ext.login import current_user

POSTS_PER_PAGE = 10

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

        #如果指令已存在就回滚操作，不然会报错
        try:
            db.session.commit()
        except:
            db.session.rollback()
            flash("该指令已存在！")

        return redirect(url_for('.index'))


    if request.method == 'POST':
        delete_gm = request.form['for_query']
        delete_gm_find = Post.query.filter_by(gm=delete_gm).first()
        db.session.delete(delete_gm_find)
        return redirect(url_for('.index'))

    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by('gm').paginate(page,POSTS_PER_PAGE,False)
    posts = pagination.items

    return render_template('index.html', form=form1,posts = posts,pagination=pagination)







