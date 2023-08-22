from exceptions import *
from validators import *

MAX_LENGTH = 255
MIN_LENGTH = 0


class Field:
    max_length = MAX_LENGTH
    min_length = MIN_LENGTH
    default_validators = []
    field_name = 'Field'

    def __init__(self, value, *,
                 max_length=None,
                 min_length=None,
                 verbose_name=None,
                 unique=False,
                 validators=None,
                 ):
        self.value = value
        self.max_length = max_length if max_length else self.max_length
        self.min_length = min_length if min_length else self.min_length
        self.verbose_name = verbose_name if verbose_name else self.field_name
        self.unique = unique
        self.validators = [] if not validators else validators

        self._check_length_attrs()
        self._clean()
        self._validate()

    def __str__(self):
        return f'{self.value: <{self.max_length}}'

    def __repr__(self):
        return f'{self.field_name}: {self.value}'

    def _check_length_attrs(self):
        if self.min_length > self.max_length:
            error_mgs = f'Атрибут поля {self.verbose_name} min_length не должен быть больше max_length'
            raise FieldError(error_mgs)
        if self.max_length < 0 or self.max_length > MAX_LENGTH:
            error_mgs = f'Длина поля {self.verbose_name} долджна быть в диапозоне от 0 до 255'
            raise FieldError(error_mgs)
        if self.min_length < 0:
            error_mgs = f'Атрибут min_length поля {self.verbose_name} не может быть меньше 0'
            raise FieldError(error_mgs)

    def get_value(self):
        return self.value

    @property
    def _length_validators(self):
        return [MaxLengthValidator(self.max_length),
                MinLengthValidator(self.min_length), ]

    def _validate(self):
        validators = [*self._length_validators, *self.default_validators, *self.validators]
        for validator in validators:
            validator(self.get_value())

    def _clean(self):
        self.value = self.value.strip()


class CharField(Field):
    field_name = 'CharField'


class IntegerField(CharField):
    field_name = 'IntegerField'
    default_validators = [
        NumberOnlyRegExValidator()
    ]
