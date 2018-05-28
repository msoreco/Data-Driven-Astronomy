import numpy as np
from sklearn.tree import DecisionTreeRegressor
from wk5_common import median_diff, get_features_targets

#
# Function validate_model
#
# Splits the data into training and testing subsets, trains the model and
# returns the prediction accuracy with median_diff.
#
# args:
#   model - The model to be used for training/prediction of redshift values
#   features - the features to train on
#   targets - the actual redshift values
#
# return:
#   the median difference between the predicted and actual redshifts
#
def validate_model(model, features, targets):
    
    # split the data into training and testing features and predictions
    split = features.shape[0]//2
    train_features = features[:split]
    train_targets = targets[:split]
    test_features = features[split:]
    test_targets = targets[split:]

    # train the model
    model.fit(train_features, train_targets)
        
    # get the predicted_redshifts
    predictions = model.predict(test_features)
    
    # use median_diff function to calculate the accuracy
    return median_diff(test_targets, predictions)


if __name__ == "__main__":
    data = np.load('data/sdss_galaxy_colors.npy')
    features, targets = get_features_targets(data)

    # initialize model
    dtr = DecisionTreeRegressor()
        
    # validate the model and print the med_diff
    diff = validate_model(dtr, features, targets)
    print('Median difference: {:f}'.format(diff))


