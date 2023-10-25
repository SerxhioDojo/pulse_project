from flask_app import app
from flask_app import socketio

from flask_app.controllers import users, posts

if __name__ == '__main__':
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True)
    app.run(debug=True)
