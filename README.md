Для запуска проекта необходимо в файле settings.py внести данные для подключения к БД по шаблону:
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'drf',
        'USER': 'postgres',
        'HOST': 'localhost',
        'PORT': 5432,
        'PASSWORD': 'user_password'

    }
}