# -*- coding: utf-8 -*-

import pika

# 连接 rabbitmq broker
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
# 创建channel
channel = connection.channel()
# 声明队列
channel.queue_declare(queue='hello')
# 向队列发布消息
channel.basic_publish(exchange='', routing_key='hello', body=b'Hello World!')
# 关闭连接
connection.close()
