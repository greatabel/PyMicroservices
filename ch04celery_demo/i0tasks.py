from celery import Celery

app = Celery('task', backend='rpc://', broker='redis://localhost:6379')

@app.task
def add(x, y):
    return x + y
