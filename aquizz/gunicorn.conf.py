import os
import multiprocessing

port = os.getenv('PORT', '5000')
bind = '0.0.0.0:' + str(port)
worker_class = 'gevent'
workers = multiprocessing.cpu_count() * 2 + 1
threads = workers * 2
max_requests = 1000
