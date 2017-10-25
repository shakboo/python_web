#!/usr/bin/env python
#coding=utf-8

from flask import render_template, redirect, request, url_for, flash
from flask.ext.login import logout_user, login_required, login_user, current_user
from . import auth
from .. import db
from ..models import User,Post,Post_filter
from .forms import LoginForm,RegistrationForm


@auth.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username = form.username.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('没有权限或密码错误')
    return render_template('auth/login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash("您已退出")
    return redirect(url_for('auth.login'))

@auth.route('/register',methods=['GET','POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, password=form.password.data)
        db.session.add(user)
        flash('您现在可以登录')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html',form=form)

@auth.route('/query', methods=['GET','POST'])
def query():
    try:
        if current_user.is_login():
            pass
    except:
        return redirect(url_for('auth.login'))
    p_f = None
    if request.method == 'POST':
        posts_delete = Post_filter.query.all()
        for post_delete in posts_delete:
            db.session.delete(post_delete)
        userFilter = request.form['userInput']
        posts = Post.query.order_by('gm').all()
        for post in posts:
            if post.gm.find(userFilter) != -1 or post.info.find(userFilter) != -1:
                p_f = Post_filter(gm_filter=post.gm,info_filter=post.info)
                db.session.add(p_f)
    posts_filter = Post_filter.query.order_by('gm_filter')
    if p_f:
        flash("查询成功")
    else:
        flash("未查找到相应数据")
    return render_template('auth/query.html',form=request.form, posts_filter=posts_filter)

