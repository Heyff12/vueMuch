# coding: utf-8
import os

HOME = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

bind = '0.0.0.0:8002'

threads = 8
backlog = 1024

workers = 1
worker_class = 'gevent'

loglevel = 'info'
access_log_format = '%(t)s %(p)s %(h)s "%(r)s" %(s)s %(L)s %(b)s "%(f)s" "%(a)s"'
accesslog = os.path.join(HOME, 'log', 'gunicorn_access.log')
errorlog = os.path.join(HOME, 'log', 'gunicorn_error.log')
