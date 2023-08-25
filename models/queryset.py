from .db import DataBase

class QuerySet:

    def __init__(self, model_class, objects_list):
        self.models_class = model_class
        self.__objects = objects_list


    def __getitem__(self, item):
        return self.__objects[item]

