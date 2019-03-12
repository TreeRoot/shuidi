import os

base_dir = os.path.abspath('.')

static_path = os.path.join(base_dir, 'static')
template_path = os.path.join(base_dir, 'templates')

cookie_secret = 111111111111111

request_info = True
debug = True
login_url = '/user/login'


# platform db
PLATFORM_MONGODB_HOST = '127.0.0.1'
PLATFORM_MONGODB_PORT = 27017
PLATFORM_MONGODB_DEFAULT = 'platform'


# workflow
WORKFLOW_MONGODB_HOST = '127.0.0.1'
WORKFLOW_MONGODB_PORT = 27017
WORKFLOW_MONGODB_DB = 'workflow'
