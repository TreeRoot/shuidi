# -*- coding:utf-8 -*-
import copy
from bson import ObjectId

import flow
import flow_instance
from framework.data import flow_db


class data_provider:
    """
        流程数据配置， 增删改查
    """
    db = flow_db
    _process_steps = False

    def __init__(self):
        self.cache = {}

    def get(self, _id=None):
        if _id is None:
            return None

        obj = None
        obj = self.cache.get(_id, None)
        if obj:
            return obj

        obj = self._get_origin(_id)
        if not obj:
            # raise Exception('no data find for id:{}'.format(_id))
            return None

        if not isinstance(obj, base_provider):
            obj = self.construct(self)
            if self._process_links:
                self._process_link(self)

        if obj:
            self.cache.update({obj._id:obj})
        return obj

    def _get_origin(self):
        table = self.get_table()
        obj = table.find_one({'_id': ObjectId(_id)})
        return obj

    def get_table(self):
        return getattr(self.db, self._table_name)

    def get_with(self, query, sort=-1):
        if not isinstance(query, dict):
            raise Exception('query is not dict')

        table = self.get_table()
        # TODO
        # 分页参数， 排序后续实现, 默认_id排序
        obj = table.find(query).sort('_id', -1)

        # 递归实例化对象
        if not isinstance(obj, base_provider):
            obj = self.construct(obj)
            if self._process_steps:
                self._process(obj)

        self.cache.update({obj._id:obj})
        return obj

    def save(self, obj, cache=True):
        if not hasattr(obj, _id):
            # raise Exception('obj has no _id')
            obj._id = ObjectId()

        table = self.get_table()
        # load to json format
        obj_load = obj.load()
        table.replace_one({'_id': obj['_id']}, obj_load, upsert=True)

        # 同时更新
        if cache:
            self.cache.update({obj._id: obj})

    def construct(self, obj):
        raise Exception('baseclass has no construct method')

    def _process_link(self, cur):
        """
            处理给定节点（步骤）相关节点实例化问题，处理逻辑目前为：
            从cur往后找，找到后实例化，继续向后找， 直到没有，然后往前找，
            逻辑相反；
        """

        need_prev = []
        need_next = []

        def is_over(ccur):
            """
                判断节点是否有前后节点，有返回True， 默认False
            """
            res = False
            for n in getattr(ccur, self._prev):
                if n isinstance(n, (str, unicode, ObjectId)):
                    res = True
                    break
            for n in getattr(ccur, self._next):
                if n isinstance(n, (str, unicode, ObjectId)):
                    res = True
                    break
            return res

        def _process(ccur, forward=True):
            # forward 前后(true 前)
            np = getattr(ccur, self._next)
            tmp = need_next
            if not forward:
                np = getattr(ccur, self._prev)
                tmp = need_prev

            for i in range(len(np)):
                n = np[i]
                node = None
                # 跳过已经实例化的
                if not isinstance(n, (str, unicode, ObjectId)):
                    node = n
                else:
                    node = self.cache.get(n, Nonf)
                    if not node:
                        j = self._get_origin(str(n))
                        node = self.construct(j)

                if not node:
                    continue

                if is_over(node):
                    tmp.append(node)

            # 替换
            np[i] = node
            if is_over(ccur):
                # 当前节点加入并跳过
                tmp.append(ccur)

        _process(cur, True)
        _process(cur, False)

        for n in need_prev:
            self._process_link(n)
        for n in need_next:
            self._process_link(n)

class flow_provider(data_provider):
    _table_name = 'flow'

    def construct(self, obj):
        if not obj:
            return None

        obj['step'] = stepd.get(obj['step'])
        return flow.flow(**obj)

class step_provider(data_provider):
    # 实例化时实例化所有相关步骤
    _prev = 'prev_steps'
    _next = 'next_steps'
    _process_links = True
    _table_name = 'step'

    def construct(self, obj):
        if not obj:
            return None

        obj['flow'] = flowd.get(obj['flow'])
        obj['rule'] = flow.flow_rule(**obj['rule'])
        return flow.step(**obj)

class stepins_provider(data_provider):
    _table_name = 'stepins'

    def get_with(self, task_id=None, step_id=None):
        if not task_id or not step_id:
            raise Exception('task id or step id is None')

        query = {
                'task': ObjectId(task_id),
                'step': ObjectId(step_id),
            }

        res = super().get_with(query)
        return res

    def construct(self, obj):
        if not obj:
            return None

        obj['task'] = taskd.get(obj['task'])
        obj['step'] = stepd.get(obj['step'])
        obj['rule'] = flow.rule(**obj['rule'])

        res = flow_instance.stepins(**obj)
        return res

class task_provider(data_provider):
    _table_name = 'task'

    def save(self, obj):
        cobj = copy.deepcopy(obj)
        if isinstance(cobj.owner, dict):
            cobj.owner = cobj.owner['_id']

        super().save(cobj)
        state = obj.state
        while state:
            stated.save(state)
            state = state.next

    def construct(self, obj=None):
        if not obj:
            return None

        obj['flow'] = flowd.get(obj['flow'])
        obj['first'] = stated.get(obj['first'])

        state = obj['first']
        self.cache.update({state._id: state})

        # 初始化状态链, 由first单向构建, 并加入cache
        while state and state.next:
            if not isinstance(state.next, flow.state):
                ns = stated._get_origin(state.next)
                ns = stated.construct(ns)
                if ns:
                    self.cache.update({ns._id: ns})
                ns.prev = state
                state = ns

        obj['cur'] = stated.get(obj['cur'])
        obj['prev'] = stated.get(obj['prev'])
        obj['next'] = stated.get(obj['next'])

        res = flow_instance.task(**obj)
        return res

class state_provider(data_provider):
    _prev = 'prev'
    _next = 'next'
    _process_links = True
    _table_name = 'state'

    def construct(self, obj):
        """
            状态链初始化，暂时交由task初始化， 本身不提供初始化；
            后续可能更改
        """
        if not obj:
            return None

        obj['task'] = taskd.get(obj['task'])
        obj['step'] = stepinsd.get(obj['step'])
        obj['prev'] = stated.get(obj['prev'])
        obj['next'] = stated.get(obj['next'])

        res = flow_instance.state(**obj)
        return res

flowd = flow_provider()
stepd = step_provider()
stepinsd = stepins_provider()
taskd = task_provider()
stated = state_provider()

