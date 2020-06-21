from prettytable import PrettyTable
from sklearn.metrics import confusion_matrix, accuracy_score
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV

import createData

def run(classifier,params):
    train, test, train_labels, test_labels = createData.split()

    #pipeline for classifier
    pipe = Pipeline(steps=[('vect', createData.vectorizer),
                    ('clf', classifier)])

    # TUNE PARAMETERS---------------------------------------------------------------------------------------------------
    # grid search keeps data balanced
    best = GridSearchCV(pipe, param_grid=params, scoring='accuracy', cv=2)
    #train (with best params)
    best.fit(train, train_labels)
    print(best.best_params_)

    #test
    predicted = best.predict(test)

    #results
    tn,fp,fn,tp = confusion_matrix(test_labels, predicted).ravel()
    matrix = PrettyTable(['TN','FP','FN','TP'])
    matrix.add_row([tn,fp,fn,tp])
    #print(matrix)
    accuracy = accuracy_score(test_labels, predicted)
    #print('accuracy = ', accuracy)
    return accuracy

#parameters for each classifier
print(SVC().get_params().keys())
paramsSVC = {'clf__C':[0.1,1,10],
             'clf__degree': [2,3],
             'clf__kernel':['linear', 'rbf', 'poly'],
             'clf__gamma':[0.1,1,10]}
print(GaussianNB().get_params().keys())
paramsGNB = {}
print(RandomForestClassifier().get_params().keys())
paramsRFC = {'clf__n_estimators':[10,100,1000],
             'clf__max_depth':[10,100,None],
             'clf__max_features':['auto','sqrt','log2'],
             'clf__min_samples_split': [2,10],
             'clf__min_samples_leaf': [1,2]}
print(DecisionTreeClassifier().get_params().keys())
paramsDTC = {'clf__criterion': ['gini','entropy'],
             'clf__splitter':['best','random'],
             'clf__max_depth':[10,100,None],
             'clf__min_samples_split': [2, 10],
             'clf__min_samples_leaf': [1, 2]}

#run multiple times
def avg(classifier,params):
    avg = 0
    nr = 10
    for i in range(nr):
        avg = avg + run(classifier,params)
    return avg/nr

#print best results for each classifier
classifiers = [SVC(),GaussianNB(),RandomForestClassifier(),DecisionTreeClassifier()]
params = [paramsSVC,paramsGNB,paramsRFC,paramsDTC]
classifiers_names = ['Support vector','Nayve Bayes','Random Forest','Decision Tree']
results_table = PrettyTable(classifiers_names)
results = []
n = len(classifiers)
for i in range(n):
    results.append(avg(classifiers[i],params[i]))
results_table.add_row(results)
print(results_table)
