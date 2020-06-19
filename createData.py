import numpy
from sklearn.feature_extraction import DictVectorizer
from sklearn.model_selection import train_test_split

import readSRT
import glob

#extarct all srt values for familiar/unfamiliar files
def createData(files):
    list = []

    for file in files:
        #here choose default feature combination
        list.append(readSRT.extract(file, 2))
    return list

#get all files
familiarSRT = glob.glob('familiar/*.srt')
unfamiliarSRT = glob.glob('unfamiliar/*.srt')

familiarData = createData(familiarSRT)
unfamiliarData = createData(unfamiliarSRT)
print('example data entry:',familiarData[0])

#create feature vectors
vectorizer = DictVectorizer(sparse=False)

#example:
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

#splitting data into train/test
def split():
    return train_test_split(numpy.concatenate((familiar, unfamiliar)),
                                                          numpy.concatenate((labels_familiar,labels_unfamiliar)),
                                                          test_size = 0.2)
