import time

from .items import MailNew, BaseModel


# mail module
class Mail(BaseModel):

    def __init__(self):
        super().__init__()
        self.module = MailNew

    # 用来建立空的类实例
    @staticmethod
    def get_instance(mail_id):
        record, created = MailNew.get_or_create(mail_id=mail_id)
        return record

    def set_sender(self, sender_id):
        self.sender_id = sender_id
        self.save_data()

    def mark_read(self):
        self.read = True
        self.save_data()
