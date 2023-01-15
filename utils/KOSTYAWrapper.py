def KostyaWrapper(cls):
    class Wrapper(cls):
        def __init__(self, *args, **kwargs):
            # super(cls, self).__init__(args, kwargs)
            # super().__init__(args,kwargs)
            # return
            if len(args) == 0:
                super(cls, self).__init__()
            if len(args) == 1:
                super(cls, self).__init__(args[0])
            if len(args) == 2:
                super(cls, self).__init__(args[0], args[1])
            if len(args) == 3:
                super(cls, self).__init__(args[0], args[1], args[2])
            if len(args) == 4:
                super(cls, self).__init__(args[0], args[1], args[2], args[3])
            if len(args) == 5:
                super(cls, self).__init__(args[0], args[1], args[2], args[3], args[4])
            if len(args) == 6:
                super(cls, self).__init__(args[0], args[1], args[2], args[3], args[4], args[5])
            if len(args) == 7:
                super(cls, self).__init__(args[0], args[1], args[2], args[3], args[4], args[5], args[6])
            if len(args) == 8:
                super(cls, self).__init__(args[0], args[1], args[2], args[3], args[4], args[5], args[6], args[7])
            if len(args) == 9:
                super(cls, self).__init__(args[0], args[1], args[2], args[3], args[4], args[5], args[6], args[7],
                                          args[8])
            if len(args) == 10:
                super(cls, self).__init__(args[0], args[1], args[2], args[3], args[4], args[5], args[6], args[7],
                                          args[8], args[9])
            super().__init__(args)

    return Wrapper
