from .queryset import QuerySet
class Manager:
    db_file = 'db.call'

    def __init__(self):
        self.objects = []
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

    def save(self, model):
        self.objects.append(model)
        print(model)

    def all(self):
        self.read_db()
        qs = QuerySet(self.model, self.objects)
        return qs

