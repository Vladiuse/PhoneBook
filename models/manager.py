from .queryset import QuerySet
from .db import DataBase
from exceptions import ObjectDoesNotExist

class Manager:
    db = DataBase()

    def __init__(self):
        self.objects = None
        self.model = None

    def __len__(self):
        return len(self.objects)

    def _clean_data(self):
        if self.objects is None:
            self.objects = dict()
        self.objects.clear()

    def get_objects_from_db(self):
        self._clean_data()
        if self.db.table:
            for row in self.db.get_rows():
                phone = self.model.parse(row)
                self.objects[phone.pk] = phone

    # def _order_records(self):
    #     self.objects.sort(key=lambda object: (object.first_name, object.last_name))

    def update_db(self):
        # self._order_records()
        self.db.write(self._objects_to_string())

    def _objects_to_string(self):
        return ''.join(model.render() for model in self.get_objects_list())

    def save(self, model):
        if self.objects is None:
            self.get_objects_from_db()

        if not model.pk:
            model.pk = self.db.get_new_pk()
            self.add_object(model)
        else:
            self.update_object(model)
        self.update_db()

    def delete(self, pk):
        self.objects.pop(pk)
        self.update_db()

    def add_object(self, obj):
        self.objects[obj.pk] = obj

    def update_object(self, obj):
        if obj.pk not in self.objects:
            raise ValueError('Ошибка обновления, нет такого айди')
        self.objects[obj.pk] = obj

    def get_objects_list(self):
        if self.objects is None:
            self.get_objects_from_db()
        return [model for pk, model in self.objects.items()]

    def get(self,*,pk):
        self.get_objects_from_db()
        try:
            return self.objects[pk]
        except KeyError:
            raise ObjectDoesNotExist


    def get_queryset(self):
        pass

    def all(self):
        self.get_objects_from_db()
        qs = QuerySet(self.model, self.get_objects_list())
        return qs

    def filter__full(self, **kwargs):
        models = []
        for model in self.get_objects_list():
            model_value = model.values
            match = [model_value[filter_key].lower() == filter_val for filter_key, filter_val in kwargs.items()]
            if all(match):
                models.append(model)
        qs = QuerySet(self.model, models)
        return qs

    def filter__startswith(self, **kwargs):
        models = []
        for model in self.get_objects_list():
            model_value = model.values
            match = [model_value[filter_key].lower().startswith(filter_val) for filter_key, filter_val in kwargs.items()]
            if any(match):
                models.append(model)
        qs = QuerySet(self.model, models)
        return qs

    def filter__in(self, **kwargs):
        models = []
        for model in self.get_objects_list():
            model_value = model.values
            match = [filter_val in model_value[filter_key].lower() for filter_key, filter_val in kwargs.items()]
            if any(match):
                models.append(model)
        qs = QuerySet(self.model, models)
        return qs

    def count(self):
        if self.objects is None:
            self.get_objects_from_db()
        return self.db.count()


