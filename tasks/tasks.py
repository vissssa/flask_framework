from datetime import datetime, timedelta

import requests

from library.temail import send_email
from library.trpc import Trpc
from public_config import serverchan_url, ISNOTIFICATION
from tasks import celery
from tasks.extentions import exception_handler, limit_au


def pass_notification():
    print('本次报警被过滤')


# 控制报警函数一分钟只报一次警
def timeguard(time_interval, default=None):
    def decorator(function):
        function.__last_run = datetime.min

        def guard(*args, **kwargs):
            now = datetime.now()
            if now - function.__last_run >= time_interval:
                function.__last_run = now
                return function(*args, **kwargs)
            elif default is not None:
                return default(*args, **kwargs)

        return guard

    return decorator


# 一个装饰器  控制记录日活用户一天一个id

# @celery.task(name='record_active_user')
# @limit_au
# @exception_handler
# def record_active_user(user_id, modified_time):
#     user_trpc = Trpc('auth')
#     data = user_trpc.requests('get', '/user/record/au', {'user_id': user_id, 'modified_time': modified_time})
#     return data
#
#
# @celery.task(name='record_au_everyday')
# @exception_handler
# def record_au_everyday():
#     user_trpc = Trpc('auth')
#     data = user_trpc.requests('get', '/user/statistics/au')
#     return data


@celery.task(name='record_statistics_route_crontab')
@exception_handler
def record_statistics_route_crontab():
    public_trpc = Trpc('public')
    data = public_trpc.requests('get', '/public/route/statistics/crontab')
    return data


@celery.task(name='notification')
@exception_handler
@timeguard(timedelta(seconds=60), pass_notification)
def send_notification(code, desp):
    is_wechat = ISNOTIFICATION[0]
    is_email = ISNOTIFICATION[1]
    local_ip = None
    try:
        res = requests.get('http://httpbin.org/ip', timeout=8)
        local_ip = res.json()['origin'].split(',')[0]
    except Exception as e:
        print(str(e))
    if local_ip:
        if local_ip == 'local_ip':
            env = '测试环境'
        else:
            env = '正式环境'
    else:
        env = 'ip地址查询失败，详见日志'
    # serverchan
    if is_wechat == '1':
        requests.get(serverchan_url, params={'text': f'{env}: {code}', 'desp': desp})
    # email
    if is_email == '1':
        send_email(env, desp)
