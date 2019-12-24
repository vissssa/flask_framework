import requests
import wrapt
from celery import Celery
from celery.schedules import crontab

from library.api.db import t_redis


def make_celery(app):
    celery = Celery(
        app.import_name,
        broker=app.config['CELERY_BROKER_URL'],
        backend=app.config['CELERY_RESULT_BACKEND'],
        include=['tasks.tasks']
    )
    celery.conf.beat_schedule = {
        'record_au_everyday': {
            'task': 'record_au_everyday',
            'schedule': crontab(hour=23, minute=30),
            'args': None,
        },
        'record_statistics_route_crontab': {
            'task': 'record_statistics_route_crontab',
            'schedule': crontab(minute='*/10'),
            'args': None,
        },
    }

    celery.conf.timezone = 'Asia/Shanghai'

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery


@wrapt.decorator
def exception_handler(wrapped, instance, args, kwargs):
    task_name = wrapped.__name__
    try:
        res = wrapped(*args, **kwargs)
    except requests.Timeout as e:
        print(f'{task_name}执行失败, 原因:{str(e)}')
        return False
    except Exception as e:
        print(f'{task_name}执行失败, 原因:{str(e)}')
        return False
    else:
        print(f'{task_name}执行成功')
        print(res)
        return True


@wrapt.decorator
def limit_au(wrapped, instance, args, kwargs):
    user_id = args[0]
    # 保存1小时的日活记录，减少auth接口的请求
    is_online = t_redis.get(f'limit_au_{user_id}')
    if is_online is None:
        t_redis.set(f'limit_au_{user_id}', 1, ex=5 * 60)
        wrapped(*args, **kwargs)
    else:
        print('smart skip this func')
        return True
