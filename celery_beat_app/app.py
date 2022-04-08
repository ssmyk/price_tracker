from celery import Celery

#celery_beat_schedule = {"time_scheduler": {"task": "job.run_update","schedule": 10.0,'options': {'queue' : 'beat'}}}
celery_beat_schedule = {"time_scheduler": {"task": "job.run_update","schedule": 10.0}}

#celery_app = Celery('beat', queue='beat',backend='rpc://', broker='amqp://beat:beat@rabbitmq/beat',beat_schedule=celery_beat_schedule)
celery_app = Celery('beat',backend='rpc://', broker='amqp://beat:beat@rabbitmq/beat',beat_schedule=celery_beat_schedule)
