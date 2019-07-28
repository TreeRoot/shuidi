# -*- coding:utf-8 -*-
import datetime
from bson import ObjectId

import flow_dataprovider as fdp
from flow import base_provider


class task(base_provider):
    def __init__(self, _id=None, name=None, flow=None, create_time=None, end_time=None, cur=None, prev=None, next=None,
            extra=None, user=None, cur_step=None, freeze=False):
        """
            任务， 流程实际执行对象
            arguments:
                _id : 标识符
                _begin: 任务是否开始（后续实现其他功能，暂时没用上）
                owner: 任务创建者
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
                freeze: 整个任务结束True
        """

        self._begin = False
        self.done = False
        self.end_time = end_time
        self.owner = owner

        self._id = _id
        self.name = name
        self.flow = flow
        self.create_time = create_time
        self.extra = extra
        self.cur_step = cur_step
        self.cur = cur
        self.first = first
        self.prev = prev
        self.next = next
        self.freeze = freeze

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

        self.cur = news
        self.first = news

    def move(self, stepins=None, user=None):
        """
            将任务从当前步骤移动到下个合法步骤，暂不支持回退
            暂时只考虑简单情况，单线性移动到下一个合法步骤，
            不会查询状态链，后续实现
        """
        if not self._begin:
            # raise Exception("task is unstart!")
            self._begin = True

        if not user:
            raise Exception('user is none')

        # 如果任务已处于最有一个步骤， 直接将状态设置为done， 结束
        cur_step = stepins.step
        if cur_step.next_step == []:
            self.cur.done(user)
            self.end_time = datetime.datetime.utcnow()
            self.freeze = True

        else:
            if not self._is_next_step(stepins):
                raise Exception('next_step not in valid next steps')

            # 任务当前状态设置done， 表示完成
            self.cur.done(user)
            self._move(stepins, user)

        fdp.taskd.save(self)
        return self

    def _move(self, stepins, user):
        """
            创建新的状态, 更改当前状态信息
        """
        prev = self.cur
        news = state(**{
                '_id': ObjectId(),
                'task': self,
                'step': stepins,
                'done': False,
                'prev': prev,
                'next': None,
                'confirm_user': user._id,
                'start_time': datetime.datetime.utcnow(),
            })

        self.cur = news
        self.prev = prev

    def _is_next_step(self, stepins):
        nsteps = slef.cur.step.step.next_steps
        ns = stepins.step

        def valid_step(ns, nsteps):
            if len(nsteps) == []:
                return False

            if ns not in nsteps:
                for n in nsteps:
                    valid_step(ns, n.step.next_steps)
            else:
                return True

        return valid_step(ns, nsteps)

    def is_done(self):
        """
            检查整个任务是否完成， 检查整个状态链是否done
        """
        state = self.first
        done = True
        while state:
            if state.done:
                state = state.next
            else:
                done = False
                break

        return True

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
        self.freeze = freeze
        self.confirm_user = confirm_user

    def done(self, user):
        """
            暂时简单的返回True，后续实现其他条件判断
        """
        self.done = True
        self.confirm_user = user._id

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
