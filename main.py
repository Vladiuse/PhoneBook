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
    ENTER_COMMAND_NUM_MSG = 'Введите номер команды:'
    db_file = 'db.call'

    def __init__(self):
        self.command_title = None
        self.commands = None

    def all_phones(self):
        phones = PhoneRecord.objects.all()

    def create_record(self, **kwargs):
        pass

    def add_record(self):
        pass

    def form_fields(self):
        fields = {'first_name': '',
                  'last_name': '',
                  'sur_name': '',
                  'organization_name': '',
                  'work_phone': '',
                  'phone': '',
                  }
        return fields

    def get_form_fields(self, initial_data=None, fields=None):
        form_data = {}
        if initial_data:
            form_data = initial_data
        if not fields:
            fields = self.form_fields()
        for field_name, error in fields.items():
            if error:
                error_value = error['value']
                error_text = error['error']
                print(error_value, error_text)
            user_answer = input(f'Введите {field_name}:')
            form_data[field_name] = user_answer
        phone = PhoneRecord(**form_data)
        if phone.is_valid():
            print('SAVE')
            phone.save()
        else:
            print('Eсть некорекнтые поля')
            correct_fields = phone.get_valid_fields()
            incorrect_fields = phone.get_invalid_fields()
            return self.get_form_fields(initial_data=correct_fields, fields=incorrect_fields)


class Client:
    MENU_INPUT_TEXT = 'Введите номер команды:'

    def __init__(self):
        self.phone_reader = PhoneBookReader()
        self._input_msg = ''
        self._actions = {}
        self._printed_text = ''
        self._command_mode = True
        self.set_menu(self.start_menu)

    def hello(self):
        msg = """
***************************
*  Телефонный справочник  *
***************************
        """
        print(msg.strip())

    def bye(self):
        print('Пока!')
        exit()

    def run(self):
        if self._printed_text:
            print(self._printed_text)
        user_answer = input(self._input_msg)
        command_method = self.get_action(user_answer)
        if command_method.__name__.endswith('_menu'):
            menu_method = command_method
            self.set_menu(menu_method)
        else:
            command_method()

    def get_action(self, user_answer):
        if user_answer == 'exit':
            self.bye()
        if user_answer not in self._actions:
            print('Wrong action')
        else:
            return self._actions[user_answer]

    def set_actions(self, actions: dict):
        self._actions = actions

    def set_printed_text(self, text: str):
        self._printed_text = text

    def set_input_msg(self, msg):
        self._input_msg = msg

    def set_menu(self, menu_method):
        enumerated_menu = self._enumerate_menu(menu_method)
        self.set_actions(self._get_menu_actions(enumerated_menu))
        self.set_printed_text(self._get_menu_text(enumerated_menu))
        self._input_msg = self.MENU_INPUT_TEXT

    def _get_menu_text(self, enumarated_menu):
        lines = ['\n']
        for command_code, command_data in enumarated_menu.items():
            command_text = command_data[0]
            line = f'[{command_code}] {command_text}'
            lines.append(line)
        text = '\n'.join(lines)
        return text

    def _get_menu_actions(self, enumarated_menu):
        actions = {}
        for command_num, command_data in enumarated_menu.items():
            actions[command_num] = command_data[1]
        return actions

    def _enumerate_menu(self, menu_method):
        menu_data = menu_method()
        enumerate_menu_actions = dict()  # TODO make ordered dict
        counter = 1
        for command_text, command in menu_data.items():
            enumerate_menu_actions[str(counter)] = [command_text, command]
            counter += 1
        return enumerate_menu_actions

    def start_menu(self):
        commands = {
            'посмотреть записи': 'x',
            'Поиск': self.search_menu,
            'Добавить запись': self.phone_reader.get_form_fields,
            'Удалить запись': self.delete_menu,
            'Изменить запись': 'xx',
            'Выйти': self.bye,
        }
        return commands

    def delete_menu(self):
        commands = {
            'Найти и удалить': self.search_menu,
            'Удалить по номеру': self.search_menu,
            'Выйти': self.bye,
        }
        return commands

    def search_menu(self):
        commands = {
            'Поиск по номеру': 'xxx',
            'Поиск по имени': 'xxx',
            'Назад': self.start_menu,
        }
        return commands


if __name__ == '__main__':
    client = Client()
    client.hello()
    while True:
        client.run()
    #
    # seed_db()
    # PhoneRecord.objects.update_db()
