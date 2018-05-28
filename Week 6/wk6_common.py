import numpy as np

#
# Function generate_features_targets
#
# Given numpy array of data creates an array of target values and
# a matrix of training instances and their features.
#
# args:
#   data - numpy array of data
#
# returns:
#   features - matrix of features for training
#   targets - array of training target labels
#
def generate_features_targets(data):
    
    targets = data['class']

    features = np.empty(shape=(len(data), 13))
    features[:, 0] = data['u-g']
    features[:, 1] = data['g-r']
    features[:, 2] = data['r-i']
    features[:, 3] = data['i-z']
    features[:, 4] = data['ecc']
    features[:, 5] = data['m4_u']
    features[:, 6] = data['m4_g']
    features[:, 7] = data['m4_r']
    features[:, 8] = data['m4_i']
    features[:, 9] = data['m4_z']
    features[:, 10] = data['petroR50_u'] / data['petroR90_u']
    features[:, 11] = data['petroR50_r'] / data['petroR90_r']
    features[:, 12] = data['petroR50_z'] / data['petroR90_z']
    
    return features, targets
