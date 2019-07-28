# -*- coding:utf-8 -*-
import datetime
from bson import ObjectId


class base_provider:
    """
        流程基类 ，提供基础通用方法，字典对象转换
    """

    # 判断保存数据库是不向下递归json化, 默认不向下
    _load_ = True

    def __eq__(self, other):
        if not hasattr(self, _id) or not hasattr(self, _id):
            return False
        if self._id == other._id:
            return True
        return False

    def load(self):
        res = {}
        name = '_' + type(self).__name__ + '__'
        for key in filter(lambda k: not k.startswith(tname), self.__dict__):
            prop = getattr(self, key)
            if callable(prop):
                continue

            if isinstance(prop, base_provider):
                # 保存数据时只保存当前相关实例_id
                if hasattr(prop, _id) and self._load_:
                    prop = prop._id
                else:
                    prop = prop.store()
            res.update({key: prop})

        return res

class flow(base_provider):
    """
        流程抽象类，模板， 暂时手动创建定义好的流程；
        arguments:
            _id: 标识符
            name: 流程名
            step: 流程第一个步骤id（只读）
            obj: 流程默认关联对象（后续实现）
            create_time: 流程创建时间
            owner: 流程创建者
            identity: 流程其他标识（后续实现）
    """
    def __init__(self, _id=None, name=None, step=None, obj=None, create_time=None, owner=None, identity=None):
        self._id = _id
        self.name = name
        self.step = step
        self.obj = obj
        self.owner = owner
        self.identity = identity
        self.create_time = create_time

class step(base_provider):
    """
        流程步骤， 流程具体每一步的操作对象；
        arguments:
            _id: 标识符
            name: 步骤名
            prev_step: 上一些步骤 []
            next_step: 下一些步骤 []
            create_time: 创建时间
            flow: 步骤所属流程
            rule: 该步骤的配置规则
                {
                    users:[],
                    fusers:[],
                    roles:[],
                    froles:[],
                }
    """
    def __init__(self, _id=None, name=None, prev_step=None, next_step=None, create_time=None, flow=None, rule=None, identity=None):
        self_id = _id
        self.name = name
        self.prev_step = prev_step
        self.next_step = next_step
        self.flow = flow
        self.rule = rule
        self.identity = identity
        self.create_time = create_time

    def load(self):
        self.prev_steps = [ObjectId(step._id) for step in self.prev_steps]
        self.next_steps = [ObjectId(step._id) for step in self.next_steps]
        self.rule = {
                'users': self.rule.users,
                'fusers': self.rule.fusers,
                'roles': self.rule.roles,
                'froles': self.rule.froles,

                }
        return super().load()

    def add_next(self, n):
        self.next_step.append(n)
        n.add_prev(self)

    def add_prev(self, p):
        self.prev_step.append(p)

class flow_rule(base_provider):
    """
        流程规则类，相关规则的转换, 非实体；
        arguments:
            users: 该步骤或步骤实例配置的执行人员 []
            fusers: 黑名单同上[]
            roles: 角色白名单[]
            froles: 角色黑名单 []
    """
    def __init__(self, users=None, fusers=None, roles=None, froles=None):
        self.users = users
        self.fusers = fusers
        self.roles = roles
        self.froles = froles

