import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or '@£$£^$%*%^(£%$£)'
    SG_KEY = os.environ.get('SENDGRID_API_KEY') or None

    # DATABASE SET UP #
    ENV = 'dev:sqlite'

    if ENV == 'dev:psql':
        SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:prologe@localhost/ml_driving'
    elif ENV == 'dev:sqlite':
        SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                'sqlite:///' + os.path.join(basedir, 'data.db')
    else:
        SQLALCHEMY_DATABASE_URI = 'postgres://wilrymijbtojcd:f47198'\
                    '586c695e41a9a0a011ca7b63da1ad53bdad197e23ac3467fb1d7c42b27@e'\
                    'c2-54-72-155-238.eu-west-1.compute.amazonaws.com:5432/db29ru'\
                    'bk7dkln5'

    SQLALCHEMY_TRACK_MODIFICATIONS = False
