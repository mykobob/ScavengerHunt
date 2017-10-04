class Route:
    def __init__(self, route=None):
        self.locations_order = [] if route is None else list(route)
        self.length = self.calculate_length()

    def calculate_length(self):
        return int(sum(x.nbors[y] for x,y in zip(self.locations_order, self.locations_order[1:])))

    def remove_last(self):
        del self.locations_order[-1]

    def start_loc(self):
        return self.locations_order[0]

    def add_endpoints(self, location):
        self.locations_order.insert(0, location)
        self.locations_order.append(location)
        self.length = self.calculate_length()

    def __str__(self):
        return "Length: {}. {}".format(str(self.length), " -> ".join([str(loc) for loc in self.locations_order]))

    def __repr__(self):
        return str(self)

    def __getitem__(self, index):
        return self.locations_order[index]

    def __setitem__(self, index, value):
        self.locations_order[index] = value
