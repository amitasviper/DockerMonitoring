from flask import Flask, render_template, url_for, request, jsonify, Response, copy_current_request_context
import random, time, json, urllib2, requests
from threading import Thread

from flask_socketio import SocketIO, send, emit

SERVER_IP = '192.168.144.148'
SERVER_PORT = '4243'
SERVER_ADDRESS = 'http://' + SERVER_IP + ':' + SERVER_PORT

async_mode = None

if async_mode is None:
	try:
		import eventlet
	except ImportError:
		pass

	if async_mode is None:
		try:
			from gevent import monkey
			async_mode = 'gevent'
		except ImportError:
			pass

	if async_mode is None:
		async_mode = 'threading'

	print "async_mode is ", async_mode

if async_mode == 'eventlet':
	import eventlet
	eventlet.monkey_patch()
elif async_mode == 'gevent':
	from gevent import monkey
	monkey.patch_all()



app = Flask(__name__)
thread = None

def background_worker():
	if True:
		print "Running on the worker thread"
		data = requests.get(SERVER_ADDRESS + '/containers/json?all=1')
		data = data.json()
		print "Got response"
		#print data
		emit('channel_container_ids_resp', data)

def background_worker_all_day(rest_resp):
	for line in rest_resp.iter_lines():
		if line:
			data = line.json()
			socketio.emit('channel_container_one', data)

#Renders the home page of the application server.
@app.route('/')
@app.route('/home')
def home():
	#print url_for('static', filename='../js/statistics.js')
	return render_template('home.html', title="Home")


""" Renders an html page which shows the list of containers in the docker swarm,
	and if the user provides a container_id also then the info about that container is displayed.
"""
@app.route('/container/')
@app.route('/container/<container_id>')
def container_info(container_id=None):
	if container_id != None:
		print "Rendering graph template with id : ", container_id
		return render_template('container_info.html', title="Container Info", container_id=container_id)
	else:
		print "Rendering to display all container ids"
		return render_template('container_info.html', title="Container Info")


@app.route('/threshold/')
def threshold():
	return render_template('threshold.html')

@app.route('/error_report/')
def error_report():
	return render_template('error_report.html')


""" THIS NEEDS TO BE REPLACED BY SOCKETIO METHOD"""
""" Rest api that serves the json data for various ajax requests """
@app.route('/jsondata/')
@app.route('/jsondata/<container_id>')
def json_data(continer_id=None):
	if container_id != None:
		data = requests.get(SERVER_ADDRESS + '/containers/' + container_id + '/json')
		data = data.json()
		return Response(json.dumps(data), mimetype='application/json')
	else:
		time.sleep(1)
		data = {'cpu_usage': [random.randrange(0, 100) for x in range(2)], 'memory_usage': random.randrange(0, 100), 'network_usage' : random.randrange(0, 100), 'io':random.randrange(0, 100)}
		print data
		return jsonify(data)

@app.route('/jsondata_containers')
def json_data_containers():
	data = requests.get(SERVER_ADDRESS + '/containers/json?all=1')
	data = data.json()
	data = Response(json.dumps(data),  mimetype='application/json')
	emit('container_ids', data, broadcast=True)
	return data

@app.route('/container_stats_one/<container_id>')
def container_stats_one(container_id=None):
	if container_id != None:
		resp = requests.get(SERVER_ADDRESS + '/containers/' + container_id + '/stats?stream=false')
		data = resp.json()
		return Response(json.dumps(data), mimetype='application/json')
	else:
		return jsonify('{}')

@app.route('/container_stats_stream/<container_id>')
def container_stats_stream(container_id=None):
	if container_id != None:
		resp = requests.get(SERVER_ADDRESS + '/containers/' + container_id + '/stats?stream=true')
		data = resp.json()
		return Response(json.dumps(data), mimetype='application/json')
	else:
		return jsonify('{}')



"""******************************* Using Socket IO from here onwards ***************************"""





"""#Renders the home page of the application server.
@app.route('/test')
def testing():
	#print url_for('static', filename='../js/statistics.js')
	return render_template('testing.html', title="Home")

@socketio.on('message')
def handle_message(message):
	print "Received : ", message

@socketio.on('send')
def handle_send(message):
	data = json.dumps(message)
	message = json.loads(data)
	message['message'] = "Modified message : " + message['message']
	print "message is ",message
	emit('message', message, broadcast=True)

@socketio.on('json')
def handle_json(json):
	print "Received json : ", str(json)"""

socketio = SocketIO(app, async_mode=async_mode)


""" For ploting graph """

@socketio.on('channel_container_one_req')
def collect_container_one(req):
	print "Request received from browser one: ", req
	container_id = req

	@copy_current_request_context
	def background_worker_one():
		if True:
			print "Running on the worker thread onet"
			rest_resp = requests.get(SERVER_ADDRESS + '/containers/' + container_id + '/stats?stream=true', stream=True)
			for line in rest_resp.iter_lines():
				if line:
					data = line
					print data,'\n\n\n\n'
					emit('channel_container_one_resp', data)
	lthread = Thread(target=background_worker_one)
	lthread.daemon = True
	lthread.start()



@socketio.on('channel_container_one_sample_req')
def collect_container_one(req):
	print "Request received from browser one: ", req
	container_id = req

	@copy_current_request_context
	def background_worker_one_sample():
		if True:
			print "Running on the worker thread onet"
			data = requests.get(SERVER_ADDRESS + '/containers/' + container_id + '/stats?stream=false')
			data = data.json()
			emit('channel_container_one_sample_resp', data)
	lthread = Thread(target=background_worker_one_sample)
	lthread.daemon = True
	lthread.start()




""" For listing all the containers"""

@socketio.on('channel_container_ids_req')
def collect_container_ids(req):
	print "Request received from browser: ", req

	@copy_current_request_context
	def background_worker():
		if True:
			print "Running on the worker thread"
			data = requests.get(SERVER_ADDRESS + '/containers/json?all=1')
			data = data.json()
			print "Got response"
			#print data
			emit('channel_container_ids_resp', data)
	lthread = Thread(target=background_worker)
	lthread.daemon = True
	lthread.start()

if __name__ == "__main__":
	socketio.run(app, host='', port=5000)
	#app.debug = True
	#app.run('', port=3000)






