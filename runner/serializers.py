def arg_dict_serializer(arg_dict):
    sorted_kv_pairs = sorted(arg_dict.items())
    return ','.join(
        f'{_serializer(key)}:{_serializer(value)}'
        for key, value in sorted_kv_pairs
    )


def _serializer(obj):
    if hasattr(obj, '__name__'):
        if hasattr(obj, '__module__'):
            return f'{obj.__module__}.{obj.__name__}'
        return obj.__name__
    return repr(obj)
