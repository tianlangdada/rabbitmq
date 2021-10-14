# -*- coding: utf-8 -*-

import pika
import uuid


class FibonacciRpcClient:

    def __init__(self):

        # 连接 rabbitmq broker
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        # 创建 channel
        self.channel = self.connection.channel()
        # 声明rpc客户端队列，用来接收rpc服务器处理的响应
        client_queue = self.channel.queue_declare(queue='', exclusive=True)
        # 获取响应队列名称
        self.client_queue_name = client_queue.method.queue
        # 消费响应队列消息
        self.channel.basic_consume(
            queue=client_queue,
            on_message_callback=self.callback,
            auto_ack=True
        )
        # 用于将rpc请求与响应关联起来
        self.corr_id = None
        self.response = None

    def callback(self, ch, method, props, body):
        """ 响应回调函数 """
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, n):
        """ 远程过程调用函数 """
        # 创建唯一字符串用于关联请求和响应
        self.corr_id = str(uuid.uuid4())
        # 发布调用信息
        self.channel.basic_publish(
            exchange='',
            routing_key='rpc_queue',
            properties=pika.BasicProperties(
                reply_to=self.client_queue_name,  # 用于命名回调队列(关联响应队列)
                correlation_id=self.corr_id,  # 关联请求和相应的唯一id
            ),
            body=str(n).encode())
        # 若没有返回值循环等待
        while self.response is None:
            # 非阻塞版的channel.start_consuming()
            self.connection.process_data_events()
        return self.response


fibonacci_rpc = FibonacciRpcClient()
print(" [x] Requesting fib(30)")
response = fibonacci_rpc.call(30)
print(" [.] Got %s" % response)
