# -*- coding: utf-8 -*-

import pika


# 消费者回调函数
def callback(ch, method, properties, body):
    print(" [x] Received %r" % body.decode())


# 连接 rabbitmq broker
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
# 创建 channel
channel = connection.channel()
# 声明direct类型交换器
channel.exchange_declare(exchange='direct_logs', exchange_type='direct')
# 声明队列(随机队列名称，声明队列只能允许当前连接访问，不可多个消费者消费一个队列)
result = channel.queue_declare(queue='', exclusive=True)
# 获取队列随机的名称
queue_name = result.method.queue

# ******************************************************************************************
# 交换器绑定队列，并且只接收路由为error的消息
channel.queue_bind(exchange='direct_logs', queue=queue_name, routing_key="error")
# ******************************************************************************************

# 从队列中消费消息
channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
print(' [*] Waiting for messages. To exit press CTRL+C')
# 开始消费并阻塞
channel.start_consuming()


