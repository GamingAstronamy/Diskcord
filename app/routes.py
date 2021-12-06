from flask import render_template, flash, redirect, url_for, request
from app import app, db, socketio, send
from app.form import LoginForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Message, Room
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

    return render_template('login.html', title='Sign In', form=form, current_user = current_user)

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/room/<room_id>')
def room(room_id):
    if current_user in Room.query.get(room_id).users:
        return render_template('room.html', room_id=room_id)

    return redirect(url_for('index'))

@socketio.on('connect')
def connection():
    update_messages()

@socketio.on('new_message')
def new_message(message):
    newMessage = Message(content=message,author=current_user)

    db.session.add(newMessage)
    db.session.commit()

    update_messages()
   

@socketio.on('userdata_request')
def userdata_request():
    userdata = current_user.toDict()
    socketio.emit('userdata', userdata)

@socketio.on('userdata_change')
def userdata_change(userdata):
    current_user.nickname = userdata['nickname']
    current_user.color = userdata['color']
    db.session.commit()

    update_messages()

def update_messages():
    messages = [message.toDict() for message in reversed(Message.query.order_by(Message.id.desc()).all())]
    socketio.emit('message_database_change', messages, broadcast=True)