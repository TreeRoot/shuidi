# -*- coding:utf-8 -*-
import datetime
from bson import ObjectId

from core.workflow.flow import flow, step


# 固定的，伪造数据，后续实现配置界面
names = ('开单', '申料', '镀膜', '生产')

class fake_flow:
    def __init__(self, names):
        self.names = names
        self.flow = flow
        self.step = step
        self.nodes = []

    def make_flow(self):
        ins = flow(
                '_id': ObjectId(),
                'name': 'erpording',
                'step': None,
                'obj': None,
                'owner': None,
                'identity': None,
                'create_time': datetime.datetime.utcnow(),
            )

    def make_steps(self, flow):
        for name in self.names:
            node = {
                    'name': name,
                    '_id': ObjectId(),
                    'prev_step': None,
                    'next_step': None,
                    'flow': flow._id,
                    'create_time': datetime.datetime.utcnow(),
                }
            self.nodes.append(node)



