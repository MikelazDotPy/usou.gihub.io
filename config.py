import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECURITY_PASSWORD_SALT = 'my_precious_two'
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True

    # gmail authentication
    MAIL_USERNAME ='onextopplay@gmail.com'
    MAIL_PASSWORD ='muhamad12345'

    # mail accounts
    MAIL_DEFAULT_SENDER = 'onextopplay@gmail.com'