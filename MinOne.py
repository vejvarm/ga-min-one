class MinOne:

    def __init__(self):
        pass

    def __call__(self, x, *args, **kwargs):
        return sum(x)


if __name__ == '__main__':
    xes = (1, 0, 0, 1, 1)
    mo = MinOne()

    print(mo(xes))
