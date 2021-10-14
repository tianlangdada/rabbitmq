# -*- coding: utf-8 -*-

import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
# 声明主交换器
channel.exchange_declare(exchange="ttl_exchange", exchange_type="direct")
# 声明队列，定义队列的过期时间为180秒(单位毫秒)
channel.queue_declare(
    queue="ttl_queue",
    durable=True,
    arguments={"x-expires": 180000}
)
# 绑定交换机和队列
channel.queue_bind(queue="ttl_queue", exchange="ttl_exchange", routing_key="ttl_key")
# 发布消息，定义每条消息的过期时间(单位毫秒)
channel.basic_publish(
    exchange="ttl_exchange",
    routing_key="ttl_key",
    body="this is a ttl message".encode(),
    # properties=pika.BasicProperties(expiration=6000)  # 此条消息过期时间为6S
)
# 关闭连接
connection.close()

