from sklearn.discriminant_analysis import LinearDiscriminantAnalysis

from MachineLearning.LearningDataHandler import LearningDataHandler

import pandas
from pandas.plotting import scatter_matrix
import matplotlib.pyplot as plt
from sklearn import model_selection
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC



class MachineLearningHandler(object):
    def load_learning_data(self, video_category):
        data_set = LearningDataHandler.get_learning_data("a")
        return data_set

    def print_dimension(self, data_set):
        print(data_set.shape)

    def show_data(self, data_set):
        print(data_set.head(20))

    def print_learning_data_stats(self, data_set):
        print(data_set.describe())

    def print_grouped_by_score(self, data_set):
        print(data_set.groupby('score').size())

    def visualize_data(self, dataset):
        dataset.plot(kind='box', subplots=True, layout=(4, 4), sharex=False, sharey=False)
        plt.show()

    def display_histograms(self, data_set):
        data_set.hist()
        plt.show()

    def display_interactions_between_variables(self, data_set):
        scatter_matrix(data_set)
        plt.show()

    def analyse_dataset(self, data_set):
        array = data_set.values
        X = array[:, 0:15]
        Y = array[:, 15]
        validation_size = 0.20
        seed = 7
        X_train, X_validation, Y_train, Y_validation = model_selection.train_test_split(X, Y, test_size=validation_size,
                                                                                        random_state=seed)

        # Test options and evaluation metric
        seed = 7
        scoring = 'accuracy'

        # Spot Check Algorithms
        models = []
        models.append(('LR', LogisticRegression()))
        # models.append(('LDA', LinearDiscriminantAnalysis()))
        models.append(('KNN', KNeighborsClassifier()))
        models.append(('CART', DecisionTreeClassifier()))
        models.append(('NB', GaussianNB()))
        models.append(('SVM', SVC()))
        # evaluate each model in turn
        results = []
        names = []
        for name, model in models:
            kfold = model_selection.KFold(n_splits=10, random_state=seed)
            cv_results = model_selection.cross_val_score(model, X_train, Y_train, cv=kfold, scoring=scoring)
            results.append(cv_results)
            names.append(name)
            msg = "%s: %f (%f)" % (name, cv_results.mean(), cv_results.std())
            print(msg)

        # fig = plt.figure()
        # fig.suptitle('Algorithm Comparison')
        # ax = fig.add_subplot(111)
        # plt.boxplot(results)
        # ax.set_xticklabels(names)
        # plt.show()

        knn = KNeighborsClassifier()
        knn.fit(X_train, Y_train)
        predictions = knn.predict(X_validation)
        print("Accuracy score")
        print(accuracy_score(Y_validation, predictions))
        print("Confusion matrix")
        print(confusion_matrix(Y_validation, predictions))
        print("Classification result")
        print(classification_report(Y_validation, predictions))

    def get_predictions(self, shots_data):
        pass

if __name__ == "__main__":
    handler = MachineLearningHandler()
    data_set = handler.load_learning_data("a")
    # handler.print_dimension(data_set)
    # handler.show_data(data_set)
    # handler.print_learning_data_stats(data_set)
    # handler.print_grouped_by_score(data_set)
    # handler.visualize_data(data_set)
    # handler.display_histograms(data_set)
    # handler.display_interactions_between_variables(data_set)
    handler.analyse_dataset(data_set)
