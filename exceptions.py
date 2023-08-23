class FieldError(Exception):

    def __init__(self, msg):
        self.mgs = msg

    def __repr__(self):
        return "Ошибка поля(%s)" % self.mgs

    def __str__(self):
        return "Ошибка поля(%s)" % self.mgs


class FieldTypeError(FieldError):

    def __init__(self,obj_1, obj_2, operation):
        self.mgs = f"'{operation}' not supported between instances of '{obj_1.__class__.__name__}' and '{obj_2.__class__.__name__}"



class ValidationError(Exception):
    def __init__(self, msg):
        self.mgs = msg

    def __repr__(self):
        return "Ошибка Валидации(%s)" % self.mgs

