'''
数据库跟踪模块
'''

from .pw_migrate import run
import os

current_path = os.path.dirname(__file__)

run(current_path + '/migrations')