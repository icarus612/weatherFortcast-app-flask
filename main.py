from flask import Flask, render_template, url_for, request, redirect
import requests
import os

app = Flask(__name__)

@app.route('/')
def index():
	error = request.args.get('error')
	return render_template('weather.html', weather=None, error=error)

@app.route('/weather')
def weather():
	city = request.args.get('city')
	state = request.args.get('state')
	country = request.args.get('country')
	unit = request.args.get('unit')
	if state:
		req = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city},{state},{country}&units={unit}&appid=b6907d289e10d714a6e88b30761fae22').json()
	else:
		req = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city},{country}&units={unit}&appid=b6907d289e10d714a6e88b30761fae22').json()
	weather = req['weather'][0]
	temp = req['main']
	return render_template('weather.html', weather=weather, temp=temp, unit=unit, error=None)

@app.route('/get_weather', methods=['POST'])
def get_weather():
	try:
		city = request.form['city']
		state = request.form['state']
		country = request.form['country']
		unit = request.form['unit-type']
		print(city, state)
		if city is "" or country is "":
			return redirect(url_for('index', error="You need a city and country."))
		else:
			return redirect(url_for('weather', city=city, country=country, state=state, unit=unit))
	except:
		return redirect(url_for('index'))

port = int(os.environ.get('PORT', 5000)) 
if __name__ == '__main__':
	app.run(threaded=True, port=port)
	