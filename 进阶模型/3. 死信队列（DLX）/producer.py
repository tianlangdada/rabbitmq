# -*- coding: utf-8 -*-

import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
# 声明主交换器
channel.exchange_declare(exchange="normal_exchange", exchange_type="direct")
# 声明队列，同时声明队列最大长度与最大字节数，两者全部设置则执行首先到达的限制
channel.queue_declare(
    queue="ttl_queue",
    durable=True,
    arguments={
        "x-max-length": 10,  # 队列最大长度
        "x-max-length-bytes": 1024  # 队列最大字节数
    }
)
# 绑定交换机和队列
channel.queue_bind(queue="normal_queue", exchange="normal_exchange", routing_key="normal_key")
# 发布消息，定义每条消息的过期时间(单位毫秒)
channel.basic_publish(
    exchange="normal_exchange",
    routing_key="normal_key",
    body="this is a normal message".encode(),
    # properties=pika.BasicProperties(expiration=6000)  # 此条消息过期时间为6S
)
# 关闭连接
connection.close()

