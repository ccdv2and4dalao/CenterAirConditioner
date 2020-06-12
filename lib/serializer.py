import json
from abc import abstractmethod


class Serializer(object):

    @abstractmethod
    def serialize(self, obj: object) -> str:
        pass


def to_json_std(obj: object) -> str:
    if type(obj) is dict: 
        return json.dumps(obj, ensure_ascii=False)
    else: 
        return json.dumps(obj.__dict__, ensure_ascii=False)


class JSONSerializer(Serializer):
    def serialize(self, obj: object) -> str:
        return to_json_std(obj)
