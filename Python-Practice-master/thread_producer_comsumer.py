#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Python中的生产者，消费者模型
'''
from threading import Thread, Lock, Condition
import time
import random
from Queue import Queue

queue = []
MAX_NUM = 10
lock = Lock()
condition = Condition()

'''
Condition内含lock
Condition的acquire()和release()内部调用了lock的acquire()和release()
'''


class ProducerThread(Thread):
    def run(self):
        nums = range(5)
        global queue
        while True:
            #lock.acquire()
            condition.acquire()
            if len(queue) == MAX_NUM:
                print 'Queue full, producer is waiting'
                condition.wait()
                print 'Space in queue, Consumer notified the producer'
            num = random.choice(nums)
            queue.append(num)
            print 'Produced', num
            condition.notify()
            condition.release()
            #lock.release()
            time.sleep(random.random())


class ConsumerThread(Thread):
    def run(self):
        global queue
        while True:
            #lock.acquire()
            condition.acquire()
            if not queue:
                print 'Nothing in queue, but Consumer will try to consume'
                condition.wait()
                print 'Producer added something to queue and notified the consumer'
            num = queue.pop(0)
            print 'Consumed', num
            condition.notify()
            condition.release()
            #lock.release()
            time.sleep(random.random())


ProducerThread().start()
ConsumerThread().start()


'''
更新：使用Queue代替list
Queue封装了Condition的行为，如wait()，notify()，acquire()
'''

new_queue = Queue()

class NewProducerThread(Thread):
    def run(self):
        nums = range(5)
        global new_queue
        while True:
            num = random.choice(nums)
            new_queue.put(num)
            print 'Produced', num
            time.sleep(random.random())


class NewConsumerThread(Thread):
    def run(self):
        global new_queue
        while  True:
            num = new_queue.get()
            new_queue.task_done()
            print 'Consumed', num
            time.sleep(random.random())

NewProducerThread().start()
NewConsumerThread().start()