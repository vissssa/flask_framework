from library.api.db import EntityModel, db


class RouteStatistics(EntityModel):
    route = db.Column(db.String(100))  # 接口
    service = db.Column(db.String(30))  # 服务
    method = db.Column(db.String(30))  # 请求方式
    count = db.Column(db.Integer, default=1)  # 次数
