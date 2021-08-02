def dot(a, b):
    return [i*j for i, j in zip(a, b)]


def element_sum(a, b):
    return [i+j for i, j in zip(a, b)]


def cumsum(lst):
    l2 = [lst[0], ]
    for val in lst[1:]:
        l2.append(l2[-1] + val)

    return l2