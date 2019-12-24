SQLALCHEMY_DATABASE_URI = 'mysql://username:password@host:port/database?charset=utf8'

TCLOUD_ENV = 'dev'
SERVER_ENV = 'dev'

REDIS_HOST = 'host'
REDIS_PORT = 0
REDIS_PASSWORD = ''
REDIS_DB = 0

CELERY_RESULT_BACKEND = f'redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/2'
CELERY_BROKER_URL = f'redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/5'

SECRET = 'vissssa'
ALGORITHM = 'HS256'
TSECRET = 'Lekima'
SALT = "vissssa"

SCKEY = 'yoursckey'
serverchan_url = f'https://sc.ftqq.com/{SCKEY}.send'

EMAIL_SENDER = 'sender@163.com'
EMAIL_PASSWORD = 'your_email_password'
EMAIL_RECEIVERS = ['receivers@163.com']
ISNOTIFICATION = '00'

# OSS
OSSAccessKeyId = 'xx'
OSSAccessKeySecret = 'xx'
OSS_ENDPOINT = 'http://oss-cn-beijing.aliyuncs.com'
OSS_BUCTET_NAME = 'vissssa'
OSSHost = 'http://vissssa.oss-cn-beijing.aliyuncs.com'
CMSHost = 'http://vissssa.club'
