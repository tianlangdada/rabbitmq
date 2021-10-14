# -*- coding: utf-8 -*-
import time

import pika


def return_callback(ch, method, properties, body):
    print(1)
    print("return callback message '%s'".format(body))


# 连接 rabbitmq broker
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
# 创建channel
channel = connection.channel()
# 声明topic类型交换机
channel.exchange_declare(exchange='topic_file', exchange_type='topic')
# topic模式的routing_key可以使用.分割并进行模糊匹配
key_list = ["info.log", "error.log", "xxx.txt", "ooo.txt", "rabbitmq.kafka.txt", "txt"]
for message_type in key_list:
    # 向direct_logs交换机发布消息，根据随机的routing_key路由到不同的队列中
    channel.basic_publish(exchange='topic_file',
                          routing_key=message_type,
                          body=f'This is a {message_type}!'.encode(),
                          mandatory=True)

channel.add_on_return_callback(return_callback)
# 关闭连接
connection.close()


