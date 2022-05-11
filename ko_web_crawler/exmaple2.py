from queue import Queue

queue = Queue()
queue.put(1)
print(queue.empty())
print(queue.get())
print(queue.empty())
