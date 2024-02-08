#!/usr/bin/env python
#
# First Steps in Programming a Humanoid AI Robot
#
# History class
# Maintain a weighted average
#

# Import required modules
import numpy as np

class History:
    def __init__(self, dim, weights):
        length = len(weights)

        # create empty list of data and weights with 'dim' dimensions
        self.data = []
        self.weights = []
        z = np.zeros((dim, 1))
        w = np.empty((dim,1))
        for weight in weights:
            w.fill(weight)
            self.data.append(z)
            self.weights.append(w)

        #print("History():\n"
        #      "data:\n{}\n"
        #      "weights:\n{}\n"
        #      .format(self.data, self.weights))

        # initialize average to allow calling average() right from the start
        self.weighted_average = np.zeros((dim, 1))

    def dump(self):
        print("History():\n"
              "data:\n{}\n"
              "weights:\n{}\n"
              "average:\n{}\n\n"
              .format(self.data, self.weights, self.weighted_average))

    def add(self, data_point):
        #print("add()\ndata_point = {}\n\n".format(data_point))
        self.data.pop()
        self.data.insert(0, data_point)

        self.weighted_average = np.average(self.data, axis=0, weights=self.weights)

    def average(self):
        return self.weighted_average


