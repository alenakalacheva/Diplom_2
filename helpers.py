from faker import Faker



class User:
    """Методы генерации данных для регистрации"""

    @staticmethod
    def create_correct_user_data():
        faker = Faker('ru_RU')
        data = {
            "email": faker.email(),
            "password": faker.password(),
            "name": faker.first_name()
        }
        return data

    @staticmethod
    def create_user_data_without_name():
        faker = Faker('ru_RU')
        data = {
            "email": faker.email(),
            "password": faker.password(),
        }
        return data

    @staticmethod
    def create_user_data_without_email():
        faker = Faker('ru_RU')
        data = {
            "password": faker.password(),
            "name": faker.first_name()
        }
        return data

    @staticmethod
    def create_user_data_without_password():
        faker = Faker('ru_RU')
        data = {
            "email": faker.email(),
            "name": faker.first_name()
        }
        return data


