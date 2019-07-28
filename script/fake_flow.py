# -*- coding:utf-8 -*-
import datetime
from bson import ObjectId
from pprint import pprint

from core.workflow.flow import flow, step


class fake_flow:
    def __init__(self, names):
        self.names = names
        self.flow = flow
        self.flowins = None
        self.step = step
        self.nodes = []
        self.stepins = []
        self.res = []

    def make_flow(self):
        self.flowins = flow(**{
                '_id': ObjectId(),
                'name': 'erpording',
                'step': None,
                'obj': None,
                'owner': None,
                'identity': None,
                'create_time': datetime.datetime.utcnow(),}
            )

    def make_steps(self, flow):
        for name in self.names:
            node = {
                    'name': name,
                    '_id': ObjectId(),
                    'prev_step': [],
                    'next_step': [],
                    'flow': flow._id,
                    'create_time': datetime.datetime.utcnow(),
                }
            self.nodes.append(node)

        self.make_stepins()

    def make_stepins(self):
        self.stepins = [step(**n) for n in self.nodes]
        self.link_steps()

    def link_steps(self):
        """
            简化版, 单线性
        """
        while self.stepins:
            last = self.stepins.pop()
            try:
                self.stepins[-1].add_next(last)
                self.res.append(last)
            except:
                self.res.append(last)

    def run(self):
        self.make_flow()
        self.make_steps(self.flowins)
        for ins in self.res:
            pprint(ins.__dict__)


if __name__ == "__main__":
    # 固定的，伪造数据，后续实现配置界面
    names = ('开单', '申料', '镀膜', '生产')
    f = fake_flow(names)
    f.run()


