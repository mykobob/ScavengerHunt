from sklearn.cluster import KMeans

from collections import defaultdict
import numpy as np

class KMean:
    
    def __init__(self, data):
        self.data = data
        self.epsilon = 1e-6

    def create_mapping(self):
        highest_key_map = {}
        self.dist_map = {}
        for route in self.data:
            length = route.length

            largest_length = highest_key_map.get(length)
            if largest_length is None:
                largest_length = length + self.epsilon
            else:
                largest_length += self.epsilon
            highest_key_map[length] = largest_length

            self.dist_map[largest_length] = route
        return np.array(list(self.dist_map.keys()))

    def cluster(self):
        num_clusters = 1
        clusterable_data = self.create_mapping()
        kmeans = KMeans(n_clusters=num_clusters, random_state=0).fit(clusterable_data.reshape(-1,1))
        labels = kmeans.labels_

        tmp_dict = defaultdict(list)
        for i in range(0, len(labels)):
            label = labels[i]
            key = clusterable_data[i]
            route = self.dist_map[key]
            tmp_dict[label].append(route)

        return list(tmp_dict.values())

