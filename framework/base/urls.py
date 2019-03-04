# -*- coding:utf-8 -*-
from .request_handler import base_handler

class single_base:
    _instance = None

    def __new__(cls, *arg, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls, *arg, **kwargs)
        return cls._instance


class url_handler(single_base):
    """
        动态绑定
    """
    _uh = []
    def __init__(self, *arg, **args):
        pass

    def _check(self, uh):
        pass

    def add(self, uh=None):
        if not isinstance(uh, tuple):
            raise Exception("参数格式错误")

        # 处理器未实例化， 暂时不判断， TODO
        # if not isinstance(uh[0], str) or not isinstance(uh[1], base_handler):
        #     raise Exception("参数格式错误")

        self._uh.append(uh)

    @property
    def urls(self):
        return self._uh


url_config = url_handler()


if __name__ == "__main__":
    u1 = url_handler()
    u1.add(('/', 'handler'))
    u2 = url_handler()
    u2.add(('/api', 'handler'))
    print(u1, u1.urls)
    print(u2, u2.urls)
