from sklearn.cluster import KMeans

import numpy as np

class KMean:
    
    def __init__(self, data):
        self.data = data
        self.epsilon = 1e-6

    def create_mapping(self):
        self.dist_map = {}
        for route in self.data:
            length = route.length 
            while length in self.dist_map:
                length += self.epsilon
            self.dist_map[length] = route
        return np.array(list(self.dist_map.keys()))

    def cluster(self):
        num_clusters = 15
        clusterable_data = self.create_mapping()
        kmeans = KMeans(n_clusters=num_clusters, random_state=0).fit(clusterable_data.reshape(-1,1))
        labels = kmeans.labels_

        tmp_dict = {}
        for i in range(0, len(labels)):
            label = labels[i]
            key = clusterable_data[i]
            route = self.dist_map[key]
            if label not in tmp_dict:
                tmp_dict[label] = []
            tmp_dict[label].append(route)

        return list(tmp_dict.values())

