class Config(object):
    ETL_SERVER = 'data.feidee.net'
    ETL_SERVER_URL = 'http://data.feidee.net/logCollect/collectByPost'
    ETL_SERVER_URL_TAIL = '/logCollect/collectByPost'
    ETL_SERVER_URL_TAIL_BATCH = '/logCollect/batchEventCollect'
    SENDCLOUD_APP_KEY = 'm3lh7hv6-3aab-ifuj-4as7-7dzv58f0q0'
    MQ_SIZE = 200000
    DEBUG = False
    HTTP_CONNECTION_POOL_SIZE = 50

class ReleaseConfig(Config):
    DEBUG = False

class TestingConfig(Config):
    DEBUG = True

class DockerConfig(Config):
    #REDIS_SERVER = os.environ.get('REDIS_SERVER')
    #ELASTICSEARCH_SERVER = [os.environ.get('ELASTICSEARCH_SERVER')]
    #REDIS_SERVER_PORT = 6379
    DEBUG = False
