# -*- coding: utf-8 -*-

import pika

# 连接 rabbitmq broker
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
# 创建channel
channel = connection.channel()
# 声明fanout类型交换机
channel.exchange_declare(exchange='logs', exchange_type='fanout')
# 向logs交换机发布消息，同时发送到绑定次交换机上的所有队列
channel.basic_publish(exchange='logs', routing_key='', body=b'Hello World!')
# 关闭连接
connection.close()


