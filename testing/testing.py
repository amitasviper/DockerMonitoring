from flask import Flask, render_template

app = Flask(__name__)

#Renders the home page of the application server.
@app.route('/')
@app.route('/home')
def home():
	return render_template('testing.html')

if __name__ == "__main__":
	app.debug = True
	app.run('', port=4000)