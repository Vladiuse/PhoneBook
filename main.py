import re


SEP_CHAR = '|'
NEW_LINE_CHAR = '\n'


class ValidationError(Exception):
    pass


class LenValidateError(Exception):
    pass


class Field:
    max_length = 30
    min_length = 1
    reg_ex = ''
    validation_error_text = ''

    def __init__(self, value, *,max_length=None, verbose_name=None,reg_ex=None, unique=False):
        self.value = value
        self.max_length = max_length if max_length else Field.max_length
        self.reg_ex = reg_ex if reg_ex else Field.reg_ex
        self.verbose_name = verbose_name
        self.unique = unique

        self._clean()
        self._validate()

    def __str__(self):
        return f'{self.value: <{self.max_length}}'


    def _validate(self):

        self._reg_validate()
        self.length_validate()

    def _clean(self):
        self.value = self.value.strip()

    def _reg_validate(self):
        if self.reg_ex:
            if not re.match(self.reg_ex, self.value):
                print(self.value)
                raise ValidationError(str(self.validation_error_text))

    def length_validate(self):
        if len(self.value) < self.min_length:
            raise LenValidateError(self.value)
        if len(self.value) > self.max_length:
            raise LenValidateError(self.value)


class IntegerField(Field):
    reg_ex = '^\d*$'
    validation_error_text='Допускаються только цифры'


class CharField(Field):
    # reg_ex = '^[A-Za-zА-Яа-я]*$'
    pass


class PhoneRecord:
    NAME_REG_EX = '^[A-Za-zА-ЯЁа-яё]*$'

    def __init__(self, first_name, last_name, sur_name,
                 organization_name, work_phone, phone):
        self.first_name = CharField(first_name, max_length=20, reg_ex=PhoneRecord.NAME_REG_EX)
        self.last_name = CharField(last_name, max_length=20, reg_ex=PhoneRecord.NAME_REG_EX)
        self.sur_name = CharField(sur_name, max_length=20, reg_ex=PhoneRecord.NAME_REG_EX)
        self.organization_name = CharField(organization_name, max_length=50)
        self.work_phone = IntegerField(work_phone, max_length=12, unique=True)
        self.phone = IntegerField(phone, max_length=12, unique=True)

    def raw_data(self):
        fields_val = [str(field) for var,field in self.__dict__.items()]
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
        db.append(phone.raw_data())
class PhoneBook:
    db_file = 'db.call'

    def __init__(self):
        self.work_phones = dict()
        self.lines = list()

    def read_db(self):
        with open(self.db_file) as file:
            for _id, line in enumerate(file):
                phone = PhoneRecord.parse(line)
                self.lines.append(phone)
                self.work_phones[phone.work_phone] = phone

    def order_book(self):
        self.lines.sort()


    def save(self):
        with open(self.db_file, 'w') as file:
            for phone in self.lines:
                file.write(phone.raw_data())

    def __len__(self):
        return len(self.lines)


if __name__ == '__main__':
    book = PhoneBook()
    book.read_db()
    print(len(book))
    book.save()
    # seed_db()