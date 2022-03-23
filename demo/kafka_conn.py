import datetime
import json
import time
from kafka import KafkaProducer

producer=KafkaProducer(bootstrap_servers='10.0.40.86:9092')
for i in range(111):
    future = producer.send('test', json.dumps(
        {"method": "get", "step": i, "type": "test", "testName": "kafka",
         "cid": "{0}".format(datetime.datetime.now().strftime('%Y%m%d%H%M%S')),
         "info": "demo{}".format(1)}).encode())
    record_metadata = future.get(timeout=10)
    print(record_metadata, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    time.sleep(3)