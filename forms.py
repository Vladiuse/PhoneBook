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