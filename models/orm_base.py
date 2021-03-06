from functools import wraps
from helper.date import Date
from helper.logging import mysql_log

import time


class BaseModel:
    def __init__(self):
        pass

    def has(self, **kwargs):
        """
        检查一个元素是否在数据库中 用法如下
        User.has(id=1)
        :param kwargs:
        :return:
        """
        return self.find_one(**kwargs) is not None

    def all(cls):
        # 按照 id 升序排序
        # name = cls.__name__
        # ds = mongua.db[name].find()
        # l = [cls._new_with_bson(d) for d in ds]
        # return l
        return cls._find()

    def _find(self, **kwargs):
        """
        db 数据查询
        """
        try:
            query = self.module.select()
            for k, v in kwargs.items():
                query = query.where(getattr(self.module, k) == v)
            l = [self._new_with_bson(d) for d in query]
            return l
        except AttributeError as exc:
            mysql_log.warn(exc)
            return []

    def find_by(self, **kwargs):
        return self.find_one(**kwargs)

    def find_all(self, **kwargs):
        """
        return all of params
        :param kwargs:
        :return:
        """
        return self._find(**kwargs)

    def find(self, **kwargs):
        """
        find id
        self.find_one(id=id)
        """
        return self.find_one(**kwargs)

    def get(self, **kwargs):
        """
        get id
        self.find_one(id=id)
        """
        return self.find_one(**kwargs)

    def find_one(self, **kwargs):
        """
        """
        # TODO 过滤掉被删除的元素
        # kwargs['deleted'] = False
        l = self._find(**kwargs)
        if len(l) > 0:
            return l[0]
        else:
            return None

    def _get_module_dict(self):
        """
        获取 module 的结构数据
        :return:
        """
        mdict = self.module.__dict__
        d = []
        for m in mdict:
            if not m.startswith('_') and m != 'DoesNotExist':
                d.append(m)
        return d

    def new(self, form=None, **kwargs):
        """
        new 是给外部使用的函数
        """
        # 创建一个空对象
        # m = self.module()
        # 把定义的数据写入空对象, 未定义的数据输出错误
        fields = self._get_module_dict().copy()
        if form is None:
            form = {}
        for f in fields:
            if f in form:
                setattr(self, f, form[f])
        # 处理额外的参数 kwargs
        for k, v in kwargs.items():
            if hasattr(self, k):
                setattr(self, k, v)
            else:
                raise KeyError
        now = Date().now().format()
        self.ct = now
        self.save_data()
        mysql_log.info('新增数据成功')
        return self

    def _new_with_bson(self, bson):
        """
        这是给内部 all 这种函数使用的函数;
        从数据库中恢复一个 model，可以理解为给这个类赋予属性值;
        调用self.__dict__可见赋予的属性
        """
        for m in self.module.__dict__:
            if not m.startswith('_') and m != 'DoesNotExist':
                setattr(self, m, getattr(bson, m))
        return self

    def save_data(self):
        """
        create new module
        实际是用来创建新的数据
        :return:
        """
        mdict = {m: getattr(self, m, '') for m in self._get_module_dict() if hasattr(self, m)}
        self.module.create(**mdict)
        # mongua.db[name].save(self.__dict__)

    def update_data(self):
        """
        save module
        实际是用来保存更新后的数据
        :return:
        """
        ujson = self.json()
        ct = Date.now().format()
        ujson.update({'ct': ct})
        self.module.update(**ujson).where(getattr(self.module, 'main_id') == ujson.get('main_id')).execute()
        mysql_log.info('更新数据成功')

    def delete(self, **kwargs):
        try:
            query = self.module.delete()
            for k, v in kwargs.items():
                query = query.where(getattr(self.module, k) == v)
            query.execute()
            mysql_log.info('删除数据成功')
        except AttributeError as exc:
            mysql_log.warn(exc)

    def json(self):
        _dict = self._get_module_dict()
        d = {k: getattr(self, k) for k in _dict}
        # TODO, 增加一个 type 属性
        return d

    def data_count(self, **kwargs):
        """
        神奇的函数, 查看数据的个数
        u.data_count(Comment)

        :return: int
        """
        return len(self.find_all(**kwargs))

    def __repr__(self):
        class_name = self.__class__.__name__
        properties = ('{0} = {1}'.format(k, v) for k, v in self.__dict__.items())
        return '<{0}: \n  {1}\n>'.format(class_name, '\n  '.join(properties))

    def test_func(cls):
        cls._new_with_bson('ll')


def close_connection(session):
    def decorate(func):
        @wraps(func)
        def wrapper():
            session.close()

        return wrapper

    return decorate


if __name__ == '__main__':
    b = BaseModel()
    print(b.__dict__)
