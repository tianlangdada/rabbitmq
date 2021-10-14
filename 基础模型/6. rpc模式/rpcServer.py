# -*- coding: utf-8 -*-

import pika

# 连接 rabbitmq broker
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
# 创建 channel
channel = connection.channel()
# 声明rpc服务端队列，用来处理rpc客户端消息
channel.queue_declare(queue='rpc_queue')


# 执行函数(斐波那契数列)
def fib(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n - 1) + fib(n - 2)


# rpc服务器队列回调处理函数
def callback(ch, method, props, body):
    n = int(body)
    print(" [.] fib(%s)" % n)
    response = fib(n)

    # 将处理结果再次发布给客户端
    ch.basic_publish(
        exchange='',
        routing_key=props.reply_to,  # 回调响应队列
        properties=pika.BasicProperties(
            correlation_id=props.correlation_id  # 用于将rpc请求与响应相关联
        ),
        body=str(response))
    # 主动确认ack
    ch.basic_ack(delivery_tag=method.delivery_tag)


# 没有确认ack的条数超过prefetch_count时, 该消费者将不会分配消息(需要auto_ack=False生效)
channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='rpc_queue', on_message_callback=callback)

print(" [x] Awaiting RPC requests")
channel.start_consuming()

