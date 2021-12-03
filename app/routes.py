from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.form import LoginForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Message
from werkzeug.urls import url_parse

@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    return render_template('index.html', title = 'Home')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)

    return render_template('login.html', title='Sign In', form=form)

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/messages')
@login_required
def messages():
    messages = Message.query.order_by(Message.id.desc()).all()
    
    return render_template('messages.html', messages=messages)

@app.route('/sendMessage')
@login_required
def sendMessage():
    content = request.args.get('message_content')
    newMessage = Message(content=content,author=current_user)

    db.session.add(newMessage)
    db.session.commit()

    return {'response' : 'success'}

@app.route('/userdata')
@login_required
def userdata():
    return {'username' : current_user.username, 'nickname' : current_user.nickname, 'color' : current_user.color}

@app.route('/setuserdata')
@login_required
def setuserdata():
    nickname = request.args.get('nickname')
    color = request.args.get('color')

    current_user.nickname = nickname
    current_user.color = color
    db.session.commit()

    return {'response' : 'success'}

