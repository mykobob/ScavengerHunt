from collections import defaultdict
import random
import itertools
import numpy as np

from kmeans import KMean

from location import Location
from route import Route

START_END_POINT = '405'

class RouteGeneration:
    def __init__(self):
        self.locations = self.parse_input_data()

    def parse_input_data(self):
        self.num_locations = int(input().strip())
        locations_dict = {}
        for i in range(0, self.num_locations):
            name = input().strip()
            locations_dict[name] = Location(name)

        for i in range(0, self.num_locations * (self.num_locations - 1) // 2):
            data = input().strip().split(',')
            src = locations_dict[data[0]]
            dest = locations_dict[data[1]]
            dist = float(data[2])
            src.add_nbor(dest, dist)
            dest.add_nbor(src, dist)
        
        return locations_dict

    def destination_locations(self):
        return [location for name, location in self.locations.items() if name != START_END_POINT] 

    def valid_destination_locations(self, location_count):
        # We subtract one to ignore the beginning location
        return self.num_locations - 1 == location_count

    def two_starting_locs(self, cluster):
        starting_loc = defaultdict(int)
        names = set()
        for route in cluster:
            starting_loc[route.start_loc().name] += 1
            names.add(route.start_loc().name)

        return self.valid_destination_locations(len(names)) and not any(starting_count < 2 for starting_count in starting_loc.values()) 

    def matching_locations(self, valid_routes, route_in_question):
        for valid_route in valid_routes:
            for i in range(1, len(valid_route.locations_order) - 2):
                if route_in_question[i] == valid_route[i] and route_in_question[i + 1] == valid_route[i + 1]:
                    return True
        return False
        # return any(route_in_question[i] == route[i] and route_in_question[i + 1] == route[i + 1] for route in valid_routes for i in range(1, route.length - 1))

    def more_than_two_per_loc(self, routes):
        index_count = defaultdict(lambda : defaultdict(int))
        for route in routes:
            for i in range(1, len(route.locations_order) - 2):
                index_count[i][route[i].name] += 1

        return len(index_count) > 0 and any(count > 2 for k, name_count in index_count.items() for name, count in name_count.items())

    # Given num_routes and a cluster, grab num_routes number of routes
    def get_num_routes(self, num_routes, cluster):
        selected = []
        beginning_locs = defaultdict(int)
        index = 0
        random.shuffle(cluster)
        while index < len(cluster) and len(selected) < num_routes:
            while index < len(cluster) and (beginning_locs[cluster[index].start_loc().name] >= 2 or self.matching_locations(selected, cluster[index]) or self.more_than_two_per_loc(selected)):
                # print(beginning_locs[cluster[index].start_loc().name] >= 2, self.matching_locations(selected, cluster[index]), self.more_than_two_per_loc(selected))
                index += 1
            if index != len(cluster):
                selected.append(cluster[index])
                beginning_locs[cluster[index].start_loc().name] += 1
            index += 1

        return selected

    def get_good_clusters(self, num_routes, clusters):
        good = []
        for cluster in clusters:
            valid_routes = self.get_num_routes(num_routes, cluster)
            while len(valid_routes) < num_routes:
                valid_routes = self.get_num_routes(num_routes, cluster)
            good.append(valid_routes)
        return good

    def apply_filters(self, num_routes, clusters):
        # There needs to be enough things in the cluster to be use for routes
        clusters = list(filter(lambda cluster: len(cluster) >= num_routes, clusters))
        print('    finished basic filtering')

        # There can only exist two routes with the same starting place
        clusters = list(filter(self.two_starting_locs, clusters))
        print('    finished same source nodes')

        # No two routes can have a location in the same position and lead to the next same location
        # Select 16 routes in each cluster that satisfy above condition
        clusters = self.get_good_clusters(num_routes, clusters)
        print('    get good clusters')

        return clusters

    def generate_routes(self, num_routes):
        all_perms = [Route(x).add_endpoints(self.locations[START_END_POINT]) for x in itertools.permutations(self.destination_locations())] 
        print('Finished generating all permutations')

        clusters = KMean(all_perms).cluster()
        print('Finished clustering')

        filtered_data = self.apply_filters(num_routes, clusters)
        print('Finished filters')

        return filtered_data

    def solve(self):
        route_perms = self.generate_routes(10)
        print('\n\n\n'.join(['    ' + '\n    '.join([str(loc) for loc in perm]) for perm in route_perms]))
        print('   diff between max and min {0:.2f}-{1:.2f}={2:.2f}'.format(max(route.length for perm in route_perms for route in perm), min(route.length for perm in route_perms for route in perm), max(route.length for perm in route_perms for route in perm) - min(route.length for perm in route_perms for route in perm)))

if __name__ == '__main__':
    RouteGeneration().solve()
