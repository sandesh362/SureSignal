# celery.py (in project root - misinformation_detector/celery.py)
import os
from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'misinformation_detector.settings')

app = Celery('misinformation_detector')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

# Celery Beat schedule for periodic tasks
app.conf.beat_schedule = {
    'scheduled-data-collection': {
        'task': 'data_ingestion.tasks.scheduled_data_collection',
        'schedule': crontab(minute=0, hour='*/6'),  # Every 6 hours
    },
    'scheduled-text-processing': {
        'task': 'text_processing.tasks.scheduled_text_processing',
        'schedule': crontab(minute=30, hour='*/2'),  # Every 2 hours at 30 min
    },
}

app.conf.timezone = 'UTC'

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')

@app.task
def health_check():
    """Health check task for monitoring"""
    return {'status': 'ok', 'message': 'Celery is working properly'}

# misinformation_detector/__init__.py
# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.
from .celery import app as celery_app

__all__ = ('celery_app',)



# core/management/commands/__init__.py



# core/management/commands/setup_pipeline.py
