from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, user_id):
        super(User,self).__init__()
        self.id = user_id
        # magic creds en attendant une db
        self.admin = user_id == "123"
