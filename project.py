import paho.mqtt.client as mqtt
import ssl
import psutil
import time
import json
 

BROKER = "10.191.158.14"  
PORT = 8883
TOPIC = "security/sensor/data"
CA_CERT = "ca.crt"      
SENSOR_ID = "Laptop_3"  

 
def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print(f" {SENSOR_ID} успешно подключен к брокеру!")
    else:
        print(f" Ошибка подключения, код: {rc}")
 

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
 

client.tls_set(ca_certs=CA_CERT, cert_reqs=ssl.CERT_NONE)
client.tls_insecure_set(True) 

 
client.on_connect = on_connect
 
try:
    print(f" Попытка подключения к {BROKER}...")
    client.connect(BROKER, PORT, 60)
    client.loop_start()
 
    while True:
        cpu_load = psutil.cpu_percent(interval=1)
        payload = json.dumps({
            "sensor_id": SENSOR_ID,
            "value": cpu_load
        })
        client.publish(TOPIC, payload)
        print(f" Отправлено: {payload}")
        time.sleep(5)
 
except Exception as e:
    print(f" Произошла ошибка: {e}")
except KeyboardInterrupt:
    print(" Остановка...")
    client.loop_stop()
    client.disconnect()