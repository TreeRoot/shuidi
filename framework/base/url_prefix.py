# -*- coding:utf-8 -*-
from functools import wraps


class url_perfix:
    """
        仿flask blueprint
        暂时自定义类型， 区分api接口
    """
    url_type = {
            "normal": "normal",
            "api": "api"
        }

    def make_url(self, prefix=None, _type=None):
        if prefix is None or isinstance(prefix, str):
            raise Exception("路径不能为空或格式不正确！")
        if _type is None:
            _type = "normail"

        if _type == "normal":
            self._url = prefix
        else:
            self._url = 'api'+ '/' + prefix

    def perfix(self, func):
        @wraps(func):
        def inner(*args, **kwargs):
            self.make_url()
        return inner

