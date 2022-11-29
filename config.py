import os


class Config(object):
    DEBUG=True

    SQLALCHEMY_ECHO=True
    SQLALCHEMY_DATABASE_URI=os.getenv('DB_URL_MYDB')

    SECRET_KEY=os.getenv('APP_SECRET_KEY')

    S3_BUCKET=os.getenv('S3_BUCKET_DS')
    S3_KEY=os.getenv('AWS_KEY')
    S3_SECRET=os.getenv('AWS_SECRET_KEY')
    S3_LOCATION=os.getenv('S3_BUCKET_URI_DS')

    SERIALIZER_SECRET_KEY = os.getenv('SERIALIZER_SECRET_KEY')
    SERIALIZER_SALT = os.getenv('SERIALIZER_SALT')


class Prod(Config):
    DEBUG=False



