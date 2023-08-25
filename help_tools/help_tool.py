from models.db import DataBase
from models.queryset import QuerySet


# тк print иногда используеться для,
# его можно спутать с принтом программы
def message(msg, *args, **kwargs):
    """Вывод текста в терминал"""
    print(msg, *args, **kwargs, )


class TablePrint:
    """Вывод в терминал таблици с элементами БД"""

    def __init__(self, object, padding=1):
        self.object = object
        self.padding = padding

    def print(self):
        """Вывести в консоль таблицу"""
        # тут ведеться подстчет ширины в символах значений в ячейках каждой колонки
        # для красивого вывода в консоли
        head = self.get_head_array()
        body = self.get_body_array()
        result_array = [head, *body]
        coll_max_width = []  # сюда складываю максимальную длину у ячейки в колоне
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
            message(text_line)
            if pos == 0:
                message(separate_line)

        self._print_lines_count()

    def _print_lines_count(self):
        """Вывод количества строк в таблице"""
        count = 1
        if isinstance(self.object, QuerySet):
            count = len(self.object)
        message(f'\nЗаписей: {count}')

    def get_head_array(self):
        """Получения масива для отрисовки шапки таблицы"""
        head = [DataBase.pk_field_name, ]
        if isinstance(self.object, QuerySet):
            head.extend(self.object.models_class.fields_map)
        else:
            head.extend(self.object.fields_map)
        return head

    def get_body_array(self):
        """Получения масива для отрисовки тела таблицы"""
        body_array = []
        if isinstance(self.object, QuerySet):
            for model in self.object:
                line = [model.pk, *model.values_list]
                body_array.append(line)
        else:
            line = [self.object.pk, *self.object.values_list]
            body_array.append(line)
        return body_array
