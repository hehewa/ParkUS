from db import get_db

class User():
    def __init__(self, user_id):
        self.id = user_id
        try:
            c = get_db().execute('select * from User where ID_User = ?', [int(user_id)])
            row = c.fetchone()
            self.authenticated = row is not None
            self.info = row
            if self.info is not None:
                self.admin = self.info['Statut'] == 1
        except:
            self.authenticated = False
