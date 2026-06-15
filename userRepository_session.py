from flask import session
from utils import generate_id

class UserRepository:
    def __init__(self):
        pass

    def get_all(self):
        return session.get("users", [])

    def find(self, id):
        users = self.get_all()
        return next((u for u in users if u["id"] == id), None)

    def _save_all(self, users):
        session["users"] = users
        session.modified = True

    def update(self, id, data):
        users = self.get_all()
        for user in users:
            if user["id"] == id:
                user.update(data)
                self._save_all(users)
                break

    def add(self, user):
        users = self.get_all()
        user['id'] = generate_id(users)
        users.append(user)
        self._save_all(users)
        return user

    def delete(self, id):
        users = self.get_all()
        filtered_users = list(filter(lambda u: u["id"] != id, users))
        self._save_all(filtered_users)