

class MegaSenaResult():

    n = None
    dt = None
    numbers = None

    def __init__(self, n, dt, numbers):
        self.n = n
        self.dt = dt
        self.numbers = [int(n) for n in numbers]


class MegasenaResultsAnalyzer:

    results = []

    def __init__(self):
        self.results = []

    def add_result(self, result):
        self.results.append(result)