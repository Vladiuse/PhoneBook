from .queryset import QuerySet
from .db import DataBase

class Manager:
    db = DataBase()

    def __init__(self):
        self.objects = None
        self.model = None

    def __len__(self):
        return len(self.objects)

    def _clean_data(self):
        self.objects = []

    def get_objects(self):
        self._clean_data()
        if self.db.table:
            for row in self.db.get_rows():
                phone = self.model.parse(row)
                self.objects.append(phone)

    def _order_records(self):
        self.objects.sort(key=lambda object: (object.first_name, object.last_name))

    def update_db(self):
        self._order_records()
        self.db.write(self._objects_to_string())

    def _objects_to_string(self):
        return ''.join(model.render() for model in self.objects)

    def save(self, model):
        if self.objects is None:
            self.get_objects()
        if not model.pk:
            model.pk = self.db.get_new_pk()
        self.objects.append(model)
        self.update_db()

    def get_queryset(self):
        pass

    def all(self):
        self.get_objects()
        qs = QuerySet(self.model, self.objects)
        return qs

