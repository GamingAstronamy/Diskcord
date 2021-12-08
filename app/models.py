from app import db, login
from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class UserRoom(db.Model):
    __tablename__ = 'userroom'

    id = db.Column(db.Integer, primary_key=True)
    user_ids = db.Column(db.Integer, db.ForeignKey('user.id'))
    room_ids = db.Column(db.Integer, db.ForeignKey('room.id'))
    

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    nickname = db.Column(db.String(64), default=username)
    password_hash = db.Column(db.String(128))
    color = db.Column(db.String(64), default='#ffffff')
    profile_picture = db.Column(db.String(128))

    current_room = db.Column(db.Integer)

    messages = db.relationship('Message', backref='author', lazy='dynamic')
    rooms = db.relationship('Room', secondary='userroom')

    def __repr__(self):
        return f'<User {self.username}>'

    def toDict(self):
        return {'id':self.id,'username':self.username,'nickname':self.nickname,'color':self.color,'current_room':self.current_room} 

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(256))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'))

    def __repr__(self):
        return f'<Message {self.content}>'

    def toDict(self):
        return {'id':self.id, 'content': self.content, 'timestamp':self.timestamp.replace(tzinfo=timezone.utc).astimezone(tz=None).strftime('%A %m/%d/%Y %I:%M %p'), 'author':self.author.toDict()}

class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    users = db.relationship('User', secondary='userroom')
    messages = db.relationship('Message', backref='room', lazy='dynamic')

    def toDict(self):
        return {'id':self.id, 'name':self.name, 'messages':[message.toDict() for message in self.messages], 'users':[user.toDict() for user in self.users]}


@login.user_loader
def load_user(id):
    return User.query.get(int(id))