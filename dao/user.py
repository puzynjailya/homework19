from dao.model.user import User


class UserDAO:
    def __init__(self, session):
        self.session = session

    def get_one_user(self, username):
        return self.session.query(User).filter(User.username == username).first()

    def create(self, user_data):
        # Добавляем нового пользователя в БД
        entity = User(**user_data)
        self.session.add(entity)
        self.session.commit()
        return entity