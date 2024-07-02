from celery import Celery

app = Celery('tasks', broker='pyamqp://guest@localhost//')

app.conf.update(
    result_backend='rpc://',
)
