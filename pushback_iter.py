import collections

class pushback_iter:
    """
    Wraps an iterable to allow pushing back previous values
    """
    def __init__(self, it):
        self.it = it
        self.buffer = collections.deque()

    def __next__(self):
        if len(self.buffer):
            return self.buffer.pop()
        return next(self.it)

    def __iter__(self):
        return self

    def push(self, line):
        self.buffer.append(line)

if __name__ == '__main__':
    again = False
    with open('a', 'r') as f:
        i = pushback_iter(f)
        for line in i:
            if line[0] == 'd' and not again:
                again = True
                i.push(line)
            print(line, end='')
