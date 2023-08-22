class FieldError(Exception):

    def __init__(self, msg):
        self.mgs = msg

    def __repr__(self):
        return "Ошибка поля(%s)" % self.mgs


class ValidationError(Exception):
    def __init__(self, msg):
        self.mgs = msg

    def __repr__(self):
        return "Ошибка Валидации(%s)" % self.mgs