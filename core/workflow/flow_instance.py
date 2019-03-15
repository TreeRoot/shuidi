# -*- coding:utf-8 -*-
import datetime
from bson import ObjectId

import fdata_provider as fdp
from flow import base_provider


class task(base_provider):
    def __init__(self, _id=None, name=None, flow=None, create_time=None, end_time=None, cur=None, prev=None, next=None,
            extra=None, user=None, cur_step=None):
        """
            任务， 流程实际执行对象
            arguments:
                _id : 标识符
                _begin: 任务是否开始（后续实现其他功能，暂时没用上）
                user: 任务创建者
                done: 任务完成与否， 整个流程的结束， 通常无法对已完成的任务进行任何操作
                name: 任务名称
                flow: 任务所属流程
                create_time: 任务创建时间
                end_time: 任务结束时间
                cur_step: 任务当前步骤
                cur: 任务当前状态
                first: 任务第一个状态
                prev: 任务上一个状态(如果有)
                next: 任务下一个状态(如果有)
        """

        self._begin = False
        self.done = False
        self._user = user

        self._id = _id
        self.name = name
        self.flow = flow
        self.create_time = create_time
        self.end_time = end_time
        self.extra = extra
        self.cur_step = cur_step
        self.cur = cur
        self.first = first
        self.prev = prev
        self.next = next

    def begin(self, user):
        if not self._begin:
            self._begin = True

        # 创建任务自动创建任务所属流程关联的步骤的步骤实例
        stepins = fdp.stepins.get_with({'task':self._id, 'step':slef.step})

        # 任务开始，就会生成状态，任务的每次改变都会生成一个状态
        news = state(**{
                '_id': ObjectId(),
                'task': self,
                'step': stepins,
                'done': False,
                'prev': None,
                'next': None,
                'confirm_user': user._id,
                'start_time': datetime.datetime.utcnow(),
            })

        self.state = news
        self.first = news

    def move(self, stepins):
        """
            将任务从当前步骤移动到下个合法步骤，暂不支持回退
        """
        if not self._begin:
            # raise Exception("task is unstart!")
            self._begin = True

        # 第一版只考虑最简单的单一情况
        # 查找next_step, 暂时进行中的任务不支持后退

    def _is_next_step(self, stepins):
        cur = self.cur.step.step
        ns = stepins.step
        def valid_step(cur, ns):
            if not cur or not ns:
                return False

            nsteps = cur.next_steps
            while len(nsteps) != 0:


class state:
    """
        任务的状态
        arguments:
            _id: 标识符
            task: 状态所属任务
            step: 状态所属步骤实例
            done: 状态是否完成
            confirm_user: 进入此状态的用户
            start_time: 进入此状态的时间
            freeze: 状态完成，自动冻结
    """
    def __init__(self, _id=None, task=None, step=None, done=None, prev=None, next=None, confirm_user=None, freeze=None):
        self._id = _id
        self.task = task
        self.step = step
        self.done = done
        self.prev = prev
        self.next = next
        self.confirm_user = confirm_user
        self.freeze = freeze

class stepins(base_provider):
    """
        流程步骤实例， 流程流转具体执行对象；
        arguments:
            _id: 标识符
            task: 步骤实例所属任务（确保步骤实例是唯一的，每个任务的步骤实例是惟一的， 方便后续其他实现及配置）
            step: 步骤实例关联的步骤
            rule: 默认继承源步骤的rule， 可在进行配置
            create_time: 步骤实例创建时间
    """
    def __init__(self, _id=None, task=None, step=None, prev_step=None, next_step=None, create_time=None, rule=None):
        self._id = _id
        self.task = task
        self.step = step
        self.rule = rule
        self.create_time = create_time
