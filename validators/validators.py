import re

from exceptions import *


class LenValidator:
    """
    Валидатор длинны
    """

    def __init__(self, limit_value):
        self.limit_value = limit_value

    def __call__(self, value):
        if not self.compare(self.limit_value, len(value)):
            raise ValidationError('Неправильная длинна')


class MaxLengthValidator(LenValidator):
    """
    Валидатор макссимальной длинны
    """

    def compare(self, a, b):
        return a >= b


class MinLengthValidator(LenValidator):
    """
    Валидатор минимальной длинны
    """

    def compare(self, a, b):
        return a <= b


class RegExValidator:
    """
    Валидатор строки по решулярномиу выражению
    """
    reg_ex = ''
    error_text = ''

    def __call__(self, value):
        if not re.match(self.reg_ex, value):
            raise ValidationError(f'{self.error_text}: Значение "{value}" не подходит под шаблон {self.reg_ex}')


class NameRegExValidator(RegExValidator):
    """
    Валидатор имени - допускаються толко буквы
    """
    reg_ex = '^[A-Za-zА-ЯЁа-яё]*$'
    error_text = 'Разрешены только руские и английские буквы'


class NumberOnlyRegExValidator(RegExValidator):
    """
    Валидатор номера - допускаються только цифры
    """
    reg_ex = '^\d*$'
    error_text = 'Разрешены только цифры'
