from functools import reduce


def map_reduce(map_function, lst):
    """
    Implementation of map-reduce where the reduce is /a b -> a+b
    :param map_function: the function that is applied on every element of list before reduction
    :param lst: the non-empty list to be map-reduced
    :return: map-reduced list
    """
    if not lst:
        raise Exception("lst can not be empty")
    return reduce(lambda a, b: a + b, map(map_function, lst))


def denormalize(center):
    """
    Denormalize a center entry by geo field.
    So if a center has three geo entries, this function returns a list of three centers with one geo entry each.
    :param center: a professional help center as found in data.yaml
    :return: center in a denormalized form
    """
    result = []
    for location in center["geo"]:
        center_copy = center.copy()
        del center_copy["geo"]
        center_copy["country"] = location["country"]
        center_copy["geo"] = {"lat": location["lat"], "long": location["long"]}
        result.append(center_copy)

    return result
