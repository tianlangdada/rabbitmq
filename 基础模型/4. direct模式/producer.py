# -*- coding: utf-8 -*-

import pika
import random

# 连接 rabbitmq broker
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
# 创建channel
channel = connection.channel()
# 声明direct类型交换机
channel.exchange_declare(exchange='direct_logs', exchange_type='direct')
# 自定义消息类型用于发送到绑定不同的routing_key队列中
message_type = random.choice(["info", "error"])
# 向direct_logs交换机发布消息，根据随机的routing_key路由到不同的队列中
channel.basic_publish(exchange='direct_logs', routing_key=message_type,
                      body=f'This is {message_type} message!'.encode())
# 关闭连接
connection.close()


