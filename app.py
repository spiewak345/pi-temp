from flask import Flask, render_template, g
from gpiozero import CPUTemperature
from datetime import datetime
import Adafruit_DHT as dht
import os
import sqlite3

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'roomtemp.db')
))

def connect_db():
    """Connects to the spcific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def get_db():
    """Opens a new database connection if there is none yet 
    for the current application context."""
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

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
    db = get_db()
    cur = db.execute('select temperature, humidity, timestamp from roomtemp order by timestamp desc limit 168')
    temps = cur.fetchall()
    return render_template('templog.html', temps=temps)

@app.route('/hello/<name>')
def hello(name):
    return render_template('page.html', name=name)

@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the requtest"""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
