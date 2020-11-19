def obj_mapper(obj, key_info):
    """
    Uses information provided from key_info to create and return a new object.

    :param obj: a dict representing an object
    :param key_info: a list of dicts containing information about the keys needed from the obj. Dicts in this list
        should be formatted as follows:
            {
                'name': string - the name of the key that will be mapped from obj to the new one,
                'formatted': function - a method that gets executed on the value of the obj key,
                'default': the value of the key if it was not found in the original obj
            }
    :return: a new, thinner object dict
    """

    res = {}

    # populate the event with relevant keys
    for k in key_info:
        key_name = k['name']
        out_obj = obj.get(key_name, None)

        if out_obj is None:
            # set default value if no event value
            if 'default' in k:
                out_obj = k['default']

        else:
            # run the event value through the formatter
            if 'formatter' in k:
                out_obj = k['formatter'](out_obj)

        res[key_name] = out_obj

    return res


