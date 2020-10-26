#!/usr/bin/env python
import pika, sys, os
import json
from configuration import GetConfiguration


cfg = GetConfiguration()
routing_key = cfg["rabbit_database"]["routing_key"]
def main():
    # connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
    print("-----",connection)
    # connection = pika.BlockingConnection(pika.ConnectionParameters(host='amqp://rabbitmq?connection_attempts=5&retry_delay=5'))
    channel = connection.channel()

    channel.queue_declare(queue=routing_key)

    def callback(ch, method, properties, body):
        dataJsonFile = []
        payload = json.loads(body)
        print(payload['title'])
        with open('file/news.json') as f:
            dataJsonFile = json.load(f)
        
        dataJsonFile.append(payload)

        with open('file/news.json', 'w') as json_file:
            json.dump(dataJsonFile, json_file, ensure_ascii=False)

    channel.basic_consume(queue=routing_key, on_message_callback=callback, auto_ack=True)

    channel.start_consuming()

if __name__ == '__main__':
    main()