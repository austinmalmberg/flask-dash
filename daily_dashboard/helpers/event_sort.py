
def sort_events(comparator, list_a, list_b):
    """
    Combines two sorted arrays so that they remain sorted.
    
    :param comparator: A comparator method that returns -1, 0, or 1 when list_a[i] is less than, equal to, or greater
        than list_b[j], respectively.
    :param list_a: A sorted list
    :param list_b: A sorted list
    :return: A new sorted list derived from list_a and list_b
    """
    i = 0   # the index of list_a
    j = 0   # the index of list_b

    res = []

    while i < len(list_a) and j < len(list_b):
        if comparator(list_a[i], list_b[j]) <= 0:
            res.append(list_a[i])
            i += 1
        else:
            res.append(list_b[j])
            j += 1

    res += list_a[i:]
    res += list_b[j:]

    return res
