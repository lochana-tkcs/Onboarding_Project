from celery import Celery

app = Celery('tasks', broker='pyamqp://guest@localhost//')

# app.conf.update(
#     result_backend='rpc://',
# )

app.conf.update(
    result_backend='rpc://',
    broker_connection_retry_on_startup=True
)
