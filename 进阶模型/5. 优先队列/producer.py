# -*- coding: utf-8 -*-

import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
# 声明主交换器
channel.exchange_declare(exchange="priority_exchange", exchange_type="direct")
# 声明队列
channel.queue_declare(
    queue="priority_queue",
    durable=True,
    arguments={"x-max-priority": 10}  # 定义队列优先级为10级(值越大级别越高)
)
# 绑定交换机和队列
channel.queue_bind(queue="priority_queue", exchange="priority_exchange", routing_key="priority_key")
# 发布消息
channel.basic_publish(
    exchange="priority_exchange",
    routing_key="priority_key",
    body="this is a priority message".encode(),
    properties=pika.BasicProperties(priority=10)  # 定义消息有限级为10级(值越大级别越高)
)
# 关闭连接
connection.close()

