import queue

q1 = queue.Queue()
q1.put(1)
q1.put(2)

print(q1.queue[0])
print(q1.queue[0])
print(q1.queue[1])

for i in range(len(q1.queue)):
    t = q1.queue[i]
    print(t)