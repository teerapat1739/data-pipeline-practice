import pika
import json
from configuration import GetConfiguration
# print('test')
cfg = GetConfiguration()
port = cfg["rabbit_url"]
database = cfg["rabbit_database"]["index"]

database = cfg["rabbit_database"]["index"]
class rabbit_publish:
    def __init__(self):
        self.conn = pika.BlockingConnection(
                        # pika.ConnectionParameters(host='localhost'))
                        # pika.ConnectionParameters(host='amqp://rabbitmq?connection_attempts=5&retry_delay=5'))
                        pika.ConnectionParameters(host='rabbitmq'))

    def send(self, payload, routing_key, exchange_key="amq.direct"):
        body = json.dumps(payload, ensure_ascii=False)
        channel = self.conn.channel()
        
        channel.queue_declare(queue=routing_key)

        channel.basic_publish(exchange='',
                              routing_key=routing_key, body=body)
                   
        channel.close()