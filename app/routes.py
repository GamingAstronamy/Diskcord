from flask import render_template, flash, redirect, url_for, request
from app import app, db, socketio
from app.form import LoginForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Message, Room
from werkzeug.urls import url_parse
from flask_socketio import join_room, leave_room

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

    return render_template('login.html', title='Sign In', form=form, current_user=current_user)

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/room')
@login_required
def room():
    if Room.query.get(current_user.current_room) in current_user.rooms:
        return render_template('room.html', title='Room')
    else:
        return redirect(url_for('index'))
    
@socketio.on('connect')
def connection():
    join_room(current_user.current_room)

@socketio.on('disconnect')
def disconnect():
    leave_room(current_user.current_room)

@socketio.on('message_request')
def message_request():
    update_messages(current_user.current_room)

@socketio.on('new_message')
def new_message(message):
    newMessage = Message(content=message,author=current_user,room_id=current_user.current_room)

    db.session.add(newMessage)
    db.session.commit()

    update_messages(current_user.current_room)

@socketio.on('userdata_request')
def userdata_request():
    userdata = current_user.toDict()
    socketio.emit('userdata', userdata)

@socketio.on('userdata_change')
def userdata_change(userdata):
    current_user.nickname = userdata['nickname']
    current_user.color = userdata['color']
    db.session.commit()

    for room in current_user.rooms:
        update_messages(room.id)

@socketio.on('room_request')
def room_request():
    rooms = [room.toDict() for room in current_user.rooms]
    socketio.emit('room_update', rooms)

@socketio.on('room_change_request')
def room_change_request(room_id):
    current_user.current_room = room_id
    db.session.commit()
    

def update_messages(room):
    messages = [message.toDict() for message in Room.query.get(room).messages.all()]
    socketio.emit('message_database_change', messages, room=room)