from datetime import datetime
import Adafruit_DHT as dht
import sqlite3
import os

# Get path info
db_file = 'roomtemp.db'
curr_dir = os.path.abspath(os.path.dirname(__file__))
full_db_path = os.path.join(curr_dir, db_file)


# First capture time, humidity and temp to log in DB
current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
humidity, temperature = dht.read_retry(dht.DHT22, 4)
temperature = temperature * 9/5.0 + 32

print(current_time, format(temperature, '.2f'), format(humidity, '.2f'))

# Open connection to DB and create cursor
dbconn = sqlite3.connect(full_db_path)
c = dbconn.cursor()
c.execute('insert into roomtemp (temperature, humidity, timestamp) values (?, ?, ?);', (format(temperature, '.2f'), format(humidity, '.2f'), current_time))
dbconn.commit()
dbconn.close()
