from .queryset import QuerySet


class Manager:
    db_file = 'db.call'

    def __init__(self):
        self.objects = None
        self.unique_keys = {}
        self.model = None

    def __len__(self):
        return len(self.objects)

    def _clean_data(self):
        self.objects = []
        self.unique_keys = {}

    def read_db(self):
        self._clean_data()
        with open(self.db_file) as file:
            for _id, line in enumerate(file):
                phone = self.model.parse(line)
                self.objects.append(phone)

    def _order_records(self):
        self.objects.sort(key=lambda object: (object.first_name, object.last_name))

    def update_db(self):
        self._order_records()
        with open(self.db_file, 'w') as file:
            for model in self.objects:
                file.write(model.render())

    def get_new_pk(self):
        return len(self) + 1

    def save(self, model):
        if self.objects is None:
            self.read_db()
        if not model.pk.get_value():
            model.pk.set_value(self.get_new_pk())
        self.objects.append(model)
        self.update_db()

    def get_queryset(self):
        pass

    def all(self):
        self.read_db()
        qs = QuerySet(self.model, self.objects)
        return qs

