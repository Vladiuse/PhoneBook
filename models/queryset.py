from .db import DataBase

class QuerySet:

    def __init__(self, model_class, objects_list):
        self.models_class = model_class
        self.objects = objects_list

        self.colls_width = self.fields_max_lengths()

    def __getitem__(self, item):
        return self.objects[item]

    def print(self):
        self._print_head()
        self._print_lines()


    def field_value_max_length(self,field_name):
        return max(len(object.fields[field_name]) for object in self.objects)

    def pk_max_length(self):
        return max(len(str(obj.pk)) for obj in self.objects)

    def fields_max_lengths(self, padding_size=1):
        colls_width = {}
        obj = self[0]
        for field_name, field in obj.fields.items():
            field_max_leng = self.field_value_max_length(field_name)
            colls_width[field_name] = field_max_leng + padding_size
        colls_width['pk'] = self.pk_max_length()
        return colls_width

    def _print_head(self):
        obj = self[0]
        head = [f'{field.verbose_name: <{self.colls_width[field_name]}}' for field_name, field in obj.fields.items()]
        head.insert(0, f'{DataBase.pk_field_name: <{self.colls_width["pk"]}}')
        line = '|' + '|'.join(head) + '|'
        print('+' + '-' * (len(line) - 2) + '+')
        print(line)
        print('+' + '-' * (len(line) - 2) + '+')

    def _print_lines(self):
        for object in self:
            rendered_fields = []
            for field_name, field in object.fields.items():
                rendered_fields.append(field.render(self.colls_width[field_name]))
            rendered_fields.insert(0, object._render_pk(max_size=self.colls_width["pk"]))
            line = '|' + '|'.join(rendered_fields) + '|'
            print(line)
        print(' ')
