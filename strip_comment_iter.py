class strip_comment_iter:
    def __init__(self, it):
        self.it = it

    def __next__(self):
       return next(self.it).split('#', 1)[0]

    def __iter__(self):
        return self
