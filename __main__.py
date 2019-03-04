# -*- coding:utf-8 -*-
import tornado
import tornado.ioloop

from framework.base.urls import url_config as urls
from framework.base.request_handler import base_handler
from settings import settings

class main_handler(base_handler):
    def get(self):
        import ipdb; ipdb.set_trace()
        self.write("test")

def main():
    _settings = {
            "debug": settings.debug,
            "static_path": settings.static_path,
            "template_path": settings.template_path,
            "login_url": settings.login_url,
            }

    urls.add(('/', main_handler))

    app = tornado.web.Application(urls.urls, **_settings)
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    print('server at 8888 port\n')
    main()
