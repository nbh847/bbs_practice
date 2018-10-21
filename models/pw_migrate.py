'''
数据库跟踪模块
'''

from . import items
from peewee_migrate import Router


def run(path):
    items.db.connect()

    # migrate_table: 迁移表的名称
    router = Router(items.db, ignore="basemodel", migrate_dir=path, migrate_table='bbsmigrate')
    router.create(auto=items)
    router.run()

    items.db.close()