import Adafruit_DHT as dht
humidity, temperature = dht.read_retry(dht.DHT22, 4)
temperature = temperature * 9/5.0 + 32
print ('Temp={0:0.1f}*F'.format(temperature))
