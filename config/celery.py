from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Set the default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Update Celery configuration for Windows
app.conf.update(
    broker_url=os.environ.get('CELERY_BROKER_URL'),
    result_backend=os.environ.get('CELERY_RESULT_BACKEND'),
    worker_pool_restarts=True,  # Required for Windows
    broker_connection_retry_on_startup=True
)

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
    