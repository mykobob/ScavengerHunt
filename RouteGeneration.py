from collections import defaultdict
from random import randrange
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

    def matching_locations(self, valid_routes, route_in_question):
        return any(route_in_question[i] == route[i] and route_in_question[i + 1] == route[i + 1] for route in valid_routes for i in range(route.length - 1))

    def get_num_routes(self, num_routes, cluster):
        used = [False] * len(cluster)
        selected = []
        while len(selected) < num_routes:
            index = randrange(len(cluster))
            while used[index] or self.matching_locations(selected, cluster[index]):
                index = randrange(len(cluster))
            selected.append(cluster[index])
            used[index] = True

        return selected

    def get_good_clusters(self, num_routes, clusters):
        good = []
        for cluster in clusters:
            valid_routes = self.get_num_routes(num_routes, cluster)
            if valid_routes is not None:
                good.append(valid_routes)
        return good

    def apply_filters(self, num_routes, clusters):
        # There needs to be enough things in the cluster to be use for routes
        clusters = list(filter(lambda cluster: len(cluster) >= num_routes, clusters))

        # There can only exist two routes with the same starting place
        clusters = list(filter(self.two_starting_locs, clusters))

        # No two routes can have a location in the same position and lead to the next same location
        # Select 16 routes in each cluster that satisfy above condition
        clusters = self.get_good_clusters(num_routes, clusters)

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
