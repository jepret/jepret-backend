import json
from redis_client import RedisClient


class RedisBaseModel:
    def __init__(self, key):
        self._key = key
        self._r = RedisClient.load()
        self._fields = []
        self.__expiry = None
        self._is_data_object = True
        self._data = None

    def _set_expiry(self, expiry: int):
        self.__expiry = expiry

    def _set_data(self, data):
        if self._is_data_object:
            self._set_data_object(data)
        else:
            self._data = data

    def _set_data_object(self, data):
        if self._data is None:
            self._data = {}

        for key in self._fields:
            if key in data:
                self._data[key] = data[key]
            else:
                raise Exception("Incomplete fields")

    def save(self):
        serializable = self._data
        serialized = json.dumps(serializable)

        return self._r.set(
            self._key + "_" + type(self).__name__, serialized, self.__expiry
        )

    def load(self):
        data = self._r.get(self._key + "_" + type(self).__name__)

        if data is None:
            return None

        data = json.loads(data)
        self._set_data(data)
        return self.data

    def delete(self):
        self._r.delete(self._key + "_" + type(self).__name__)

    def to_dict(self):
        data = {}

        for field_name in self._fields:
            data[field_name] = getattr(self, field_name)

        return data

    @property
    def data(self):
        return self._data


class Session(RedisBaseModel):
    def __init__(self, key, data=None):
        super().__init__(key)
        self._fields = ["id", "email", "name", "id_card", "phone_number"]
        if data:
            self._set_data(data)
