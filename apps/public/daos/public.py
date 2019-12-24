from apps.public.models.public import RouteStatistics
from apps.public.settings.config import ROUTE_STATISTICS
from library.api.db import db, t_redis
from library.api.render import row2list


# 定时任务调用   来自jobs服务
def record_statistics_route():
    routes = t_redis.keys(f'{ROUTE_STATISTICS}*')
    for r in routes:
        server_info = {'name': '', 'routes': [], 'count': 0}
        r_info = t_redis.hgetall(r)
        r_name = r.replace(ROUTE_STATISTICS, '')
        server_info['name'] = r_name
        add_list = []

        for k, v in r_info.items():
            v = int(v)
            k_info = k.split(']')
            method = k_info[0].replace('[', '')
            route = k_info[1]
            ret = RouteStatistics.query.filter_by(service=r_name,
                                                  route=route,
                                                  method=method).first()
            if ret:
                ret.count = v
            else:
                ret = RouteStatistics(
                    service=r_name,
                    route=route,
                    method=method,
                    count=v
                )
            add_list.append(ret)

        with db.auto_commit():
            db.session.add_all(add_list)
    return 'success'


def get_statistics_route_db():
    query = RouteStatistics.query.add_columns(
        RouteStatistics.route,
        RouteStatistics.service,
        RouteStatistics.method,
        RouteStatistics.count,
    ).all()
    data = row2list(query)
    return 0, data


def update_module(module_id, post_form):
    pass
