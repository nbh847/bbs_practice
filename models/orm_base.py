from functools import wraps
from helper.date import Date
from helper.logging import mysql_log


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
        return cls.find_one(**kwargs) is not None

    def _find(self, **kwargs):
        """
        db 数据查询
        """
        query = self.module.select()
        for k, v in kwargs.items():
            query = query.where(getattr(self.module, k) == v)
        # for q in query:
        #     print(q.__dict__)
        # for item in self.module.__dict__:
        #     if item.startswith('_'):
        #         print('_ : {}'.format(item))
        #     else:
        #         print(item)
        # print(self.module.__name__)
        # l = [self._new_with_bson(d) for d in query]
        # return l

    def find_one(self, **kwargs):
        """
        """
        # TODO 过滤掉被删除的元素
        # kwargs['deleted'] = False
        l = self._find(**kwargs)
        # print('find one debug', kwargs, l)
        # if len(l) > 0:
        #     return l[0]
        # else:
        #     return None

    def _new_with_bson(self, bson):
        """
        这是给内部 all 这种函数使用的函数
        从数据库中恢复一个 model，可以理解为给这个类赋予属性值
        """
        for d in self.__dict__:
            if fields in bson:
                setattr(self, k, bson[k])
            else:
                # 设置默认值
                setattr(m, k, v)
        setattr(m, '_id', bson['_id'])
        # 这一句必不可少，否则 bson 生成一个新的_id
        # FIXME, 因为现在的数据库里面未必有 type
        # 所以在这里强行加上
        # 以后洗掉db的数据后应该删掉这一句
        m.type = cls.__name__.lower()
        return m

    def update_data(self, key_id, **field_dict):
        ct = Date.now().format()
        field_dict.update({'ct': ct})
        self.module.update(**field_dict).where(getattr(self.module, 'mail_id') == key_id).execute()

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
