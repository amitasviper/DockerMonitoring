from flask import Flask, render_template, url_for, request, jsonify
import random, time
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
	if container_id == None:
		print "Rendering empty container page"
	else:
		print "Rendering graph template"
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
	data = {'cpu_usage': [random.randrange(0, 100) for x in range(3)], 'memory_usage': random.randrange(0, 100), 'network_usage' : random.randrange(0, 100), 'io':random.randrange(0, 100)}
	print data
	return jsonify(data)


if __name__ == "__main__":
	app.debug = True
	app.run('', port=3000)






