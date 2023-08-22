import re

SEP_CHAR = '|'
NEW_LINE_CHAR = '\n'
MAX_LENGTH = 255
MIN_LENGTH = 0


class ValidationError(Exception):
    pass


class LenValidator:
    def __init__(self, limit_value):
        self.limit_value = limit_value

    def __call__(self, value):
        if not self.compare(self.limit_value, len(value)):
            raise ValidationError


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
            raise ValidationError


class NameRegExValidator(RegExValidator):
    reg_ex = '^[A-Za-zА-ЯЁа-яё]*$'
    error_text = 'Разрешены только руские и английские буквы'


class NumberOnlyRegExValidator(RegExValidator):
    reg_ex = '^\d*$'
    error_text = 'Разрешены только цифры'


class Field:
    max_length = MAX_LENGTH
    min_length = MIN_LENGTH
    default_validators = []

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
        self.verbose_name = verbose_name
        self.unique = unique
        self.validators = [] if not validators else validators

        self._clean()
        self._validate()

    def __str__(self):
        return f'{self.value: <{self.max_length}}'

    def _check_length_attrs(self):
        if self.min_length > self.max_length:
            raise ValidationError()
        if not (self.max_length > 0 and self.max_length < MAX_LENGTH):
            raise ValidationError('Длина поня долджны быть в диапозоне от 0 до 255')
        if self.min_length < 0:
            raise ValidationError()

    def get_value(self):
        return self.value

    @property
    def _length_validators(self):
        return [MaxLengthValidator(self.max_length),
                MinLengthValidator(self.min_length), ]

    def _validate(self):
        validators = [*self._length_validators, *self.default_validators, *self.validators]
        for validator in validators:
            print(validator)
            validator(self.get_value())

    def _clean(self):
        self.value = self.value.strip()


class CharField(Field):
    pass


class IntegerField(CharField):
    default_validators = [
        NumberOnlyRegExValidator()
    ]


class PhoneRecord:

    def __init__(self, first_name, last_name, sur_name,
                 organization_name, work_phone, phone):
        self.first_name = CharField(
            first_name,
            max_length=20,
            validators=[NameRegExValidator(), ],
        )
        self.last_name = CharField(
            last_name,
            max_length=20,
            validators=[NameRegExValidator(), ],
        )
        self.sur_name = CharField(
            sur_name,
            max_length=20,
            validators=[NameRegExValidator(), ],
        )
        self.organization_name = CharField(
            organization_name,
            max_length=50,
        )
        self.work_phone = IntegerField(
            work_phone,
            min_length=9,
            max_length=12,
            unique=True,
        )
        self.phone = IntegerField(
            phone,
            min_length=9,
            max_length=12,
            unique=True,
        )

    def render(self):
        fields_val = [str(field) for var, field in self.__dict__.items()]
        return SEP_CHAR.join(fields_val) + NEW_LINE_CHAR

    @staticmethod
    def parse(line):
        return PhoneRecord(*line.split(SEP_CHAR))


class DataBase:
    db_file = 'db.call'

    def write(self):
        pass

    def append(self, line):
        with open(self.db_file, 'a') as file:
            file.write(line)

    def read(self, lines_count):
        pass


def clean_phone(phone):
    return ''.join(char for char in phone if char.isdigit())


def seed_db():
    from faker import Faker
    faker = Faker('ru')
    db = DataBase()
    for _ in range(100):
        phone = PhoneRecord(
            first_name=faker.first_name(),
            last_name=faker.last_name(),
            sur_name=faker.middle_name(),
            organization_name=faker.company(),
            phone=clean_phone(faker.phone_number()),
            work_phone=clean_phone(faker.phone_number())
        )
        db.append(phone.render())


class PhoneBook:
    db_file = 'db.call'

    def __init__(self):
        self.work_phones = dict()
        self.lines = list()

    def __len__(self):
        return len(self.lines)

    def read_db(self):
        with open(self.db_file) as file:
            for _id, line in enumerate(file):
                phone = PhoneRecord.parse(line)
                self.lines.append(phone)
                self.work_phones[phone.work_phone] = phone

    def _order_records(self):
        self.lines.sort()

    def save(self):
        self._order_records()
        with open(self.db_file, 'w') as file:
            for phone in self.lines:
                file.write(phone.render())


if __name__ == '__main__':
    seed_db()
