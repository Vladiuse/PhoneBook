from validators import *
from fields import *
from enum import Enum

SEP_CHAR = '|'
NEW_LINE_CHAR = '\n'


class QuerySet:

    def __init__(self, model_class, objects):
        self.models_class = model_class
        self.objects = objects

    def __getitem__(self, item):
        return self.objects[item]


class Manager:
    db_file = 'db.call'

    def __init__(self):
        self.objects = []
        self.unique_keys = {}

    def __len__(self):
        return len(self.objects)

    def _clean_data(self):
        self.objects = []
        self.unique_keys = {}

    def read_db(self):
        self._clean_data()
        with open(self.db_file) as file:
            for _id, line in enumerate(file):
                phone = PhoneRecord.parse(line)
                self.objects.append(phone)

    def _order_records(self):
        self.objects.sort(key=lambda object: (object.first_name, object.last_name))

    def update_db(self):
        self._order_records()
        with open(self.db_file, 'w') as file:
            for model in self.objects:
                file.write(model.render())

    def save(self, model):
        self.objects.append(model)
        print(model)

    def all(self):
        self.read_db()
        qs = QuerySet(PhoneRecord, self.objects)
        return qs


class Model:

    def __init__(self):
        self._errors_messages = []

    def is_valid(self):
        if not hasattr(self, '_is_valid'):
            self._check_fields()
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
                self._errors_messages.extend(field.errors_messages)

    def render(self):
        fields_val = [field.render() for field in self.fields_list]
        return SEP_CHAR.join(fields_val) + NEW_LINE_CHAR

    def save(self):
        if not hasattr(self, '_is_valid'):
            raise AttributeError
        if self.is_valid():
            self._save()
        else:
            raise ValueError

    def _save(self):
        self.objects.save(self)

    @classmethod
    def parse(cls, line):
        return cls(*line.split(SEP_CHAR))

    @property
    def fields(self):
        fields = {field_name: field for field_name, field in self.__dict__.items() if isinstance(field, Field)}
        return fields

    @property
    def fields_list(self):
        return [field for field_name, field in self.fields.items()]


class PhoneRecord(Model):
    objects = Manager()

    def __init__(self, first_name, last_name, sur_name,
                 organization_name, work_phone, phone):
        super().__init__()
        self.first_name = CharField(
            first_name,
            max_length=20,
            validators=[NameRegExValidator(), ],
            verbose_name='Имя',
        )
        self.last_name = CharField(
            last_name,
            max_length=20,
            validators=[NameRegExValidator(), ],
            verbose_name='Фамилия',
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


def seed_db(count=10):
    from faker import Faker
    faker = Faker('ru')
    for _ in range(count):
        phone = PhoneRecord(
            first_name=faker.first_name(),
            last_name=faker.last_name(),
            sur_name=faker.middle_name(),
            organization_name=faker.company(),
            phone=clean_phone(faker.phone_number()),
            work_phone=clean_phone(faker.phone_number())
        )
        if phone.is_valid():
            phone.save()
        else:
            print(phone)
            raise ZeroDivisionError


class PhoneBookReader:
    db_file = 'db.call'

    def print_all(self):
        phones = PhoneRecord.objects.all()
        self.print_objects(phones)

    @staticmethod
    def field_value_max_length(field_name, qs):
        return max(len(object.fields[field_name].get_value()) for object in qs.objects)

    def print_objects(self, qs):
        colls_width = PhoneBookReader.fields_max_lengths(qs, padding_size=1)
        self.print_head(qs, colls_width)
        self.print_lines(qs, colls_width)


    def print_head(self, qs, colls_width):
        obj = qs[0]
        head = [f'{field.verbose_name: <{colls_width[field_name]}}' for field_name, field in obj.fields.items()]
        line = '|'+'|'.join(head)+'|'
        print(line)
        print('|'+'-'*(len(line)-2)+'|')


    def print_lines(self,qs, colls_width):
        for object in qs:
            rendered_fields = []
            for field_name, field in object.fields.items():
                rendered_fields.append(field.render(colls_width[field_name]))
            line = '|' + '|'.join(rendered_fields) + '|'
            print(line)


    @staticmethod
    def fields_max_lengths(qs, padding_size=0):
        colls_width = {}
        obj = qs[0]
        for field_name, field in obj.fields.items():
            field_max_leng = PhoneBookReader.field_value_max_length(field_name, qs)
            colls_width[field_name] = field_max_leng + padding_size
        print(colls_width)
        return colls_width


if __name__ == '__main__':
    phone_book = PhoneBookReader()
    phone_book.print_all()

    #
    # seed_db()
    # PhoneRecord.objects.update_db()
