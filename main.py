from forms import  PhoneSearchIdForm, PhoneRecordForm, PhoneSearchForm
from model import PhoneRecord
from help_tools import TalbePrint
import math


class PhoneBookReader:

    PAGE_SIZE = 10

    def __init__(self):
        self.command_title = None
        self.commands = None
        self.current_page = 1


    def _search(self, search_func):
        form = PhoneSearchForm()
        form.run()
        filter_vals = form.get_filter_vals()
        qs = search_func(**filter_vals)
        TalbePrint(qs).print()

    def all_phones(self):
        phones = PhoneRecord.objects.all()
        TalbePrint(phones).print()

    def search__full(self):
        self._search(PhoneRecord.objects.filter__full)

    def search__startswith(self):
        self._search(PhoneRecord.objects.filter__startswith)

    def search__in(self):
        self._search(PhoneRecord.objects.filter__in)

    def create(self):
        create_form = PhoneRecordForm()
        create_form.run()

    def edit(self):
        serach_form = PhoneSearchIdForm()
        serach_form.run()
        phone = serach_form.model
        form = PhoneRecordForm(initial=phone)
        form.run()

    def delete(self):
        serach_form = PhoneSearchIdForm()
        serach_form.run()
        if serach_form.model:
            phone = serach_form.model
            phone.delete()
            print(f'Запись с ID={phone.pk} удалена')


    def show_page(self):
        start = self.current_page * self.PAGE_SIZE - self.PAGE_SIZE
        end = self.current_page * self.PAGE_SIZE
        phones = PhoneRecord.objects.all()[start:end]
        TalbePrint(phones).print()
        self.print_current_page()

    def next(self):
        self.current_page += 1


    def prev(self):
        self.current_page -= 1


    def last_page_num(self):
        records_count = PhoneRecord.objects.count()
        last_page_num = math.ceil(records_count // self.PAGE_SIZE)
        return last_page_num


    @property
    def has_next(self):
        return self.current_page < self.last_page_num()


    @property
    def has_prev(self):
        return not self.current_page == 1

    def print_current_page(self):
        print(f'Номер страницы: {self.current_page}, всего {self.last_page_num()}', )




class Client:
    MENU_INPUT_TEXT = '\nВведите номер команды:'
    INCORRECT_COMMAND_TEXT = '\nНеверный номер команды!'
    BACK_MENU_TEXT = 'Назад'
    EXIT_TEXT = 'Выход'

    def __init__(self):
        self.phone_reader = PhoneBookReader()
        self._input_msg = ''
        self._actions = {}
        self._printed_text = ''
        self._command_mode = True
        self.set_menu(self.start_menu)

        self._next_menu = None

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
        if user_answer not in self._actions:
            print(self.INCORRECT_COMMAND_TEXT)
            return
        command_method = self.get_action(user_answer)
        if command_method.__name__.endswith('_menu'):
            menu_method = command_method
            self.set_menu(menu_method)
        else:
            command_method()
            if self._next_menu is None:
                self.set_menu(self.start_menu)
            else:
                self.set_menu(self._next_menu)

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
            if command_text in [self.EXIT_TEXT, self.BACK_MENU_TEXT]:
                enumerate_menu_actions[str(0)] = [command_text, command]
            else:
                enumerate_menu_actions[str(counter)] = [command_text, command]
            counter += 1
        return enumerate_menu_actions

    def start_menu(self):
        self._next_menu = None
        commands = {
            'Посмотреть записи': self.show_records_menu,
            'Поиск': self.search_menu,
            'Добавить запись': self.phone_reader.create,
            'Изменить запись': self.phone_reader.edit,
            'Удалить запись': self.delete_menu,
            self.EXIT_TEXT: self.bye,
        }
        return commands

    def show_records_menu(self):
        self._next_menu = None
        commands = {
            'Постраничный просмотр': self.page_view_menu,
            'Посмотреть все записи': self.phone_reader.all_phones,
            self.BACK_MENU_TEXT: self.start_menu,
        }
        return commands


    def delete_menu(self):
        self._next_menu = self.delete_menu
        commands = {
            'Удалить по ID': self.phone_reader.delete,
            self.BACK_MENU_TEXT: self.start_menu,
        }
        return commands

    def search_menu(self):
        self._next_menu = None
        commands = {
            'Поиск (Полное совпадение)': self.phone_reader.search__full,
            'Поиск (Начинаеться с)': self.phone_reader.search__startswith,
            'Поиск (Частичное совпадение)': self.phone_reader.search__in,
            self.BACK_MENU_TEXT: self.start_menu,
        }
        return commands

    def page_view_menu(self):
        self._next_menu = self.page_view_menu
        self.phone_reader.show_page()
        commands = {}
        if self.phone_reader.has_next:
            commands.update({
                'Сдедующая страница': self.phone_reader.next,
            })
        if self.phone_reader.has_prev:
            commands.update({
                'Предыдущая страница': self.phone_reader.prev,
            })
        commands.update({
            self.BACK_MENU_TEXT: self.start_menu,
        })
        return commands


if __name__ == '__main__':
    client = Client()
    client.hello()
    while True:
        client.run()
