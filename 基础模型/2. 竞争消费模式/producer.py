# -*- coding: utf-8 -*-

import pika

# 连接 rabbitmq broker
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
# 创建channel
channel = connection.channel()
# 声明队列
channel.queue_declare(queue='task_queue', durable=True)  # 队列持久化
# 发布持久化消息
channel.basic_publish(
    exchange='',
    routing_key='task_queue',
    body=b'Hello World!',
    properties=pika.BasicProperties(delivery_mode=2)  # 消息持久化
)

# 关闭连接
connection.close()
