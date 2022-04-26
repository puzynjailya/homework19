from dao.model.genre import Genre


class GenreDAO:
    def __init__(self, session):
        self.session = session

    def get_one(self, gid):
        return self.session.query(Genre).get(gid)

    def get_all(self):
        return self.session.query(Genre).all()

    def create(self, genre_d):
        ent = Genre(**genre_d)
        self.session.add(ent)
        self.session.commit()
        return ent

    def delete(self, gid):
        """
        DAO удаления данных из БД по ИД
        :param gid:  id жанра
        :return: ничего
        """
        # Получаем запись
        genre = self.get_one(gid)

        # Удаляем запись
        self.session.delete(genre)
        self.session.commit()

    def update(self, genre_data):
        """
        DAO добавления данных в БД
        :param genre_data: 
        :return: 
        """
        # Добавляем данные genre_data
        self.session.add(genre_data)
        self.session.commit()
