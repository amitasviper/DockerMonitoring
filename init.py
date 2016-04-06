from flask import Flask, render_template, url_for, request, jsonify, Response
import random, time, json
app = Flask(__name__)

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
@app.route('/jsondata')
def json_data():
	time.sleep(1)
	data = {'cpu_usage': [random.randrange(0, 100) for x in range(2)], 'memory_usage': random.randrange(0, 100), 'network_usage' : random.randrange(0, 100), 'io':random.randrange(0, 100)}
	print data
	return jsonify(data)

def get_dummy_container_info():
	return {
             "Id": ''.join(random.choice('0123456789abcdefghijklmnopqrstuvwxyz') for i in range(20)),
             "Names":["/boring_feynman"],
             "Image": "ubuntu:latest",
             "ImageID": ''.join(random.choice('0123456789abcdefghijklmnopqrstuvwxyz') for i in range(64)),
             "Command": "echo 1",
             "Created": 1367854155,
             "Status": "Exit 0",
             "Ports": [{"PrivatePort": 2222, "PublicPort": 3333, "Type": "tcp"}],
             "Labels": {
                     "com.example.vendor": "Acme",
                     "com.example.license": "GPL",
                     "com.example.version": "1.0"
             },
             "SizeRw": 12288,
             "SizeRootFs": 0,
             "NetworkSettings": {
                     "Networks": {
                             "bridge": {
                                      "NetworkID": "7ea29fc1412292a2d7bba362f9253545fecdfa8ce9a6e37dd10ba8bee7129812",
                                      "EndpointID": "2cdc4edb1ded3631c81f57966563e5c8525b81121bb3706a9a9a3ae102711f3f",
                                      "Gateway": "172.17.0.1",
                                      "IPAddress": "172.17.0.2",
                                      "IPPrefixLen": 16,
                                      "IPv6Gateway": "",
                                      "GlobalIPv6Address": "",
                                      "GlobalIPv6PrefixLen": 0,
                                      "MacAddress": "02:42:ac:11:00:02"
                              }
                     }
             }
     }

@app.route('/jsondata_containers')
def json_data_containers():
	data = []
	for i in range(10):
		data.append(get_dummy_container_info())
	#print data
	return Response(json.dumps(data),  mimetype='application/json')


if __name__ == "__main__":
	app.debug = True
	app.run('', port=3000)






