from exceptions import ObjectDoesNotExist

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


class PhoneSearchIdForm:

    def __init__(self, model_class):
        self.pk = None
        self.model_class = model_class
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