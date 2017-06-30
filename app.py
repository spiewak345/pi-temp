from flask import Flask, render_template
from gpiozero import CPUTemperature
from datetime import datetime
import Adafruit_DHT as dht

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cputemp')
def cputemp():
    cpu = CPUTemperature()
    temp = cpu.temperature
    return render_template('cpu.html', temp=str(temp))

@app.route('/roomtemp')
def roomtemp():
    current_time = str(datetime.now())
    humidity, temperature = dht.read_retry(dht.DHT22, 4)
    temperature = temperature * 9/5.0 + 32
    return render_template('roomtemp.html', current_time=str(current_time), temperature=format(temperature, '.2f'), humidity=format(humidity, '.2f'))

@app.route('/templog')
def templog():
    return render_template('templog.html')

@app.route('/hello/<name>')
def hello(name):
    return render_template('page.html', name=name)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
