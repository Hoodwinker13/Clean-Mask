import os


class Config:
    DEBUG = False


class DevelopmentConfig(Config):
    DEBUG = True
    CORS = {r'*':{'origins':'*'}}
    HOST = "127.0.0.1"
    PORT = "5000"

    ES_HOST = "http://localhost:9200"
    INDEX_NAME = "mask"
    DOC_TYPE = "mask_data"

    FILE_PATH = os.path.join(os.path.dirname(__file__), 'static')


class ProductionConfig(Config):
    DEBUG = False
    CORS = {r'*':{'origins':'*'}}
    HOST = "0.0.0.0"
    PORT = "5000"

    ES_HOST = "http://localhost:9200"


config_by_name = {
    "dev": DevelopmentConfig,
    "prod": ProductionConfig,
}