import os
import time

from celery import Celery

from calculations_libs.long_calculation import long_calculation


celery = Celery(__name__)
celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379")
celery.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379")


@celery.task(name="create_task", bind=True)  # task bedzie powiazany z obiektem taska
def create_task(self, task_type):  # dodajemy self - reprezentacja obiektu
    result = long_calculation(self)
    return result
