##################################################################
# Author: edassni
# Dated: Feb 27, 2023
# Module Name: Learning System
# Copyright Ericsson 2023
##################################################################

from xml.sax.handler import feature_namespaces
from sklearn.feature_selection import SequentialFeatureSelector
from sklearn import tree,preprocessing
from sklearn.metrics import accuracy_score
from sklearn.datasets import make_blobs
from sklearn.model_selection import train_test_split
import pydotplus

def learningSystemRegressorModel(n,X,y,X_test):
    dt_reg = tree.DecisionTreeRegressor() # loading regression model:: decision tree
    sffs = SequentialFeatureSelector(dt_reg, n_features_to_select=n, direction="forward") # loading feature selection model:: sequential forward feature selection 
    X_selected = sffs.fit_transform(X, y) # selecting top n features or parameters from the given training set
    # print(X_selected)
    X_test_selected = sffs.transform(X_test) # selecting same top n features or parameters as training from the testing set
    dt_reg = dt_reg.fit(X_selected,y) # training the regression model
    y_reg_predict = dt_reg.predict(X_test_selected) # testing the regression model
    print("Predicted Regression Outcome: ", y_reg_predict) # predicted regression outcome
    return y_reg_predict

def testingPerformance(y_test, y_predict):
    perf = round(accuracy_score(y_test, y_predict)*100,2) # performance of the model computation
    print("Accuracy: ", perf) # accuracy of the model
    return perf

def decisionTreePlot(dt_clf,feature_names,target_names,samples):
    dot_data = tree.export_graphviz(dt_clf, out_file=None,
                                feature_names=feature_names,
                                class_names=target_names,
                                filled=True, rounded=True,
                                special_characters=True)
    graph = pydotplus.graph_from_dot_data(dot_data)

    # empty all nodes, i.e.set color to white and number of samples to zero
    for node in graph.get_node_list():
        if node.get_attributes().get('label') is None:
            continue
        if 'samples = ' in node.get_attributes()['label']:
            labels = node.get_attributes()['label'].split('<br/>')
            print(labels)
            for i, label in enumerate(labels):
                if label.startswith('samples = '):
                    labels[i] = 'samples = 0'
            node.set('label', '<br/>'.join(labels))
            node.set_fillcolor('white')

    decision_paths = dt_clf.decision_path(samples)

    for decision_path in decision_paths:
        for n, node_value in enumerate(decision_path.toarray()[0]):
            if node_value == 0:
                continue
            node = graph.get_node(str(n))[0]            
            node.set_fillcolor('green')
            labels = node.get_attributes()['label'].split('<br/>')
            for i, label in enumerate(labels):
                if label.startswith('samples = '):
                    labels[i] = 'samples = {}'.format(int(label.split('=')[1]) + 1)

            node.set('label', '<br/>'.join(labels))

    filename = 'tree.png'
    graph.write_png(filename)
    return

def learningSystemClassifierModel(n,feature_names,target_names,X,y,X_test):
    dt_clf = tree.DecisionTreeClassifier() # loading classifier model:: decision tree
    sffs = SequentialFeatureSelector(dt_clf, n_features_to_select=n, direction="forward") # loading feature selection model:: sequential forward feature selection 
    X_selected = sffs.fit_transform(X, y) # selecting top n features or parameters from the given training set
    selected_features = sffs.get_feature_names_out(feature_names)
    # print(selected_features.tolist())
    X_test_selected = sffs.transform(X_test) # selecting same top n features or parameters as training from the testing set
    dt_clf = dt_clf.fit(X_selected,y) # training the classifier model
    text_representation = tree.export_text(dt_clf,feature_names=selected_features.tolist())
    y_predict = dt_clf.predict(X_test_selected) # testing the classifier model
    print("Predicted Classifier Outcome: ", y_predict) # predicted classifier outcome
    # print(dt_clf.decision_path(X_test_selected))
    decisionTreePlot(dt_clf,selected_features.tolist(),target_names,X_test_selected)
    return y_predict, text_representation

def trainingSetReading(filename):
    X = []
    y = []
    feature_names = []
    startTag = True
    with open(filename,'r') as trainFile:
        for line in trainFile:
            words = line.strip('\r\n').split(',')
            if startTag:
                feature_names = words[:-1]
                startTag = False
                continue
            X.append([float(data) for data in words[:-1]])
            y.append(float(words[-1]))
    return feature_names,X,y


def parameterSetting():
    n = 5 # number of features selected for classification
    trainingSetFilename = 'learningSet.csv'
    feature_names,X,y = trainingSetReading(trainingSetFilename)
    target_names = ['Undesirable','Desirable']
    X_test = [[16252,23042,80,11,53,68,1822,175,3.27,8.16,5288],[3283,4413,95,76,50,75,722,115,3.54,2.64,9986],[1934,501,71,38,45,62,381,1568,6.36,7.69,3834]] # testing set:: parameter values
    y_test = [1, 0, 0] # testing set:: actual label
    return n, feature_names, target_names, X, y, X_test, y_test


def main():
    n, feature_names, target_names, X, y, X_test, y_test = parameterSetting() # parameter values:: training, testing set with class label and feature selection limit
    
    ## Classifier Model
    y_predict, text_representation = learningSystemClassifierModel(n, feature_names, target_names, X, y, X_test) # outcome testing results
    print("Actual Labels: ", y_test) # actual label
    print(text_representation)
    perf = testingPerformance(y_test, y_predict) # performance measure
    print(perf)
    return

if __name__ == '__main__':
    main()

