import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SSL_DISABLE = False
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
    FLASKY_MAIL_SENDER = 'Flasky Admin <flasky@example.com>'
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')
    MEDIA_FOLDER = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'data')

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    # SQLALCHEMY_DATABASE_URI = 'mysql://ionams:!2345iondbams5432!@209.97.175.39:3306/ams'
    # SQLALCHEMY_BINDS = {'users': 'mysql://ionams:!2345iondbams5432!@209.97.175.39:3306/ion'}
    SQLALCHEMY_DATABASE_URI = 'mysql://ionbiller:!2345iondbbiller5432!@209.97.175.39:3306/ams'
    SQLALCHEMY_BINDS = {
        'users': 'mysql://ionbiller:!2345iondbbiller5432!@209.97.175.39:3306/ion',
        'toll': 'mysql://ionapi:!2345iondbapi5432!@209.97.175.39:3306/rdb'
    }
    # SQLALCHEMY_DATABASE_URI = 'mysql://root:password@localhost:3306/ams'
    # SQLALCHEMY_BINDS = {'users': 'mysql://root:password@localhost:3306/ion'}
    MONGO_DBNAME = 'ion'
    MONGO_URI = 'mongodb://iondb:!2345iondb0005432!@209.97.175.39/ion'

class TestingConfig(Config):
    # TESTING = TrueSQLALCHEMY_DATABASE_URI = 'mysql://root:password@localhost/ams'
    # SQLALCHEMY_BINDS = {'users': 'mysql://root:password@localhost/ion'}
    # SQLALCHEMY_DATABASE_URI = 'mysql://ionams:!2345iondbams5432!@209.97.175.39:3306/ams'
    # SQLALCHEMY_BINDS = {'users': 'mysql://ionams:!2345iondbams5432!@209.97.175.39:3306/ion'}
    SQLALCHEMY_DATABASE_URI = 'mysql://ionbiller:!2345iondbbiller5432!@209.97.175.39:3306/ams'
    SQLALCHEMY_BINDS = {
        'users': 'mysql://ionbiller:!2345iondbbiller5432!@209.97.175.39:3306/ion',
        'toll': 'mysql://ionapi:!2345iondbapi5432!@209.97.175.39:3306/rdb'
    }
    WTF_CSRF_ENABLED = False
    MONGO_DBNAME = 'ion'
    MONGO_URI = 'mongodb://iondb:!2345iondb0005432!@209.97.175.39/ion'


class ProductionConfig(Config):
    # SQLALCHEMY_DATABASE_URI = 'mysql://root:password@localhost/ams'
    # SQLALCHEMY_BINDS = {'users': 'mysql://root:password@localhost/ion'}
    # SQLALCHEMY_DATABASE_URI = 'mysql://ionams:!2345iondbams5432!@209.97.175.39:3306/ams'
    # SQLALCHEMY_BINDS = {'users': 'mysql://ionams:!2345iondbams5432!@209.97.175.39:3306/ion'}
    SQLALCHEMY_DATABASE_URI = 'mysql://ionbiller:!2345iondbbiller5432!@209.97.175.39:3306/ams'
    SQLALCHEMY_BINDS = {
        'users': 'mysql://ionbiller:!2345iondbbiller5432!@209.97.175.39:3306/ion',
        'toll': 'mysql://ionapi:!2345iondbapi5432!@209.97.175.39:3306/rdb'
    }
    MONGO_DBNAME = 'ion'
    MONGO_URI = 'mongodb://iondb:!2345iondb0005432!@209.97.175.39/ion'

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)

        # email errors to the administrators
        import logging
        from logging.handlers import SMTPHandler
        credentials = None
        secure = None
        if getattr(cls, 'MAIL_USERNAME', None) is not None:
            credentials = (cls.MAIL_USERNAME, cls.MAIL_PASSWORD)
            if getattr(cls, 'MAIL_USE_TLS', None):
                secure = ()
        mail_handler = SMTPHandler(
            mailhost=(cls.MAIL_SERVER, cls.MAIL_PORT),
            fromaddr=cls.FLASKY_MAIL_SENDER,
            toaddrs=[cls.FLASKY_ADMIN],
            subject=cls.FLASKY_MAIL_SUBJECT_PREFIX + ' Application Error',
            credentials=credentials,
            secure=secure)
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)


class HerokuConfig(ProductionConfig):
    SSL_DISABLE = bool(os.environ.get('SSL_DISABLE'))

    @classmethod
    def init_app(cls, app):
        ProductionConfig.init_app(app)

        # handle proxy server headers
        from werkzeug.contrib.fixers import ProxyFix
        app.wsgi_app = ProxyFix(app.wsgi_app)

        # log to stderr
        import logging
        from logging import StreamHandler
        file_handler = StreamHandler()
        file_handler.setLevel(logging.WARNING)
        app.logger.addHandler(file_handler)


class UnixConfig(ProductionConfig):
    @classmethod
    def init_app(cls, app):
        ProductionConfig.init_app(app)

        # log to syslog
        import logging
        from logging.handlers import SysLogHandler
        syslog_handler = SysLogHandler()
        syslog_handler.setLevel(logging.WARNING)
        app.logger.addHandler(syslog_handler)

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'heroku': HerokuConfig,
    'unix': UnixConfig,

    'default': DevelopmentConfig
}
# use ion
# db.createUser({
# 	user: "ion",
# 	pwd: "!2345ewallet5432!",
# 	roles:
# 		[
# 		{ role: "readWrite", db: "ion" }
# 	],
#     mechanisms:[
#         "SCRAM-SHA-1"
#     ]
# })

# db.createUser({
# 	user: "ewallet",
# 	pwd: "!2345ewallet5432!",
# 	roles:
# 		[
# 		{ role: "readWrite", db: "e_wallet_test" }
# 	]
# })

# db.createUser({
# 	user: "iondb",
# 	pwd: "!2345iondb0005432!",
# 	roles:
# 		[
# 		{ role: "readWrite", db: "ion" }
# 	]
# })
