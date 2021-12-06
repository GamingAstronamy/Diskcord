from app import app, db, socketio
from app.models import User, Message, Room

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Message': Message, 'Room': Room}

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=443)