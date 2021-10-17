# -*- coding: utf-8 -*-

import pika


def callback(ch, method, properties, body):
    print(" [x] Dead Message %r" % body.decode())


# 创建连接和channel
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
# 声明死信交换器、死信队列并绑定
channel.exchange_declare(exchange="dlx_5s", exchange_type="direct")
channel.queue_declare(queue="queue_delay_5s", durable=True)
channel.queue_bind(queue="queue_delay_5s", exchange="dlx_5s", routing_key="routing_5s")
# 开始消费
channel.basic_consume(queue="queue_delay_5s", on_message_callback=callback, auto_ack=True)
print(' [*] Waiting for messages. To exit press CTRL+C')
# 开始消费并阻塞
channel.start_consuming()

