import time
from models import Model


class Board(Model):
    def __init__(self, form):
        self.id = int(form.get('id', 0))
        self.title = form.get('title', '')
        self.ct = int(time.time())
        self.ut = self.ct
