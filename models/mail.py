import time
from sqlalchemy import Column, String
from models import Model
from .orm_base import BaseModel


class Mail(Model):
    def __init__(self, form):
        self.id = None
        self.content = form.get('content', '')
        self.title = form.get('title', '')

        self.ct = int(time.time())
        self.read = False

        self.sender_id = -1
        self.receiver_id = int(form.get('to', -1))

    def set_sender(self, sender_id):
        self.sender_id = sender_id
        self.save()

    def mark_read(self):
        self.read = True
        self.save()


class MailNew(BaseModel):
    __tablename__ = 'mail'
    # 表的结构:
    id = Column(String(20), primary_key=True)
    name = Column(String(20))
    title = Column(String(100))
