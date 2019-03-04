import os

base_dir = os.path.abspath('.')

static_path = os.path.join(base_dir, 'static')
template_path = os.path.join(base_dir, 'templates')

cookie_secret = 111111111111111

request_info = True
debug = True
login_url = '/user/login'

