class Location:
    def __init__(self, name):
        self.name = name
        self.nbors = {}

    def add_nbor(self, nbor, dist):
        self.nbors[nbor] = dist

    def get_dist(self, other):
        return self.nbors[nbor]

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return (self.name) == (other.name)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name
