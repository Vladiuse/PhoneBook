from fields import *
from models import Model


class PhoneRecord(Model):

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


PhoneRecord._set_class()


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
        line = '|' + '|'.join(head) + '|'
        print(line)
        print('|' + '-' * (len(line) - 2) + '|')

    def print_lines(self, qs, colls_width):
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
