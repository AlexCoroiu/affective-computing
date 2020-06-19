from prettytable import PrettyTable
from sklearn.metrics import confusion_matrix, accuracy_score
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression

import createData

#TODO: decide on classifier parameters
#TODO: grid search for best parameters?

def run(classifier):
    train, test, train_labels, test_labels = createData.split()
    pipe = Pipeline(steps=[('vect', createData.vectorizer),
                           ('clf', classifier)])
    #train
    pipe.fit(train, train_labels)

    #test
    predicted = pipe.predict(test)

    #results
    tn,fp,fn,tp = confusion_matrix(test_labels, predicted).ravel()
    matrix = PrettyTable(['TN','FP','FN','TP'])
    matrix.add_row([tn,fp,fn,tp])
    #print(matrix)
    accuracy = accuracy_score(test_labels, predicted)
    #print('accuracy = ', accuracy)
    return accuracy

def avg(classifier):
    avg = 0
    nr = 100
    for i in range(nr):
        avg = avg + run(classifier)
    return avg/nr

classifiers = [SVC(),GaussianNB(),RandomForestClassifier(),DecisionTreeClassifier()]
classifiers_names = ['Support vector','Nayve Bayes','Random Forest','Decision Tree']
results_table = PrettyTable(classifiers_names)
results = []
for c in classifiers:
    results.append(avg(c))
results_table.add_row(results)
print(results_table)