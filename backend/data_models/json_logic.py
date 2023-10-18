from typing import Union


class JsonSerializable:
    """
        A class that can be serialized to json
    """

    def _toJson(self, obj):
        """
            Converts a object to Json.
        """
        if isinstance(obj, JsonSerializable):
            return obj.toJson()
        elif isinstance(obj, list):
            return [self._toJson(entry) for entry in obj]
        elif isinstance(obj, dict):
            return {k: self._toJson(v) for k, v in obj.items()}
        else:
            return obj

    def toJson(self):
        output = {}
        for k, v in self.__dict__.items():
            if not k.startswith("_") and not callable(v):
                output[k] = self._toJson(v)
        return output

    def __repr__(self):
        return str(self.toJson())


class JsonInitializable (JsonSerializable):
    """
        A class that can be initialized from a json object by passing it the object's dictionary representation.
        The class constructor must allow for no arguments to be passed, along with *args and **kwargs, this is to allow for dictionary splatting to intialize the object.
        Constructors used to perform validation.
    """
    @classmethod
    def from_object(self, arg: Union[dict, "JsonSerializable"]):
        if isinstance(arg, dict):
            return self(**arg)
        elif isinstance(arg, self):
            return arg
        else:
            raise TypeError(f"Trying to initialize with unusable type. Recieved {type(arg)}. Arg is {arg}")