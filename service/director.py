from dao.director import DirectorDAO


class DirectorService:
    def __init__(self, dao: DirectorDAO):
        self.dao = dao

    def get_one(self, did):
        return self.dao.get_one(did)

    def get_all(self):
        return self.dao.get_all()

    def create(self, director_d):
        return self.dao.create(director_d)

    def update(self, did, director_d):
        """
        Сервис обновления данных режиссера
        :param did: ИД режиссера
        :param director_d: данные для обновления
        :return: dao
        """
        director = self.get_one(did)
        director.name = director_d.get("name")
        self.dao.update(director_d)
        return self.dao

    def delete(self, did):
        self.dao.delete(did)
