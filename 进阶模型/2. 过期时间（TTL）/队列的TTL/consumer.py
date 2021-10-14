# -*- coding: utf-8 -*-

import pika


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body.decode())


# 创建连接和channel
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
# 声明交换器、队列并绑定
channel.exchange_declare(exchange="ttl_exchange", exchange_type="direct")
channel.queue_declare(queue="ttl_queue", durable=True, arguments={"x-expires": 180000})
channel.queue_bind(queue="ttl_queue", exchange="ttl_exchange", routing_key="ttl_key")
# 开始消费
channel.basic_consume(queue="ttl_queue", on_message_callback=callback, auto_ack=True)
print(' [*] Waiting for messages. To exit press CTRL+C')
# 开始消费并阻塞
channel.start_consuming()
