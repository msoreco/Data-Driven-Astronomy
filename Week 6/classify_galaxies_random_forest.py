import numpy as np
from matplotlib import pyplot as plt
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import cross_val_predict
from sklearn.ensemble import RandomForestClassifier
from support_functions import generate_features_targets, plot_confusion_matrix, calculate_accuracy
from wk6_common import generate_features_targets

#
# Function rf_predict_actual
#
# Creates and trains a random forest classifier for galaxies, and
# predicts labels for a test data set
#
# args:
#   data - numpy array of Galaxy Zoo Project data
#   n_estimators - number of trees to train in random forest
#
# returns:
#   predictions - predicted galaxy labels (Elliptical, Spiral, Merged)
#   actual_labels - true galaxy labels
#
def rf_predict_actual(data, n_estimators):
    
    # Generate the features and targets
    features, targets = generate_features_targets(data)

    # Instantiate a random forest classifier using n estimators
    rfc = RandomForestClassifier(n_estimators=n_estimators)
    
    # Get predictions using 10-fold cross validation with cross_val_predict
    predictions = cross_val_predict(rfc, features, targets, cv=10)
        
    # Return the predictions and their actual classes
    return predictions, targets

#
# Run example
#
if __name__ == "__main__":
    
    # Load galaxy data
    data = np.load('data/galaxy_catalogue.npy')

    # Set number of trees to use in random forest
    number_estimators = 50
    
    # Get predicted and actual galaxy categories
    predicted, actual = rf_predict_actual(data, number_estimators)
    
    # Calculate the model score using your function
    accuracy = calculate_accuracy(predicted, actual)
    print("Accuracy score:", accuracy)
        
    # Calculate the models confusion matrix using sklearns confusion_matrix function
    class_labels = list(set(actual))
    model_cm = confusion_matrix(y_true=actual, y_pred=predicted, labels=class_labels)
            
    # Plot the confusion matrix using the provided functions.
    plt.figure()
    plot_confusion_matrix(model_cm, classes=class_labels, normalize=False)
    plt.show()


