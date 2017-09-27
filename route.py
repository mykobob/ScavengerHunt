class Route:
    def __init__(self, route=None):
        self.locations_order = [] if route is None else list(route)
        self.length = sum(x.nbors[y] for x,y in zip(self.locations_order, self.locations_order[1:]))

    def remove_last(self):
        del self.locations_order[-1]

    def __str__(self):
        return "Length: {}. {}".format(str(self.length), " -> ".join([str(loc) for loc in self.locations_order]))

    def __repr__(self):
        return str(self)

