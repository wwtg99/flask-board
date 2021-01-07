from celery.utils.log import get_task_logger
from flask import current_app as app
from worker import celery


# logger = get_task_logger(__name__)
# retry_for = (Exception, )
# retry_kwargs = {
#     'max_retries': 3,
#     'countdown': 1
# }


# define your tasks here
# @celery.task(autoretry_for=retry_for, retry_kwargs=retry_kwargs)
# def test():
#     # do something within flask app
#     pass
