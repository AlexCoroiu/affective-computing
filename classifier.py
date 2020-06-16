from prettytable import PrettyTable
from sklearn.metrics import confusion_matrix, accuracy_score
from sklearn.svm import SVC
from sklearn.pipeline import Pipeline

import createData

#TODO: decide on classifier (binary)
#TODO: decide on classifier parameters
classifier = SVC()
svc_pipe = Pipeline(steps = [('vect', createData.vectorizer),
                                 ('clf',classifier)])

#TODO: grid search for best parameters?

#train
svc_pipe.fit(createData.train, createData.train_labels)

#test
predicted = svc_pipe.predict(createData.test)

#results
tn,fp,fn,tp = confusion_matrix(createData.test_labels, predicted).ravel()
matrix = PrettyTable(['TN','FP','FN','TP'])
matrix.add_row([tn,fp,fn,tp])
print(matrix)
print('accuracy= ', accuracy_score(createData.test_labels, predicted))
