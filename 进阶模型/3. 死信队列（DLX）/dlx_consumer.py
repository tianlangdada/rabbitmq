# -*- coding: utf-8 -*-

import pika


def callback(ch, method, properties, body):
    print(" [x] Dead Message %r" % body.decode())


# 创建连接和channel
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
# 声明死信交换器、死信队列并绑定
channel.exchange_declare(exchange="dlx_exchange", exchange_type="direct")
channel.queue_declare(queue="dlx_queue", durable=True)
channel.queue_bind(queue="dlx_queue", exchange="dlx_exchange", routing_key="dlx_routing_key")
# 开始消费
channel.basic_consume(queue="dlx_queue", on_message_callback=callback, auto_ack=True)
print(' [*] Waiting for messages. To exit press CTRL+C')
# 开始消费并阻塞
channel.start_consuming()

