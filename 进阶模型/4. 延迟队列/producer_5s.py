# -*- coding: utf-8 -*-

import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
# ######################################### 声明主交换器 #########################################
channel.exchange_declare(exchange="normal_exchange", exchange_type="direct")
# 队列内消息过期时间5s，到期后进入死信交换器
channel.queue_declare(queue="queue_5s", durable=True,
                      arguments={
                          "x-message-ttl": 5000,  # 消息过期时间(5s)
                          "x-dead-letter-exchange": "dlx_5s",  # 死信交换器
                      })
channel.queue_bind(queue="queue_5s", exchange="normal_exchange", routing_key="routing_5s")
# ######################################## 声明死信交换器 #########################################
channel.exchange_declare(exchange="dlx_5s", exchange_type="direct")
channel.queue_declare(queue="queue_delay_5s", durable=True)
# 如果未指定死信队列的 routing_key，则使用原队列的 routing_key
channel.queue_bind(queue="queue_delay_5s", exchange="dlx_5s", routing_key="routing_5s")
# ########################################## 发布消息 ############################################
channel.basic_publish(
    exchange="normal_exchange",
    routing_key="routing_5s",
    body=f"this is a delay message, delay time [5S]".encode(),
)
# 关闭连接
connection.close()
