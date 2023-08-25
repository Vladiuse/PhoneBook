from .db import DataBase

class QuerySet:

    def __init__(self, model_class, objects_list):
        self.models_class = model_class
        self.__objects = objects_list

    def __getitem__(self, item):
        if isinstance(item, int):
            return self.__objects[item]
        else:
            return QuerySet(self.models_class,self.__objects[item.start:item.stop])

    def __len__(self):
        return len(self.__objects)

    def __str__(self):
        return f'<QuerySet>: {[str(obj) for obj in self.__objects]}'

