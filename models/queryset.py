class QuerySet:

    def __init__(self, model_class, objects):
        self.models_class = model_class
        self.objects = objects

    def __getitem__(self, item):
        return self.objects[item]