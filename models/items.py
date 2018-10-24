# 主要是负责model模块
# -*- coding: utf-8 -*-

# Define here the models for your scraped items


import peewee as pw
from config import *
from .orm_base import BaseModel

db = pw.MySQLDatabase(MYSQL_DB_NAME,
                      host=MYSQL_HOST,
                      port=MYSQL_PORT,
                      user=MYSQL_USER,
                      passwd=MYSQL_PASSWORD,
                      charset=MYSQL_CHARSET)


# mail module
class MailNew(pw.Model):
    main_id = pw.IntegerField(verbose_name="main id", primary_key=True, default=0)
    content = pw.CharField(verbose_name='mail content', max_length=800, default='')
    title = pw.CharField(verbose_name='mail title', max_length=200, default='')
    read = pw.BooleanField(verbose_name='mail title', default=False)
    sender_id = pw.IntegerField(verbose_name="mail sender id", default=0)
    receiver_id = pw.IntegerField(verbose_name="mail receiver id", default=0)
    ct = pw.DateTimeField(verbose_name="mail create time", default='1970-01-01')

    class Meta:
        database = db
        db_table = 'mail'


class UserNew(pw.Model):
    main_id = pw.IntegerField(verbose_name="main id", primary_key=True, default=0)
    username = pw.CharField(verbose_name='username', max_length=300, null=False, default='')
    password = pw.CharField(verbose_name='password', max_length=500, null=False, default='')
    role = pw.IntegerField(verbose_name="mail sender id", default=11)
    ct = pw.DateTimeField(verbose_name="mail create time", default='1970-01-01')

    class Meta:
        database = db
        db_table = 'user'
