import json


class Map(dict):
    """
    Example:
    m = Map({'first_name': 'Eduardo'}, last_name='Pool', age=24, sports=['Soccer'])
    """
    def __init__(self, *args, **kwargs):

        super(Map, self).__init__(*args, **kwargs)
        for arg in args:
            if isinstance(arg, dict):
                for k, v in arg.items():
                    self[k] = v

        if kwargs:
            for k, v in kwargs.items():
                self[k] = v

    def __getattr__(self, attr):
        return self.get(attr)

    def __setattr__(self, key, value):
        self.__setitem__(key, value)

    def __setitem__(self, key, value):
        super(Map, self).__setitem__(key, value)
        self.__dict__.update({key: value})

    def __delattr__(self, item):
        self.__delitem__(item)

    def __delitem__(self, key):
        super(Map, self).__delitem__(key)
        del self.__dict__[key]


class Metadata(Map):
    """
    Metadata that can be stored for your model.
    """
    def __setitem__(self, key, value):
        try:
            if len(self) == 6:
                raise Exception('Metadata items limit exceeded. Max allowed is 6.')
            elif len(key) > 20:
                raise Exception('Maximum metadata key characters of 20 exceeded. Your key has {} characters'.format(len(key)))
            elif len(json.dumps(value)) > 50:
                raise Exception('Maximum metadata value characters of 50 exceeded. Your value has {} characters'.format(len(json.dumps(value))))
            json.dumps(key)
            json.dumps(value)
        except Exception as e:
            raise Exception(e)
        super(Metadata, self).__setitem__(key, value)

    def __delitem__(self, key):
        super(Metadata, self).__delitem__(key)
