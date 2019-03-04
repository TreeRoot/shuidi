# -*- coding:utf-8 -*-
import os
import json
import inspect
from tornado.web import RequestHandler

from settings import settings

class base_handler(RequestHandler):
    def prepare(self):
        if settings.request_info:
            print("{}  {}:{}".format(self.request.uri, self.request.method, self.request.remote_ip))

    def json(self, obj, content_type="text/javasctipt; charset=utf-8", cls=None):
        self.set_header("Content-Type", content_type)
        self.write(json.dumps(obj, cls=cls).replace("</", "<\\/"))

    def template(self, name=None, *args, **kwargs):
        """
            优先name指定的模板名称，默认以当前class的类名的小写；
            class User:
                pass

            模板名称: user.html, 路径首先在模块下对应的templates ，然后再平台的templates，
            类似于flask蓝图划分
        """
        if name:
            path = self._get_template_path + '/' + name + '.html'
            if not os.path.exists(path):
                pass
        
    def _get_template_name(self, name=None):
        if not name:
            # name = self.__class__.__name__.split('.')[0]
            name = self.__class__.__name__
        return name

    def _get_template_path(self):
        pass

    def get_current_user(self):
        pass

    def get_args(self, *args, **kwargs):
        pass
