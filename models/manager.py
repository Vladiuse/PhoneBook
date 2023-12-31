from .queryset import QuerySet
from .db import DataBase
from exceptions import ObjectDoesNotExist

class Manager:
    """Клас менеджера - отчечает за взаимодейстиве с БД"""
    db = DataBase()

    def __init__(self):
        self.objects = None
        self.model = None

    def __len__(self):
        return len(self.objects)

    def _clean_data(self):
        """
        обнулить данные менеджера
        :return:
        """
        if self.objects is None:
            self.objects = dict()
        self.objects.clear()

    def get_objects_from_db(self):
        """
        Загрузить обьекты из БД
        """
        self._clean_data()
        if self.db.table:
            for row in self.db.get_rows():
                phone = self.model.parse(row)
                self.objects[phone.pk] = phone


    def update_db(self):
        """
        Обновить базу данных - перезаписывает в нее те обекты которые храняться в self.objects
        """
        self.db.write(self._objects_to_string())

    def _objects_to_string(self) -> str: #TODO перенести в клас DataBase
        """
        Акрквести обьекты в текст для записи в БД
        :return: строку
        """
        return ''.join(model.render() for model in self.get_objects_list())

    def save(self, model):
        """Сохоанить модель в БД
        если нет первичного ключа - созраниться как новая запись,
        если есть - обновит существующую
        """
        if self.objects is None:
            self.get_objects_from_db()

        if not model.pk:
            model.pk = self.db.get_new_pk()
            self.add_object(model)
        else:
            self.update_object(model)
        self.update_db()

    def delete(self, pk:int):
        """
        Удаление записи из БД
        :param pk: int
        """
        self.objects.pop(pk)
        self.update_db()

    def add_object(self, obj):
        """
        Добавить обьект в массив выгруженых с БД обьектов
        :param obj: класс Model
        """
        self.objects[obj.pk] = obj

    def update_object(self, obj):
        """
        Обновить обьект
        :param obj:  класс Model
        """
        if obj.pk not in self.objects:
            raise ValueError('Ошибка обновления, нет такого айди')
        self.objects[obj.pk] = obj

    def get_objects_list(self) -> list:
        """
        Получить список с обьектами
        """
        if self.objects is None:
            self.get_objects_from_db()
        return [model for pk, model in self.objects.items()]

    def get(self,*,pk:int):
        """
        Получить один обьект из БД
        Если не найден - вывоветься ошибка
        :return:
        """
        self.get_objects_from_db()
        try:
            return self.objects[pk]
        except KeyError:
            raise ObjectDoesNotExist


    # def get_queryset(self):
    #     pass

    def all(self):
        """
        Получить QuerySet со всеми обьектами созраненими в БД
        :return: QuerySet
        """
        self.get_objects_from_db()
        qs = QuerySet(self.model, self.get_objects_list())
        return qs

    def filter__full(self, **kwargs): #TODO DRY
        """
        Фильтрация элементов по нескольком полям
        Необходимо точное сответвие
        Регистр не учитываеться
        :return: QuerySet
        """
        models = []
        for model in self.get_objects_list():
            model_value = model.values
            match = [model_value[filter_key].lower() == filter_val for filter_key, filter_val in kwargs.items()]
            if all(match):
                models.append(model)
        qs = QuerySet(self.model, models)
        return qs

    def filter__startswith(self, **kwargs): #TODO DRY
        """
        Фильтрация элементов по нескольком полям
        Выберутся те модели, у которых хотя бы одно поле начинаеться с переданного значения
        Регистр не учитываеться
        :return: QuerySet
        """
        models = []
        for model in self.get_objects_list():
            model_value = model.values
            match = [model_value[filter_key].lower().startswith(filter_val) for filter_key, filter_val in kwargs.items()]
            if any(match):
                models.append(model)
        qs = QuerySet(self.model, models)
        return qs

    def filter__in(self, **kwargs): #TODO DRY
        """
        Фильтрация элементов по нескольком полям
        Выберутся те модели, у которых хотя бы одно содержит переданную подстроку
        Регистр не учитываеться
        :return: QuerySet
        """
        models = []
        for model in self.get_objects_list():
            model_value = model.values
            match = [filter_val in model_value[filter_key].lower() for filter_key, filter_val in kwargs.items()]
            if any(match):
                models.append(model)
        qs = QuerySet(self.model, models)
        return qs

    def count(self)->int:
        """
        Подсчет кол-ва записей в БД
        """
        if self.objects is None:
            self.get_objects_from_db()
        return self.db.count()


