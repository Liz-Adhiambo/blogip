import os


class Config:
    SECRET_KEY = '5791628bb0b13ce0c676dfde280ba24578ik'
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://liz:1234@localhost/bloglist'
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'lizcreatesapps'
    MAIL_PASSWORD = 'creatingapps123'