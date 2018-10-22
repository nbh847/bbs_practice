from functools import wraps


class BaseModel:
    def __init__(self):
        print('print new module')

    @classmethod
    def has(cls, **kwargs):
        """
        检查一个元素是否在数据库中 用法如下
        User.has(id=1)
        :param kwargs:
        :return:
        """
        return cls.find_one(**kwargs) is not None

    @classmethod
    def _find(cls, **kwargs):
        """
        db 数据查询
        """
        name = cls.__name__
        # TODO 过滤掉被删除的元素
        # kwargs['deleted'] = False
        # flag_sort = '__sort'
        # sort = kwargs.pop(flag_sort, None)
        key, value = '', ''
        for k, v in kwargs.items():
            key, value = k, v
            break
        if key == '':
            return None
        ds = cls.select().where(getattr(cls, key) == value).get()
        print(ds.id)
        # print('ds', ds)
        # l = [cls._new_with_bson(d) for d in ds]
        # return l

    @classmethod
    def find_one(cls, **kwargs):
        """
        """
        # TODO 过滤掉被删除的元素
        # kwargs['deleted'] = False
        l = cls._find(**kwargs)
        # print('find one debug', kwargs, l)
        # if len(l) > 0:
        #     return l[0]
        # else:
        #     return None

    @classmethod
    def _new_with_bson(cls, bson):
        """
        这是给内部 all 这种函数使用的函数
        从数据库中恢复一个 model，可以理解为给这个类赋予属性值
        """
        m = cls()
        if k in bson:
            setattr(m, k, bson[k])
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

    def update_data(self, **field_dict):
        print('self id', self.mail_id)
        self.update(**field_dict).where(getattr(self, 'mail_id') == self.mail_id).execute()


    @classmethod
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
