class Map(dict):
    """
    An object that maps keys to values. A map cannot contain duplicate keys; each key can map to at most one value.
    This class is inherited from :code:`dict` class, but supporting dot notation to get the value of the key.
    """

    def __init__(self, *args, **kwargs):
        super(Map, self).__init__(*args, **kwargs)
        for arg in args:
            if isinstance(arg, dict):
                for k, v in arg.items():
                    if isinstance(v, dict):
                        v = Map(v)
                    self[k] = v
        if kwargs:
            for k, v in kwargs.items():
                self[k] = v

    def __getattr__(self, attr):
        """
        :param attr:
        :return:
        :rtype: Map
        :rtype: object
        """
        return self.get(attr)

    def __setattr__(self, key, value):
        self.__setitem__(key, value)

    def __setitem__(self, key, value):
        super(Map, self).__setitem__(key, value)
        if isinstance(value, dict):
            value = Map(value)
        self.__dict__.update({key: value})

    def __delattr__(self, item):
        self.__delitem__(item)

    def __delitem__(self, key):
        super(Map, self).__delitem__(key)
        del self.__dict__[key]

    def __repr__(self):
        def inner(d, indent=0):
            for k, v in d.items():
                if type(v) is Map:
                    s.append('{indent}{key}:\n'.format(indent='\t' * indent, key=k))
                    if inner(v, indent + 1):
                        s.append('{}\n'.format('\t' * indent))
                    continue
                s.append('{indent}{key}: {value}\n'.format(indent='\t' * indent, key=k, value=str(v)))
            return True

        s = []
        inner(self.__dict__)
        return ''.join(s)

    def get_nested_values(self):
        res = []
        for v in self.__dict__.values():
            res.append(v)
        return res.copy()


if __name__ == '__main__':
    m = Map({'first_name': 'Dan'}, last_name='Eldon', age=24, sports=['Football', 'Baseball'])

    # Add new key
    m.new_key = 'Hello world!'
    print('m.new_key:', m.new_key)

    # Update values
    m.new_key = 'Yay!'
    print('m.new_key:', m.new_key)

    # Delete key
    del m.new_key

    # Complex value
    m.dict_key = {"one": 1, "four": {"first term": 2, "second_term": 2}}
    print()
    print(m)

    # Nested values
    m.nested = Map({'a': 1, 'b': 2, 'c': 3})
    print()
    print(m.nested.get_nested_values())
