from models.db import DataBase
from models.queryset import QuerySet


def message(msg, *args, **kwargs):
    print(msg, *args, **kwargs)


class TalbePrint:

    def __init__(self, object, padding=1):
        self.object = object
        self.padding = padding

    def print(self):
        head = self.get_head_array()
        body = self.get_body_array()
        result_array = [head, *body]
        coll_max_width = []
        for col_num, elem in enumerate(head):
            max_coll_len = max(len(str(array[col_num])) for array in result_array)
            max_coll_len += self.padding
            coll_max_width.append(max_coll_len)

        for line in result_array:
            for elem_pos, elem in enumerate(line):
                line[elem_pos] = f'{elem: <{coll_max_width[elem_pos]}}'


        separate_line = '+' + '-' * (sum(coll_max_width) + 6) + '+'
        for pos, line in enumerate(result_array):
            text_line = '|' + '|'.join(line) + '|'
            print(text_line)
            if pos == 0:
                print(separate_line)
        message(self._print_lines_count())

    def _print_lines_count(self):
        count = 1
        if isinstance(self.object, QuerySet):
            count = len(self.object)
        print(f'\nЗаписей: {count}')


    def get_head_array(self):
        head = [DataBase.pk_field_name, ]
        obj = self.object
        if isinstance(self.object, QuerySet):
            obj = self.object[0]
        model_fields_names = [field.verbose_name for field in obj.fields_list]
        head.extend(model_fields_names)
        return head

    def get_body_array(self):
        body_array = []
        if isinstance(self.object, QuerySet):
            for model in self.object:
                line = [model.pk, *model.values_list]
                body_array.append(line)
        else:
            line = [self.object.pk, *self.object.values_list]
            body_array.append(line)
        return body_array

    def __str__(self):
        pass
