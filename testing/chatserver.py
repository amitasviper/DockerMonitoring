from flask import Flask, render_template
import json
from flask_socketio import SocketIO, send, emit

app = Flask(__name__)
socketio = SocketIO(app)

@socketio.on('message')
def handle_message(message):
	print "Received : ", message

@socketio.on('custom event')
def handle_send(message):
	data = json.dumps(message)
	message = json.loads(data)
	message['message'] = "Modified message : " + message['message']
	print "message is ",message
	emit('message', message, broadcast=True)

@socketio.on('json')
def handle_json(json):
	print "Received json : ", str(json)

if __name__ == "__main__":
	socketio.run(app)