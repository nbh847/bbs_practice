from functools import wraps


class BaseModel(object):
    def __init__(self):
        print('class name', self.__name__)

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
        for k, v in kwargs:
            key, value = locals()[k], v
            break
        if key == '':
            return None
        ds = cls.select().where(cls.k )
        # if sort is not None:
        #     ds = ds.sort(sort)
        l = [cls._new_with_bson(d) for d in ds]
        return l

    @classmethod
    def find_one(cls, **kwargs):
        """
        """
        # TODO 过滤掉被删除的元素
        # kwargs['deleted'] = False
        l = cls._find(**kwargs)
        # print('find one debug', kwargs, l)
        if len(l) > 0:
            return l[0]
        else:
            return None

    def save(self):
        session = self.get_dbsession()


Base = declarative_base()


def TableCreator(tablename, **kwargs):
    def len_str(str):
        str_list = {
            'String': 200,
        }
        return

    class MyTable(Base):
        __tablename__ = tablename
        for k, v in kwargs.items():
            if k == 'id':
                id = Column(locals()[v], primary_key=True)
            else:
                k = Column(locals()[v](len_str(v)))

    return MyTable


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
