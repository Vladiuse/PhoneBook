from exceptions import ObjectDoesNotExist
from model import PhoneRecord
from help_tools import message


class PhoneRecordForm:
    """
    Класс формы модели
    Можно как создавать новую, так и изменять запись из БД
    """

    COLLECT_DATA_MSG = 'Заполните форму'
    UPDATE_DATA_MSG = 'Обновите поля формы (если не вводить значение,поле не будет изменено)'

    def __init__(self, *, initial=None):
        self.fields = ['first_name', 'last_name', 'sur_name', 'organization_name', 'work_phone', 'phone']
        self.initial = initial
        self.initial_data = self.get_initial_data()
        self.models_class = PhoneRecord
        self._is_valid = False

    def _empty_fields(self):
        """
        Получить словарь полей для создания новой модели
        """
        return {field_name: '' for field_name in self.fields}

    def get_initial_data(self):
        """
        Получить словарь ИмяПоля:значение если передан в initial экземпляр иодели(для изменения)
        если создаеться новая запись - значения формы будут пустыми
        :return:
        """
        if not self.initial:
            return self._empty_fields()
        else:
            fields = {}
            for field_name, field in self.initial.fields.items():
                fields[field_name] = field.get_value()
            return fields

    def run(self):
        """
        Отображение формы в терминале
        """
        self.collect_data()
        model = self.models_class(**self.initial_data)
        if model.is_valid():
            self.save(model)
        else:
            incorrect_fields = model.get_invalid_fields()
            self.fix_validations_errors(incorrect_fields=incorrect_fields)

    def fix_validations_errors(self, incorrect_fields=None):
        """
        проверить все ли поля валидны, если не т предложен пользователю их исправить
        """
        for field_name, field in incorrect_fields.items():
            error_value = field['value']
            error_text = field['error']
            message(error_text)
            user_answer = input(f'Введите {field_name}:')
            self.initial_data[field_name] = user_answer
        model = self.models_class(**self.initial_data)
        if model.is_valid():
            self.save(model)
        else:
            message('Eсть некорекнтые поля')
            self.initial_data = model.get_valid_fields()
            incorrect_fields = model.get_invalid_fields()
            return self.fix_validations_errors(incorrect_fields=incorrect_fields)

    def _collect_changes(self):
        """
        Собрать данные от пользователя при изменения сужествуюзей записи
        если поле пропущено (нажат энтер без ввода) подтянеться то чначение которое было
        """
        message(self.UPDATE_DATA_MSG)
        for field_name, field_value in self.initial_data.items():
            message(f'Текущее значение: {field_value}')
            user_value = input(f'Новое значение {field_name}: ')
            if user_value:
                self.initial_data[field_name] = user_value

    def collect_data(self):
        """
        Выбрать режим сбора данные, в зависимости передан ли initial
        """
        message(self.COLLECT_DATA_MSG)
        if self.initial:
            self._collect_changes()
        else:
            self._feed_fields()

    def _feed_fields(self):
        """
        Собрать данные при создании новой записи
        """
        for field_name, field_value in self.initial_data.items():
            user_value = input(f'Введите {field_name}: ')
            self.initial_data[field_name] = user_value

    def save(self, model):
        """Сохранить форму
        Если есть у модели pk - тогда обновиться уже созданая
        """
        if self.initial:
            model.pk = self.initial.pk
        model.save()
        message('Запись сохранена')


class PhoneSearchForm(PhoneRecordForm):
    """
    Форма для поиска записей
    """

    COLLECT_DATA_MSG = 'Введите значения для поиск или пропустите его (Enter)'

    def __init__(self, *, initial=None):
        super().__init__(initial=None)

    def run(self):
        self.collect_data()
        self._clean()

    def _clean(self):
        """
        Отчитска данных от пользователя, удирает пропущеные поля,
         убирает пробелы и переводит в нижний решистер
        """
        for field_name, field_val in self.initial_data.items():
            self.initial_data[field_name] = field_val.strip().lower()

    def get_filter_vals(self):
        return {field_name: field_value for field_name, field_value in self.initial_data.items() if field_value}


class PhoneSearchIdForm:
    """
    Форма поиска записи по ID
    """

    def __init__(self):
        self.pk = None
        self.model_class = PhoneRecord
        self.model = None

    def run(self):
        while True:
            model_id = input('Введите ID записи: ')
            try:
                model_id = int(model_id)
                phone = self.model_class.objects.get(pk=model_id)
            except ValueError:
                message('ID состоит только из цифр!')
            except ObjectDoesNotExist:
                message(f'Запись с ID {model_id} не найдена')
                break
            else:
                self.model = phone
                break
