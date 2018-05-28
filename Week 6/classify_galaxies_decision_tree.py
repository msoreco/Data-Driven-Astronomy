import numpy as np
from sklearn.tree import DecisionTreeClassifier
from wk6_common import generate_features_targets

#
# Function splitdata_train_test
#
# Splits a numpy array of data into training and testing sets, with
# a specified fraction of the data in the training set.
#
# args:
#   data - numpy array of training data
#   fraction_training - fraction of data for training (btwn 0.0 and 1.0)
#
# returns:
#   training_set
#   testing_set
#
def splitdata_train_test(data, fraction_training):
    
    # Shuffle data
    np.random.seed(0)
    shuffled = np.random.shuffle(data)
    
    # Calculate number of training instances
    train_count = int(len(data) * fraction_training)

    # Split data
    training_set = data[:train_count]
    testing_set = data[train_count:]
        
    return training_set, testing_set

#
# Function dtc_predict_actual
#
# Given numpy array of Galaxy Zoo Project data, splits the data into
# training and testing sets, trains a decision tree model on the training
# data, then calculates predicted labels for the testing set.
#
# args:
#   data - numpy array of SDSS data
#
# returns:
#   predictions - array of predicted labels for each galaxy
#   test_targets - array of true labels for each galaxy
#
def dtc_predict_actual(data):
    
    # Split the data into training and testing sets (training fraction of 0.7)
    training_set, testing_set = splitdata_train_test(data, 0.7)

    # Generate the feature and targets for the training and test sets
    train_features, train_targets = generate_features_targets(training_set)
    test_features, test_targets = generate_features_targets(testing_set)
        
    # Train a DecisionTreeClassifier model
    dtc = DecisionTreeClassifier()
    dtc.fit(train_features, train_targets)

    # get predictions for the test_features
    predictions = dtc.predict(test_features)
            
    # return the predictions and the test_targets
    return predictions, test_targets

#
# Run example
#
if __name__ == '__main__':
    data = np.load('data/galaxy_catalogue.npy')
    predicted_class, actual_class = dtc_predict_actual(data)
    print("Some initial results...\n   predicted,  actual")
    for i in range(10):
        print("{}. {}, {}".format(i, predicted_class[i], actual_class[i]))
