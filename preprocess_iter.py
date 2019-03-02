class preprocess_iter:
    def __init__(self, it, prompt=False):
        self.it = it
        self.prompt = prompt

    def __next__(self):
        while True:
            if self.prompt:
                print(self.prompt, end='', flush=True)
            s = next(self.it).split('#', 1)[0].strip()
            if len(s):
                break
        return s

    def __iter__(self):
        return self
