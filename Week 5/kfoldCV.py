import numpy as np
from matplotlib import pyplot as plt
from sklearn.model_selection import KFold
from sklearn.tree import DecisionTreeRegressor
from wk5_common import median_diff, get_features_targets

#
# Function cross_validate_predictions
#
# Performs k-fold cross-validation using the given model, features, targets and number of folds.
#
# args:
#   model - the model to be trained
#   features - the features to train on
#   targets - actual redshift values
#   k - the number of cross-validation sets to use
#
# return:
#
def cross_validate_predictions(model, features, targets, k):
    
    # Split and shuffle data
    kf = KFold(n_splits=k, shuffle=True)
    
    # Declare an array for predicted redshifts from each iteration
    all_predictions = np.zeros_like(targets)

    # Perform cross-validation
    for train_indices, test_indices in kf.split(features):
        
        # Split the data into training and testing
        training_features = features[train_indices]
        training_targets = targets[train_indices]
        test_features = features[test_indices]
        test_targets = targets[test_indices]

        # Fit the model for the current set
        model.fit(training_features, training_targets)
        
        # Predict using the model
        predictions = model.predict(test_features)
        
        # Put the predicted values in the all_predictions array defined above
        all_predictions[test_indices] = predictions
            
    # return the predictions
    return all_predictions


#
# Train model, make predictions, print median difference between predicted and actual redshifts
# and plot results.
#
if __name__ == "__main__":
    data = np.load('data/sdss_galaxy_colors.npy')
    features, targets = get_features_targets(data)

    # Initialize model
    dtr = DecisionTreeRegressor(max_depth=19)
        
    # Call your cross validation function
    predictions = cross_validate_predictions(dtr, features, targets, 10)

    # Calculate and print the rmsd as a sanity check
    diffs = median_diff(predictions, targets)
    print('Median difference: {:.3f}'.format(diffs))
        
    # Plot the results to see how well our model looks
    plt.scatter(targets, predictions, s=0.4)
    plt.xlim((0, targets.max()))
    plt.ylim((0, predictions.max()))
    plt.xlabel('Measured Redshift')
    plt.ylabel('Predicted Redshift')
    plt.show()
