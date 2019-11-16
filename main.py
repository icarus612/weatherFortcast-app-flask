from flask import Flask, render_template, url_for, request, redirect
import requests
import os

app = Flask(__name__)

@app.route('/')
def index():
	return render_template('weather.html', weather=None, temp=None)

@app.route('/<city>/<country>', methods=['GET', 'POST'])
@app.route('/<city>/<state>/<country>', methods=['GET', 'POST'])
def weather(city, country, state=None):
	if state:
		req = requests.get(f'https://openweathermap.org/data/2.5/weather?q={city},{state},{country}&units=imperial&appid=b6907d289e10d714a6e88b30761fae22').json()
	else:
		req = requests.get(f'https://openweathermap.org/data/2.5/weather?q={city},{country}&units=imperial&appid=b6907d289e10d714a6e88b30761fae22').json()
	weather = req['weather'][0]
	temp = req['main']
	print(weather, temp)
	return render_template('weather.html', weather=weather, temp=temp)

@app.route('/get_weather', methods=['POST'])
def get_weather():
	try:
		city = request.form['city']
		state = request.form['state'] if request.form['state'] != "" else None
		country = request.form['country']
		return redirect(url_for('weather', city=city, country=country, state=state))
	except:
		return redirect(url_for('index'))

port = int(os.environ.get('PORT', 5000)) 
if __name__ == '__main__':
	app.run(threaded=True, port=port)