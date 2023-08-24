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

    def __init__(self):
        self.commands = None

        self.set_commands(self.start_command())

    def start(self):
         self.hello()

    def hello(self):
        msg = """
***************************
*  Телефонный справочник  *
***************************
        """
        print(msg.strip())

    def set_commands(self, commands):
        res = dict()  # TODO make ordered dict
        counter = 1
        for command_text, command in commands.items():
            res[str(counter)] = [command_text, command]
            counter += 1
        self.commands = res

    def print_command(self):
        for command_code, command_data in self.commands.items():
            command_text = command_data[0]
            print(f'[{command_code}] {command_text}')

    def start_command(self):
        commands = {
            'посмотреть записи': self.print_all,
            'Поиск': 'xx',
            'Добавить запись': 'xx',
            'Удалить запись': 'xx',
            'Изменить запись': 'xx',
            'Выйти': self.bye,
        }
        return commands

    def run_command(self, command_code):
        command = self.commands[command_code][1]
        command()


    def bye(self):
        print('Пока!')
        exit()

    def print_all(self):
        phones = PhoneRecord.objects.all()
        self.print_objects(phones)

    @staticmethod
    def field_value_max_length(field_name, qs):
        return max(len(object.fields[field_name].get_value()) for object in qs.objects)

    def print_objects(self, qs):
        colls_width = PhoneBookReader.fields_max_lengths(qs, padding_size=1)
        self._print_head(qs, colls_width)
        self._print_lines(qs, colls_width)

    def _print_head(self, qs, colls_width):
        obj = qs[0]
        head = [f'{field.verbose_name: <{colls_width[field_name]}}' for field_name, field in obj.fields.items()]
        line = '|' + '|'.join(head) + '|'
        print('+' + '-' * (len(line) - 2) + '+')
        print(line)
        print('+' + '-' * (len(line) - 2) + '+')

    def _print_lines(self, qs, colls_width):
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
    ENTER_COMM_NUMBER_MSG = 'Введите номер команды:'
    phone_book = PhoneBookReader()
    phone_book.hello()
    while True:
        phone_book.print_command()
        user_answer = input(ENTER_COMM_NUMBER_MSG)
        phone_book.run_command(user_answer)
    # phone_book.print_all()

    #
    # seed_db()
    # PhoneRecord.objects.update_db()
