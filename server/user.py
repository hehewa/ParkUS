from flask_login import UserMixin
from utils import query_db

class User(UserMixin):
    def __init__(self, user_id):
        super(User,self).__init__()
        self.id = user_id
        # magic creds en attendant une db
        self.admin = user_id == "123"
        self.info = query_db('select * from User where ID_User = ?',
            [int(user_id)], one=True)
        self.authenticated = self.info is not None

    @property
    def is_authenticated(self):
        return self.authenticated
