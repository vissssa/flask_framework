from flask import Blueprint

from apps.public.daos.public import (
    get_statistics_route_db,
    record_statistics_route,
    update_module,
)
from library.api.extentions import parse_json_formdict, validation

public = Blueprint('public', __name__)


@public.route('/module/<int:module_id>', methods=['POST'])
@validation('POST:module_update')
def post_demo(module_id):
    """
    validation为数据验证装饰器，类似于wtf，这里做成yaml文件方便配置，易于阅读
    返回值在tflask中有定制，这里使用字典也是为了更直观（不为了少些几个单词而牺牲可读性）
    :param module_id:
    :type module_id:
    :return:
    :rtype:
    """
    post_form = parse_json_formdict('module_update')
    code = update_module(module_id, post_form)

    return {'code': code}


@public.route('/route/statistics/db/', methods=['GET'])
def route_statistics_db():
    code, data = get_statistics_route_db()
    return {'code': code, 'data': data}


@public.route('/route/statistics/crontab/', methods=['GET'])
def route_statistics_crontab():
    data = record_statistics_route()
    return {'data': data}
