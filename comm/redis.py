import redis
import pickle
from datetime import datetime

from api.blueprints import utils as api_tools
from utility.dataclass import Environment as data_env


class RedisWrapper:
    def connect(self):
        connection_pool = redis.ConnectionPool(host="127.0.0.1", port=6379, db=0)
        return redis.StrictRedis(connection_pool=connection_pool)


def get_redis(key):
    redis = RedisWrapper().connect()
    r = redis.get(key)
    if r is None:
        # TODO: Delete redis and see if this is working or not?
        if key == "environment":
            config = api_tools.get_config()
            if not config:
                config = api_tools.new_config()
            update_redis(key, config)
            get_redis(key)
            
    return pickle.loads(r)


def set_redis(key, obj):
    redis = RedisWrapper().connect()
    redis.set(key, pickle.dumps(obj))


def update_redis(key, data):
    r_data = None

    if key == "environment":
        r_data = data_env()
        for k, v in data.items():
            if hasattr(r_data, k):
                try:
                    v = datetime.strptime(v, "%H:%M:%S").time()
                except Exception as e:
                    pass
                setattr(r_data, k, v)
        
    if r_data is not None:
        set_redis(key, r_data)
