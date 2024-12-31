import json
import network
import time
from umqtt.simple import MQTTClient
import dht 
from machine import Pin

led = machine.Pin("LED", machine.Pin.OUT)
sensor = dht.DHT22(Pin(15))

wifi_ssid = "BLAH" #change
wifi_password = "BLAH" #change

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(wifi_ssid, wifi_password)
while wlan.isconnected() == False:
    print('Waiting for connection...')
    time.sleep(1)
print("Connected to WiFi")

mqtt_host = '192.168.1.141' #change
mqtt_publish_topic = "XYZ/feeds/principal"  #change
mqtt_port = 1883 #change
mqtt_client_id = "sensor_1" #change

mqtt_client = MQTTClient(
        client_id=mqtt_client_id,
        server=mqtt_host,
        port=mqtt_port)

mqtt_client.connect()

try:
    while True:
        sensor.measure()
        temp = sensor.temperature()
        humidity = sensor.humidity()

        data = {
            "temperature": temp, 
            "humidity": humidity
        }
        
        json_data = json.dumps(data)
        mqtt_client.publish(mqtt_publish_topic, json_data)

        led.on()
        time.sleep(0.3)
        led.off()
        time.sleep(3)
except Exception as e:
    print(f'Failed to publish message: {e}')
finally:
    mqtt_client.disconnect()
