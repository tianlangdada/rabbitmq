# -*- coding: utf-8 -*-
import time

import pika


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body.decode())
    # 拒绝消息进入死信交换器
    ch.basic_reject(delivery_tag=method.delivery_tag, requeue=False)
    # ch.basic_ack(delivery_tag=method.delivery_tag)


# 创建连接和channel
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
# 声明交换器、队列并绑定
channel.exchange_declare(exchange="normal_exchange", exchange_type="direct")
channel.queue_declare(queue="normal_queue", durable=True,
                      arguments={
                          "x-max-length": 3,  # 队列最大长度
                          "x-max-length-bytes": 1024,  # 队列最大字节数
                          "x-dead-letter-exchange": "dlx_exchange",
                          "x-dead-letter-routing-key": "dlx_routing_key",
                      })
channel.queue_bind(queue="normal_queue", exchange="normal_exchange", routing_key="normal_key")
# 开始消费
channel.basic_consume(queue="normal_queue", on_message_callback=callback, auto_ack=False)
print(' [*] Waiting for messages. To exit press CTRL+C')
# 开始消费并阻塞
channel.start_consuming()
