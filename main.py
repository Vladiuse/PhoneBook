from fields import *
from models import Model
from forms import PhoneRecordForm, PhoneSearchIdForm, PhoneEditForm
from model import PhoneRecord
from help_tool import message

class PhoneBookReader:
    ENTER_COMMAND_NUM_MSG = 'Введите номер команды:'
    db_file = 'db.call'

    def __init__(self):
        self.command_title = None
        self.commands = None

    def all_phones(self):
        phones = PhoneRecord.objects.all()
        phones.print()

    def form_fields(self):
        fields = {'first_name': '',
                  'last_name': '',
                  'sur_name': '',
                  'organization_name': '',
                  'work_phone': '',
                  'phone': '',
                  }
        return fields

    def create(self, initial_data=None, fields=None):
        form_data = {}
        if initial_data:
            form_data = initial_data
        if not fields:
            fields = PhoneRecordForm.get_form()
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
            return self.create(initial_data=correct_fields, fields=incorrect_fields)

    def edit_form(self):
        while True:
            serach_form = PhoneSearchIdForm()
            serach_form.run()
            phone = serach_form.model
            message('Обновите поля формы (если не вводить значение,поле не будет изменено')
            form = PhoneRecordForm.get_form(phone)
            for field_name, field_value in form.items():
                message(f'Текущее значение: {field_value}')
                input(f'Новое значение {field_name}: ')
            break

    def delete_form(self):
        while True:
            serach_form = PhoneSearchIdForm()
            serach_form.run()
            phone = serach_form.model
            phone.delete()
            print(f'Запись с ID={phone.pk} удалена')
            break

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
            self.set_menu(self.start_menu)
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
            'посмотреть записи': self.phone_reader.all_phones,
            'Поиск': self.search_menu,
            'Добавить запись': self.phone_reader.create,
            'Изменить запись': self.phone_reader.edit_form,
            'Удалить запись': self.delete_menu,
            'Выйти': self.bye,
        }
        return commands

    def delete_menu(self):
        commands = {
            'Найти и удалить': self.search_menu,
            'Удалить по ID': self.phone_reader.delete_form,
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
    # client = Client()
    # client.hello()
    # while True:
    #     client.run()
    phone = PhoneRecord.objects.get(pk=23)
    form = PhoneEditForm()
    form.run()


