from prettytable import PrettyTable
from sklearn.metrics import confusion_matrix, accuracy_score
from sklearn.svm import SVC
from sklearn.pipeline import Pipeline

import createData

#TODO: decide on classifier (binary)
#TODO: decide on classifier parameters


#TODO: grid search for best parameters?

def runSVC():
    train, test, train_labels, test_labels = createData.split()
    classifier = SVC()
    svc_pipe = Pipeline(steps=[('vect', createData.vectorizer),
                               ('clf', classifier)])
    #train
    svc_pipe.fit(train, train_labels)

    #test
    predicted = svc_pipe.predict(test)

    #results
    tn,fp,fn,tp = confusion_matrix(test_labels, predicted).ravel()
    matrix = PrettyTable(['TN','FP','FN','TP'])
    matrix.add_row([tn,fp,fn,tp])
    print(matrix)
    accuracy = accuracy_score(test_labels, predicted)
    print('accuracy= ', accuracy)
    return accuracy

avg = 0
nr = 10
for i in range(nr):
    avg = avg + runSVC()

avg = avg/nr
print('average = ', avg)
