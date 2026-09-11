import random

class Person:
    _counter = 0

    def __init__(self, age, masked, vaccinated, status, x=None, y=None):
        self.id = Person._counter
        Person._counter += 1

        self.age = age
        self.masked = masked
        self.vaccinated = vaccinated
        self.status = status
        self.x = x if x is not None else random.randint(0, 500)
        self.y = y if y is not None else random.randint(0, 500)
        self.beta = self._calculate_beta()

    def _calculate_beta(self):
        beta = 0.3
        if self.masked == 'Yes':
            beta *= 0.7
        if self.vaccinated == 'Yes':
            beta *= 0.5
        if self.age > 60:
            beta *= 1.3
        return beta

    def __lt__(self, other):
        # Priority for vaccination: older and unvaccinated first
        return (not self.vaccinated, -self.age) < (not other.vaccinated, -other.age)
