# -*- coding:utf-8 -*-
import datetime
from bson import ObjectId

from .flow_instance import task, stepins
from .flow_dataprovider import flowd, stepinsd


def start_task(flow=None, name=None, user=None, extra=None, begin=True, **kwargs):
    flow_ins = flowd.get(flow)
    if not flow_ins:
        raise Exception('flow is none or invalid formate')

    if not name:
        raise Exception('name is none')

    if not user:
        raise Exception('user is none')

    task_ins = task(
                _id = ObjectId(),
                name = name,
                flow = flow_ins._id,
                create_time = datetime.datetime.utcnow(),
                extra = extra,
            )

    task_ins = task.save()
    # 创建stepins
    all_steps = get_flow_steps(flow)
    for step in all_steps:
        stepins_ins = stepins(
                    '_id': ObjectId(),
                    'task': task_ins,
                    'step': step,
                    'create_time': datetime.datetime.utcnow(),
                )
        stepins_ins.save()

    if begin:
        task.begin()

    return task

def move_task(*args, **kwargs):
    pass

def get_flow_steps(flow):
    flow_ins = flowd.get(flow)
    if not flow_ins:
        raise Exception('flow is none or invalid')

    def get_steps(steps, all_steps):
        """
            单线性
        """
        for step in steps:
            if step not in all_steps:
                all_steps.append(step)
                get_steps(step.next_steps, all_steps)

    all_steps = []
    step = flow.step
    all_steps.append(step)

    next_steps = step.next_step
    get_steps(next_steps, all_steps)

    return all_steps
