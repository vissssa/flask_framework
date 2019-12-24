from flask import Flask

import public_config
from library.api.db import db
from tasks.extentions import make_celery

app = Flask(__name__)

app.config.from_object(public_config)
db.init_app(app)
celery = make_celery(app)
