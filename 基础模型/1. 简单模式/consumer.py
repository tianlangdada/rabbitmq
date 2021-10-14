# -*- coding: utf-8 -*-

import pika


# 消费者回调函数
def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)


# 连接 rabbitmq broker
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
# 创建 channel
channel = connection.channel()
# 声明队列
channel.queue_declare(queue='hello')
# 从队列中消费消息，并自动确认ack
channel.basic_consume(queue='hello', auto_ack=True, on_message_callback=callback)
print(' [*] Waiting for messages. To exit press CTRL+C')
# 开始消费并阻塞
channel.start_consuming()



