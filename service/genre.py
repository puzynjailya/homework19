from dao.genre import GenreDAO


class GenreService:
    def __init__(self, dao: GenreDAO):
        self.dao = dao

    def get_one(self, bid):
        return self.dao.get_one(bid)

    def get_all(self):
        return self.dao.get_all()

    def create(self, genre_d):
        return self.dao.create(genre_d)

    def update(self, gid, genre_data):
        """
        Сервис обновления данных жанров
        :param gid: id обновляемой записи
        :param genre_data: обновляемые данные
        :return: ничего. Выполнят метод Data Access Object по обновлению данных
        """
        genre = self.dao.get_one(gid)
        genre.name = genre_data.get('name')

        self.dao.update(genre)

        return self.dao

    def delete(self, rid):
        """
        Сервис удаления данных
        :param rid: id удаляемой записи
        :return: ничего
        """
        self.dao.delete(rid)
