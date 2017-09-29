from collections import defaultdict
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

    def two_starting_locs(self, cluster):
        starting_loc = defaultdict(int)
        names = set()
        for route in cluster:
            starting_loc[route.start_loc()] += 1
            names.add(route.start_loc().name)
        return len(names) == 8 and not any(starting_count < 2 for starting_count in starting_loc.values()) 

    def apply_filters(self, num_routes, clusters):
        print(len(clusters))
        clusters = list(filter(lambda cluster: len(cluster) >= num_routes, clusters))
        print(len(clusters))
        # There can only exist two routes with the same starting place
        clusters = list(filter(self.two_starting_locs, clusters))
        print(len(clusters))
        # No two routes can have a location in the same position and lead to the next same location

        return clusters


    def generate_routes(self, num_routes):
        all_perms = [Route(x) for x in itertools.permutations(self.locations)] 
        clusters = KMean(all_perms).cluster()

        return self.apply_filters(num_routes, clusters)

    def solve(self):
        route_perms = self.generate_routes(16)
        print('\n\n\n'.join(['    ' + '\n    '.join([str(loc) for loc in perm]) for perm in route_perms]))

if __name__ == '__main__':
    RouteGeneration().solve()
