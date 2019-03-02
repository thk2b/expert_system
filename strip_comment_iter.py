class strip_comment_iter:
    def __init__(self, it):
        self.it = it

    def __next__(self):
        while True:
            s = next(self.it).split('#', 1)[0].strip()
            if len(s):
                break
        return s

    def __iter__(self):
        return self
