from validators import *
from models import Model
from models import CharField, IntegerField


class PhoneRecord(Model):
    """
    класс можели записи телефона
    """

    # fields_map - это костылек, тк не смог получить список полей без
    # вызова __init__(те создании экземпляра)
    # пришлось просто их руками записать
    fields_map = ['first_name', 'last_name', 'sur_name', 'organization_name', 'work_phone', 'phone']

    def __init__(self, first_name, last_name, sur_name,
                 organization_name, work_phone, phone, **kwargs):
        super().__init__(**kwargs)
        self.first_name = CharField(
            first_name,
            max_length=20,
            validators=[NameRegExValidator(), ],
            verbose_name='Имя',
        )
        self.last_name = CharField(
            last_name,
            max_length=20,
            validators=[NameRegExValidator(), ],
            verbose_name='Фамилия',
        )
        self.sur_name = CharField(
            sur_name,
            max_length=20,
            validators=[NameRegExValidator(), ],
        )
        self.organization_name = CharField(
            organization_name,
            max_length=50,
        )
        self.work_phone = IntegerField(
            work_phone,
            min_length=9,
            max_length=12,
            unique=True,
        )
        self.phone = IntegerField(
            phone,
            min_length=9,
            max_length=12,
            unique=True,
        )

    def __str__(self):
        return f'<PhoneRec:{self.pk}>'


PhoneRecord._set_class()  # костыль для предачи Manager текущего класса Model
