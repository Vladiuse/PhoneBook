from .manager import Manager
from fields import Field, PrimaryKeyField
from .db import DataBase

class Model:
    objects = Manager()

    def __init__(self,pk=None):
        self.pk = pk
        self._errors_messages = {}
        self._set_class()
        self._field_names_setted = False

    @classmethod
    def _set_class(cls):
        cls.objects.model = cls


    def _set_fields_name(self):
        for field_name, field in self.fields.items():
            field.name = field_name

    def is_valid(self):
        if not hasattr(self, '_is_valid'):
            self._check_fields()
            self._collect_fields_errors()
            return self._is_valid
        return self._is_valid

    def _check_fields(self):
        setattr(self, '_is_valid', True)
        for field in self.fields_list:
            field.validate()
            if field.is_error:
                self._is_valid = False

    @property
    def errors(self):
        if not hasattr(self, '_is_valid'):
            raise AttributeError
        return self._errors_messages

    def _collect_fields_errors(self):
        for field in self.fields_list:
            if field.is_error:
                self._errors_messages[field.name] = field.errors_messages

    def _render_pk(self, max_size=None):
        if not max_size:
            max_size = DataBase.pk_max_size
        return f'{self.pk: <{max_size}}'

    def render(self):
        fields_val = [field.render() for field in self.fields_list]
        fields_val.insert(0, self._render_pk())
        return DataBase.SEP_CHAR.join(fields_val) + DataBase.NEW_LINE_CHAR

    @classmethod
    def parse(cls, line):
        pk, *attrs = line.split(DataBase.SEP_CHAR)
        return cls(*attrs,pk=int(pk))



    def save(self):
        if not hasattr(self, '_is_valid'):
            raise AttributeError
        if self.is_valid():
            self._save()
        else:
            raise ValueError('Модель не проверена')

    def delete(self):
        self.objects.delete(self.pk)

    def _save(self):
        self.objects.save(self)



    @property
    def fields(self):
        fields = {field_name: field for field_name, field in self.__dict__.items() if isinstance(field, Field)}
        if not self._field_names_setted:
            for field_name, field in fields.items():
                field.name = field_name

        return fields

    @property
    def fields_list(self):
        return [field for field_name, field in self.fields.items()]

    @property
    def values_list(self):
        return [field.get_value() for field in self.fields_list]

    def get_valid_fields(self):
        valid_fields = {field_name: field.get_value() for field_name, field in self.fields.items() if not field.is_error}
        if 'pk' in valid_fields:
            valid_fields.pop('pk')
        return valid_fields

    def get_invalid_fields(self):
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


