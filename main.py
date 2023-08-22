from validators import *
from fields import *
from enum import Enum

SEP_CHAR = '|'
NEW_LINE_CHAR = '\n'


class Model:

    def __init__(self):
        self.errors = []

    def render(self):
        fields_val = [str(field) for field_name, field in self.fields]
        return SEP_CHAR.join(fields_val) + NEW_LINE_CHAR

    @staticmethod
    def parse(line):
        return PhoneRecord(*line.split(SEP_CHAR))

    @property
    def fields(self):
        fields = {field_name: field for field_name, field in self.__dict__.items() if isinstance(field, Field)}
        return fields


class PhoneRecord(Model):

    def __init__(self, first_name, last_name, sur_name,
                 organization_name, work_phone, phone):
        super().__init__()
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
    field = CharField('123', max_length=1000, verbose_name='xxx')
