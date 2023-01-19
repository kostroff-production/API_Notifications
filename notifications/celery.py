import os

from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module for the 'celery_prod' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'notifications.settings')
os.environ.setdefault('FORKED_BY_MULTIPROCESSING', '1')

app = Celery('notifications')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery_prod-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


app.conf.beat_schedule = {
    'send_message_every_1_minutes': {
        'task': 'app.tasks.schedule_send',
        'schedule': crontab()
    },
    'send_statistic_every_5_minutes': {
        'task': 'app.tasks.send_statistic',
        'schedule': crontab(minute='*/5')
    }
}


