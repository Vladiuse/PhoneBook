from main import PhoneRecord

def clean_phone(phone):
    # подчищаю номер телефона от Faker от невалидных символов
    return ''.join(char for char in phone if char.isdigit())


def seed_db(count=10):
    # Заподнить базу данных фейковыми значениями
    from faker import Faker
    faker = Faker('ru')
    for _ in range(count):
        phone = PhoneRecord(
            first_name=faker.first_name(),
            last_name=faker.last_name(),
            sur_name=faker.middle_name(),
            organization_name=faker.company(),
            phone=clean_phone(faker.phone_number()),
            work_phone=clean_phone(faker.phone_number()),
        )
        if phone.is_valid():
            phone.save()
        else:
            print(phone)
            raise ZeroDivisionError

seed_db()