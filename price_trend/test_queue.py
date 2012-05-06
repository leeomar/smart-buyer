#/bin/python

import Queue

pq=Queue.PriorityQueue()
pq.put((2, {'priority': 2}))
pq.put((5, {'priority': 5}))
pq.put((3, {'priority': 3}))
pq.put((0, {'priority': 0}))

while not pq.empty():
    print pq.get()
