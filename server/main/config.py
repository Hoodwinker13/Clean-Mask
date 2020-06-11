import os


class Config:
    DEBUG = False


class DevelopmentConfig(Config):
    DEBUG = True
    CORS = {r'*':{'origins':'*'}}
    HOST = "127.0.0.1"
    PORT = "5000"

    ES_HOST = "http://localhost:9200"
    
    ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
    FILE_PATH = os.path.join(ROOT_DIR, 'static/img')


class ProductionConfig(Config):
    DEBUG = False
    CORS = {r'*':{'origins':'*'}}
    HOST = "0.0.0.0"
    PORT = "5000"

    ES_HOST = "http://localhost:9200"

    ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
    FILE_PATH = os.path.join(ROOT_DIR, 'static/img')


config_by_name = {
    "dev": DevelopmentConfig,
    "prod": ProductionConfig,
}