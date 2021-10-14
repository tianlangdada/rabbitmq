# -*- coding: utf-8 -*-

import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
# 声明主交换器、声明队列、绑定队列
channel.exchange_declare(
    exchange="normal_exchange",
    exchange_type="direct",
    arguments={"alternate-exchange": "bak_exchange"}  # 声明备份交换器
)
channel.queue_declare(queue="normal_queue", durable=True)
channel.queue_bind(queue="normal_queue", exchange="normal_exchange", routing_key="normal_key")
# 声明备份交换器(交换器类型为fanout)、声明队列、绑定队列
channel.exchange_declare(exchange="bak_exchange", exchange_type="fanout")
channel.queue_declare(queue="bak_queue", durable=True)
channel.queue_bind(queue="bak_queue", exchange="bak_exchange")
# 发布内容
for message_type in ["normal_key", "error_key"]:
    channel.basic_publish(
        exchange="normal_exchange",
        routing_key=message_type,
        body=f"routing_key: {message_type}".encode()
    )
# 关闭连接
connection.close()

