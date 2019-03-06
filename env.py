# -*- coding:utf-8 -*-
import os
import sys
from functools import wraps

def find_modules(func):
    @wraps(func)
    def inner(*args, **kwargs):
        # 暂时运行时启动modules
        sys.path.insert(0, os.path.join(os.path.abspath(__file__), "modules"))

        return func(*args, **kwargs)

    return inner
