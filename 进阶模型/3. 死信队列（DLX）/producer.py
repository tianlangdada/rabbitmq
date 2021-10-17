# -*- coding: utf-8 -*-

import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
# ######################################### 声明主交换器 #########################################
channel.exchange_declare(exchange="normal_exchange", exchange_type="direct")
channel.queue_declare(queue="normal_queue", durable=True,
                      arguments={
                          "x-max-length": 3,  # 队列最大长度
                          "x-max-length-bytes": 1024,  # 队列最大字节数
                          "x-dead-letter-exchange": "dlx_exchange",
                          "x-dead-letter-routing-key": "dlx_routing_key",
                      })
channel.queue_bind(queue="normal_queue", exchange="normal_exchange", routing_key="normal_key")
# ######################################## 声明死信交换器 #########################################
channel.exchange_declare(exchange="dlx_exchange", exchange_type="direct")
channel.queue_declare(queue="dlx_queue", durable=True)
channel.queue_bind(queue="dlx_queue", exchange="dlx_exchange", routing_key="dlx_routing_key")
# ########################################## 发布消息 ############################################
for i in range(3):
    channel.basic_publish(
        exchange="normal_exchange",
        routing_key="normal_key",
        body=f"this is a normal message {i}".encode(),
    )
# 关闭连接
connection.close()
