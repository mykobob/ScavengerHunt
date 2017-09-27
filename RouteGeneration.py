import itertools
import numpy as np

from kmeans import KMean

from location import Location
from route import Route

class RouteGeneration:
    def __init__(self):
        self.locations = self.parse_input_data()

    def parse_input_data(self):
        num_locations = int(input().strip())
        locations_dict = {}
        for i in range(0, num_locations):
            name = input().strip()
            locations_dict[name] = Location(name)

        for i in range(0, num_locations * (num_locations - 1) // 2):
            data = input().strip().split(',')
            src = locations_dict[data[0]]
            dest = locations_dict[data[1]]
            dist = float(data[2])
            src.add_nbor(dest, dist)
            dest.add_nbor(src, dist)
        
        return list(locations_dict.values())

    def generate_routes(self, num_routes):
        all_perms = [Route(x) for x in itertools.permutations(self.locations)] 
        clusters = KMean(all_perms).cluster()
        max_variance = [str(max(cluster, key=lambda route: route.length).length - min(cluster, key=lambda route: route.length).length) for cluster in clusters]
        print('\n'.join(max_variance))
        return clusters

    def solve(self):
        route_perms = self.generate_routes(16)
        print('\n\n\n'.join(['    ' + '\n    '.join([str(loc) for loc in perm]) for perm in route_perms]))

if __name__ == '__main__':
    RouteGeneration().solve()
