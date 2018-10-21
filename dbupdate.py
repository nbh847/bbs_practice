'''
数据库跟踪模块
'''

from models.pw_migrate import run
import os

current_path = os.path.dirname(__file__)
print(current_path)
run(current_path + '/models/migrations')