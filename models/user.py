from .items import BaseModel, UserNew


# class User(Model):
#     """
#     User 是一个保存用户数据的 model
#     现在只有两个属性 username 和 password
#     """
#
#     def __init__(self, form):
#         self.id = form.get('id', None)
#         self.username = form.get('username', '')
#         self.password = form.get('password', '')
#         self.role = int(form.get('role_id', 11))
#
#     def salted_password(self, password, salt='$!@><?>HUI&DWQa`'):
#         import hashlib
#         def sha256(ascii_str):
#             return hashlib.sha256(ascii_str.encode('ascii')).hexdigest()
#
#         hash1 = sha256(password)
#         hash2 = sha256(hash1 + salt)
#         return hash2
#
#     def hashed_password(self, pwd):
#         import hashlib
#         # 用 ascii 编码转换成 bytes 对象
#         p = pwd.encode('ascii')
#         s = hashlib.sha256(p)
#         # 返回摘要字符串
#         return s.hexdigest()
#
#     @classmethod
#     def register(cls, form):
#         name = form.get('username', '')
#         pwd = form.get('password', '')
#         if len(name) > 2 and User.find_by(username=name) is None:
#             u = User.new(form)
#             u.password = u.salted_password(pwd)
#             u.save()
#             return u
#         else:
#             return None
#
#     @classmethod
#     def validate_login(cls, form):
#         u = User(form)
#         user = User.find_by(username=u.username)
#         if user is not None and user.password == u.salted_password(u.password):
#             return user
#         else:
#             return None


class User(BaseModel):
    def __init__(self):
        super().__init__()
        self.module = UserNew

    def salted_password(self, password, salt='@345%$#(#&$%sdfegikQ@@K'):
        import hashlib
        def sha256(ascii_str):
            return hashlib.sha256(ascii_str.encode('ascii')).hexdigest()

        hash1 = sha256(password)
        hash2 = sha256(hash1 + salt)
        return hash2

    def hashed_password(self, pwd):
        import hashlib
        # 用 ascii 编码转换成 bytes 对象
        p = pwd.encode('ascii')
        s = hashlib.sha256(p)
        # 返回摘要字符串
        return s.hexdigest()

    def register(self, form):
        name = form.get('username', '')
        pwd = form.get('password', '')
        if len(name) > 2 and self.find_by(username=name) is None:
            u = self.new(form)
            u.password = u.salted_password(pwd)
            u.update_data()
            return u
        else:
            return None

    def validate_login(self, form):
        mdict = {f:form.get(f) for f in form}
        print('validate login form get', mdict)
        user = self.find_by(**mdict)
        if user is not None and form.get('password') == user.password:
            return user
        else:
            return None