# -*- coding: utf-8 -*-

import pika


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body.decode())


# 创建连接和channel
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
# 声明交换器、队列并绑定
channel.exchange_declare(
    exchange="bak_exchange",
    exchange_type="fanout",
)
channel.queue_declare(queue="bak_queue", durable=True)
channel.queue_bind(queue="bak_queue", exchange="bak_exchange")
# 开始消费
channel.basic_consume(queue="bak_queue", on_message_callback=callback, auto_ack=True)
print(' [*] Waiting for messages. To exit press CTRL+C')
# 开始消费并阻塞
channel.start_consuming()
