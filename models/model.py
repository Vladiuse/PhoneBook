from .manager import Manager
from models.fields import Field
from .db import DataBase

class Model:
    """
    Базовый класс можели
    Описывает поля таблицы в БД
    """
    objects = Manager()

    def __init__(self,pk=None):
        self.pk = pk
        self._errors_messages = {}
        self._set_class()
        self._field_names_setted = False

    @classmethod
    def _set_class(cls):
        """
        Получить класс модели
        """
        cls.objects.model = cls


    def _set_fields_name(self):
        """
        Установить полям название, как названы переменные в модели
        :return:
        """
        for field_name, field in self.fields.items():
            field.name = field_name

    def is_valid(self):
        """
        Проверка модели на валидность
        """
        if not hasattr(self, '_is_valid'):
            self._check_fields()
            self._collect_fields_errors()
            return self._is_valid
        return self._is_valid

    def _check_fields(self):
        """
        Запуск валидаторов полей модели
        """
        setattr(self, '_is_valid', True)
        for field in self.fields_list:
            field.validate()
            if field.is_error:
                self._is_valid = False

    @property
    def errors(self) -> dict:
        """
        Список с ошибками полей
        """
        if not hasattr(self, '_is_valid'):
            raise AttributeError
        return self._errors_messages

    def _collect_fields_errors(self):
        """
        Собрать ошибки с полей
        """
        for field in self.fields_list:
            if field.is_error:
                self._errors_messages[field.name] = field.errors_messages

    def _render_pk(self, max_size=None):
        """
        перевести в строку первичный ключ для записи в БД,
        будут доставлены пробелы до значения max_length поля
        """
        if not max_size:
            max_size = DataBase.pk_max_size
        return f'{self.pk: <{max_size}}'

    def render(self):
        """
        перевести в строку значение поля,
        будут доставлены пробелы до значения max_length поля
        """
        fields_val = [field.render() for field in self.fields_list]
        fields_val.insert(0, self._render_pk())
        return DataBase.SEP_CHAR.join(fields_val) + DataBase.NEW_LINE_CHAR

    @classmethod
    def parse(cls, line:str):
        """
        Спарсить со строки значени полей и получить экземпляр класса
        """
        pk, *attrs = line.split(DataBase.SEP_CHAR)
        return cls(*attrs,pk=int(pk))



    def save(self):
        """
        Сохранить модель
        перед этим нужно вызвать is_valid
        """
        if not hasattr(self, '_is_valid'):
            raise AttributeError
        if self.is_valid():
            self._save()
        else:
            raise ValueError('Модель не проверена')

    def delete(self):
        """
        Удаление модели
        """
        self.objects.delete(self.pk)

    def _save(self):
        """
        Созранение - вызываеться save Manager
        """
        self.objects.save(self)



    @property
    def fields(self) ->dict:
        """
        получить словарь с названиями полей: полями
        :return:
        """
        fields = {field_name: field for field_name, field in self.__dict__.items() if isinstance(field, Field)}
        if not self._field_names_setted:
            for field_name, field in fields.items():
                field.name = field_name

        return fields

    @property
    def fields_list(self) ->list:
        """
        Поля в виде списка
        """
        return [field for field_name, field in self.fields.items()]

    @property
    def values_list(self) ->list:
        """
        Список о значениями полей
        :return:
        """
        return [field.get_value() for field in self.fields_list]
    @property
    def values(self) ->dict:
        """
        Словарь с названиями полей и их значениями
        """
        return {field_name: field.get_value() for field_name, field in self.fields.items()}

    def get_valid_fields(self)->dict:
        """
        Получить словарь с валидными полями
        """
        valid_fields = {field_name: field.get_value() for field_name, field in self.fields.items() if not field.is_error}
        if 'pk' in valid_fields:
            valid_fields.pop('pk')
        return valid_fields

    def get_invalid_fields(self)->dict:
        """
        Получить словарь с невалидными полями
        """
        incorrect_fields = {}
        for field_name, field in self.fields.items():
            if field.is_error:
                dic = {
                    field.name: {
                        'value': field.get_value(),
                        'error': field.errors_messages,
                    }
                }
                incorrect_fields.update(dic)
        return incorrect_fields


