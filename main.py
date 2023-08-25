from forms import PhoneSearchIdForm, PhoneRecordForm, PhoneSearchForm
from model import PhoneRecord
from help_tools import TablePrint
import math


class PhoneBookReader:
    """Клас телефонной книги"""

    PAGE_SIZE = 10

    def __init__(self):
        self.command_title = None
        self.commands = None
        self.current_page = 1

    def _search(self, search_func):
        """
        Вывести список телефонных записей удовлетворяющий условию поиска
        """
        form = PhoneSearchForm()
        form.run()
        filter_vals = form.get_filter_vals()
        qs = search_func(**filter_vals)
        TablePrint(qs).print()

    def all_phones(self):
        """
        Вывести все записи телефонов
        :return:
        """
        phones = PhoneRecord.objects.all()
        TablePrint(phones).print()

    def search__full(self):
        """Поиск - полное соответствие"""
        self._search(PhoneRecord.objects.filter__full)

    def search__startswith(self):
        """Поиск одно из полей начинаеться с.."""
        self._search(PhoneRecord.objects.filter__startswith)

    def search__in(self):
        """Поиск - одно из полей содержит подстроку"""
        self._search(PhoneRecord.objects.filter__in)

    # view
    def create(self):
        """
        Cоздание новой записы
        """
        create_form = PhoneRecordForm()
        create_form.run()

    # view
    def edit(self):
        """
        редактирование сузествующей записы (поиск по  ШВ)
        """
        serach_form = PhoneSearchIdForm()
        serach_form.run()
        phone = serach_form.model
        form = PhoneRecordForm(initial=phone)
        form.run()

    # view
    def delete(self):
        """
        Удалить запись - поиск по ID
        """
        serach_form = PhoneSearchIdForm()
        serach_form.run()
        if serach_form.model:
            phone = serach_form.model
            phone.delete()
            print(f'Запись с ID={phone.pk} удалена')

    def show_page(self):
        """
        Показать страницу с записями справочника
        """
        start = self.current_page * self.PAGE_SIZE - self.PAGE_SIZE
        end = self.current_page * self.PAGE_SIZE
        phones = PhoneRecord.objects.all()[start:end]
        TablePrint(phones).print()
        self.print_current_page()

    def next(self):
        """
        Следующая страница справочника
        """
        self.current_page += 1

    def prev(self):
        """Предедущая страница справочника"""
        self.current_page -= 1

    def last_page_num(self):
        """
        Получить номер последней страницы справочника
        :return:
        """
        records_count = PhoneRecord.objects.count()
        last_page_num = math.ceil(records_count // self.PAGE_SIZE)
        return last_page_num

    @property
    def has_next(self):
        """
        Есть ли еще страницы дальще
        """
        return self.current_page < self.last_page_num()

    @property
    def has_prev(self):
        """
        Есть ли предыдущая страница
        """
        return not self.current_page == 1

    def print_current_page(self):
        """
        Вывести количество страниц в справочнике и текущю страницу:
        """
        print(f'Номер страницы: {self.current_page}, всего {self.last_page_num()}', )


class Client:
    """Класс управляющий интерфейом командной строки"""

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
        """
        Выйти из программы
        """
        print('Пока!')
        exit()

    def run(self):
        """
        Главный цикл - проверяет команты
        , елси это команды меню- отображает коды и названия дейсткий,
        при выборе команд поиска/удаления/создания формы перехватывают главный цикл на себя
        :return:
        """
        if self._printed_text:
            print(self._printed_text)
        user_answer = input(self._input_msg)
        if user_answer not in self._actions:
            print(self.INCORRECT_COMMAND_TEXT)
            return
        command_method = self.get_action(user_answer)
        if command_method.__name__.endswith('_menu'):
            # отобразить выбраное менб и его команды
            menu_method = command_method
            self.set_menu(menu_method)
        else:
            # запуск внешних действий
            command_method()
            if self._next_menu is None:  # определить какое меню показывать следующим
                self.set_menu(self.start_menu)
            else:
                self.set_menu(self._next_menu)

    def get_action(self, user_answer: str):
        """
        Проверка ввода от пользователя
        при exit програма выключиться
        при вводе несуществующей команды - высветиться ошибка
        """
        if user_answer == 'exit':
            self.bye()
        if user_answer not in self._actions:
            print('Wrong action')
        else:
            return self._actions[user_answer]

    def set_actions(self, actions: dict):
        """
        Установить словарь с действиями
        """
        self._actions = actions

    def set_printed_text(self, text: str):
        """
        Установить отображаемый текст
        """
        self._printed_text = text

    def set_input_msg(self, msg: str):
        """
        Установить отображаемый текс в input
        """
        self._input_msg = msg

    def set_menu(self, menu_method):
        """
        Установить выбраное менб:
        """
        enumerated_menu = self._enumerate_menu(menu_method)
        self.set_actions(self._get_menu_actions(enumerated_menu))
        self.set_printed_text(self._get_menu_text(enumerated_menu))
        self._input_msg = self.MENU_INPUT_TEXT

    def _get_menu_text(self, enumarated_menu: dict) -> str:
        """
        получить словарь для текстового отображения в консоле выбраного меню
        коды комманд и их подписи
        """
        lines = ['\n']
        for command_code, command_data in enumarated_menu.items():
            command_text = command_data[0]
            line = f'[{command_code}] {command_text}'
            lines.append(line)
        text = '\n'.join(lines)
        return text

    def _get_menu_actions(self, enumarated_menu) -> dict:
        """
        преобразовать менб в словарь - с номерами команд и
        связаными с ними функциями
        """
        actions = {}
        for command_num, command_data in enumarated_menu.items():
            actions[command_num] = command_data[1]
        return actions

    def _enumerate_menu(self, menu_method) -> dict:
        """
        Пронумеровать выбраное меню (чтоб у команд появились номера)
        Если это команда выхода или вазврата в предыдущее меню - будет задан номер 0
        """
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

    def start_menu(self) -> dict:
        """Стартовое меню"""
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

    def show_records_menu(self) -> dict:
        """Менб просмотра записей справочника"""
        self._next_menu = None
        commands = {
            'Постраничный просмотр': self.page_view_menu,
            'Посмотреть все записи': self.phone_reader.all_phones,
            self.BACK_MENU_TEXT: self.start_menu,
        }
        return commands

    def delete_menu(self) -> dict:
        """Меню удаления записей"""
        self._next_menu = self.delete_menu
        commands = {
            'Удалить по ID': self.phone_reader.delete,
            self.BACK_MENU_TEXT: self.start_menu,
        }
        return commands

    def search_menu(self) -> dict:
        """менб поиска записей справочника"""
        self._next_menu = None
        commands = {
            'Поиск (Полное совпадение)': self.phone_reader.search__full,
            'Поиск (Начинаеться с)': self.phone_reader.search__startswith,
            'Поиск (Частичное совпадение)': self.phone_reader.search__in,
            self.BACK_MENU_TEXT: self.start_menu,
        }
        return commands

    def page_view_menu(self) -> dict:
        """Меню постраничного просмотра"""
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
