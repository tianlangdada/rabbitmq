# -*- coding: utf-8 -*-

import pika
import time


# 消费者回调函数
def callback(ch, method, properties, body):
    print(" [x] Received %r" % body.decode())
    # 延时, 模拟处理重消息消费者死掉无法发送ack, 生产者会将消息重新分配
    time.sleep(10)
    print(" [x] Done")
    # 确认ack
    ch.basic_ack(delivery_tag=method.delivery_tag)


# 连接 rabbitmq broker
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
# 创建 channel
channel = connection.channel()
# 声明持久化队列
channel.queue_declare(queue='task_queue', durable=True)
# 没有确认ack的条数超过prefetch_count时, 该消费者将不会分配消息(需要auto_ack=False生效)
channel.basic_qos(prefetch_count=1)
# 从队列中消费消息(不会自动ack)
channel.basic_consume(queue='task_queue', on_message_callback=callback)
print(' [*] Waiting for messages. To exit press CTRL+C')
# 开始消费并阻塞
channel.start_consuming()
