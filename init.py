from flask import Flask, render_template, url_for, request, jsonify, Response
import random, time, json, urllib2, requests
app = Flask(__name__)

SERVER_IP = '192.168.144.148'
SERVER_PORT = '4243'
SERVER_ADDRESS = 'http://' + SERVER_IP + ':' + SERVER_PORT

#Renders the home page of the application server.
@app.route('/')
@app.route('/home')
def home():
	print url_for('static', filename='../js/statistics.js')
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
		print "Rendering container id page"
		return render_template('container_info.html', title="Container Info")


@app.route('/threshold/')
def threshold():
	return render_template('threshold.html')

@app.route('/error_report/')
def error_report():
	return render_template('error_report.html')

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
  return Response(json.dumps(data),  mimetype='application/json')

if __name__ == "__main__":
	app.debug = True
	app.run('', port=3000)






