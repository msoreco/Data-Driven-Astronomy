import numpy as np

#
# Function median_diff
#
# Calculates median of differences between predicted and actual values.
#
# args:
#   predicted - numpy array representing predicted values
#   actual - numpy array of actual values
#
# return:
#   the median difference
#
def median_diff(predicted, actual):
    return np.median(abs(predicted - actual))

#
# Function get_features_targets
#
# Extracts features and target redshift values from raw data.
#
# args:
#   data - raw array of galaxy color data
#
# return:
#   numpy array containing the following columns:
#       0:  u - g color index
#       0:  g - r color index
#       0:  r - i color index
#       0:  i - z color index
#       0:  actual redshift values
#
def get_features_targets(data):
    ug = data['u'] - data['g']
    gr = data['g'] - data['r']
    ri = data['r'] - data['i']
    iz = data['i'] - data['z']
    return np.array([ug, gr, ri, iz]).T, data['redshift']
