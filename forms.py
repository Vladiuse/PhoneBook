from exceptions import ObjectDoesNotExist
from model import PhoneRecord
from help_tool import message

class PhoneRecordForm:

    @staticmethod
    def _empty_fields():
        fields = {'first_name': '',
                  'last_name': '',
                  'sur_name': '',
                  'organization_name': '',
                  'work_phone': '',
                  'phone': '',
                  }
        return fields

    @staticmethod
    def get_form(model=None):
        if model:
            fields = {}
            for field_name, field in model.fields.items():
                fields[field_name] = field.get_value()
            return fields
        else:
            return PhoneRecordForm._empty_fields()

class PhoneEditForm:

    def __init__(self, *,initial=None):
        self.initial = initial
        self.initial_data = self.get_initial_data()
        self.models_class = PhoneRecord
        # self._fields = None

        self._is_valid = False


    @staticmethod
    def _empty_fields():
        fields = {'first_name': '',
                  'last_name': '',
                  'sur_name': '',
                  'organization_name': '',
                  'work_phone': '',
                  'phone': '',
                  }
        return fields

    def get_initial_data(self):
        if not self.initial:
            return self._empty_fields()
        else:
            fields = {}
            for field_name, field in self.initial.fields.items():
                fields[field_name] = field.get_value()
            return fields

    # def get_form(self):
    #     fields = {}
    #     for field_name, field in self.initial_model.fields.items():
    #         fields[field_name] = field.get_value()
    #     self._fields = fields


    def run(self):
        model = self.models_class(**self.initial_data)
        if model.is_valid():
            model.save()
        else:
            self.fix_validations_errors()

    def fix_validations_errors(self,inccorect_fields=None):
        for field_name, field in inccorect_fields.items():
            error_value = field['value']
            error_text = field['error']
            message(error_value, error_text)
            user_answer = input(f'Введите {field_name}:')
            self.initial_data[field_name] = user_answer
        phone = self.models_class(**self.initial_data)
        if phone.is_valid():
            print('SAVE')
            phone.save()
        else:
            print('Eсть некорекнтые поля')
            self.initial_data = phone.get_valid_fields()
            incorrect_fields = phone.get_invalid_fields()
            return self.fix_validations_errors(inccorect_fields=incorrect_fields)

    def _collect_changes(self):
        message('Обновите поля формы (если не вводить значение,поле не будет изменено')
        for field_name, field_value in self.initial_data.items():
            message(f'Текущее значение: {field_value}')
            user_value = input(f'Новое значение {field_name}: ')
            if user_value:
                self.initial_data[field_name] = user_value
        print('Updated data',self.initial_data)

    def save(self):
        pass






class PhoneSearchIdForm:

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
                print('ID состоит только из цифр!')
            except ObjectDoesNotExist:
                print(f'Запись с ID {model_id} не найдена')
            else:
                self.model = phone
                break