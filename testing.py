from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)

#Renders the home page of the application server.
@app.route('/')
@app.route('/home')
def home():
	return render_template('testing.html', title="Home")

@socketio.on('message')
def handle_message(message):
	print "Received message : ", message

@socketio.on('json')
def handle_json(json):
	print "Received json : ", str(json)

if __name__ == "__main__":
	socketio.run(app)