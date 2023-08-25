import re

from exceptions import *

class LenValidator:
    def __init__(self, limit_value):
        self.limit_value = limit_value

    def __call__(self, value):
        if not self.compare(self.limit_value, len(value)):
            raise ValidationError('Неправильная длинна')


class MaxLengthValidator(LenValidator):

    def compare(self, a, b):
        return a >= b


class MinLengthValidator(LenValidator):
    def compare(self, a, b):
        return a <= b


class RegExValidator:
    reg_ex = ''
    error_text = ''

    def __call__(self, value):
        if not re.match(self.reg_ex, value):
            raise ValidationError(f'Значение {value} не подходит под шаблон {self.reg_ex}' )


class NameRegExValidator(RegExValidator):
    reg_ex = '^[A-Za-zА-ЯЁа-яё]*$'
    error_text = 'Разрешены только руские и английские буквы'


class NumberOnlyRegExValidator(RegExValidator):
    reg_ex = '^\d*$'
    error_text = 'Разрешены только цифры'
#
#
# class PrimaryKeyValidator:
#
#     def __call__(self, value):
#         try:
#             int(value)
#         except ValueError:
#             raise ValidationError('ID должен состоять только из цифр')