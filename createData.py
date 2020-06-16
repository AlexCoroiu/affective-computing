import numpy
from sklearn.feature_extraction import DictVectorizer
from sklearn.model_selection import train_test_split

import readSRT
import glob

#extarct all srt values for familiar/unfamiliar files
def createData(files):
    list = []

    for file in files:
        list.append(readSRT.extract(file))
    return list

#get all files
familiarSRT = glob.glob('familiar/*.srt')
unfamiliarSRT = glob.glob('unfamiliar/*.srt')

familiarData = createData(familiarSRT)
unfamiliarData = createData(unfamiliarSRT)
print('example data entry:',familiarData[0])

#create feature vectors
vectorizer = DictVectorizer(sparse=False)

featureVectorsFamiliar = vectorizer.fit_transform(familiarData)
featureVectorsUnfamiliar = vectorizer.transform(unfamiliarData)
print('vocab:', vectorizer.get_feature_names())
print('example feature vector:', featureVectorsFamiliar[0])

#createdata numpy
familiar = numpy.array(familiarData)
unfamiliar = numpy.array(unfamiliarData)

#create labels numpy
labels_familiar = numpy.array([1]*len(familiar))
labels_unfamiliar = numpy.array([0]*len(unfamiliar))


#TODO: maybe manual split? to make sure training data is 50-50
#splitting data into train/test
train, test, train_labels, test_labels = train_test_split(numpy.concatenate((familiar, unfamiliar)),
                                                          numpy.concatenate((labels_familiar,labels_unfamiliar)),
                                                          test_size = 0.2)
print('train:',train, train_labels)
print('test:',test, test_labels)
