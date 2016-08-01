#!/usr/bin/env python
# encoding: utf-8
"""
genderPredictor.py
"""
import nltk
from nltk import NaiveBayesClassifier,classify
import USSSALoader
import random
import csv 

class genderPredictor():
    
    def getFeatures(self):
        maleNames,femaleNames=self._loadNames()
        
        featureset = list()
        
        for nameTuple in maleNames:
            features = self._nameFeatures(nameTuple[0])
            male_prob, female_prob = self._getProbDistr(nameTuple)
            features['male_prob'] = male_prob
            features['female_prob'] = female_prob
            featureset.append((features,'M'))
        
        for nameTuple in femaleNames:
            features = self._nameFeatures(nameTuple[0])
            male_prob, female_prob = self._getProbDistr(nameTuple)
            features['male_prob'] = male_prob
            features['female_prob'] = female_prob
            featureset.append((features,'F'))
    
        return featureset
    
    def trainAndTest(self,trainingPercent=0.80):
        featureset = self.getFeatures()
        random.shuffle(featureset)
        
        name_count = len(featureset)
        
        cut_point=int(name_count*trainingPercent)
        
        train_set = featureset[:cut_point]
        test_set  = featureset[cut_point:]
        
        self.train(train_set)
        
        return self.test(test_set)
        
    def classify(self,name):
        feats=self._nameFeatures(name)
        return self.classifier.classify(feats)
        
    def train(self,train_set):
        self.classifier = NaiveBayesClassifier.train(train_set)
        return self.classifier
        
    def test(self,test_set):
       return classify.accuracy(self.classifier,test_set)
    
    def _getProbDistr(self,nameTuple):
            male_prob = (nameTuple[1] * 1.0) / (nameTuple[1] + nameTuple[2])
            if male_prob == 1.0:
                male_prob = 0.99
            elif male_prob == 0.0:
                male_prob = 0.01
            else:
                pass
            female_prob = 1.0 - male_prob
            return (male_prob, female_prob)
        
    def getMostInformativeFeatures(self,n=5):
        return self.classifier.most_informative_features(n)
        
    def _loadNames(self):
        return USSSALoader.getNameList()
        
    def _nameFeatures(self,name):
        name=name.upper()
        return {
            'last_letter': name[-1],
            'last_two' : name[-2:],
            'last_three': name[-3:],
            'last_is_vowel' : (name[-1] in 'AEIOUY')
        }








f = open("context.txt","rb")
# li = [line.strip() for line in f.readlinesf 
lf = f.read().strip().decode("utf-8")
print lf

def get_human_names(lf):
    tokens = nltk.tokenize.word_tokenize(lf)
    pos = nltk.pos_tag(tokens)
    sentt = nltk.ne_chunk(pos, binary = False)
    person_list = []
    person = []
    name = ""
    for subtree in sentt.subtrees(filter=lambda t: t.label()== 'PERSON'):
        for leaf in subtree.leaves():
            person.append(leaf[0])
        if len(person) > 1: #avoid grabbing lone surnames
            for part in person:
                name += part + ' '
            if name[:-1] not in person_list:
                person_list.append(name[:-1])
            name = ''
        person = []

    print person_list

    return (person_list)


names = get_human_names(lf)




if __name__ == "__main__":
    gp = genderPredictor()
    accuracy=gp.trainAndTest()
    print 'Accuracy: %f'%accuracy
    print 'Most Informative Features'
    feats=gp.getMostInformativeFeatures(10)
    for feat in feats:
        print '\t%s = %s'%feat

    dat = []
    k = 0
    for nam in names:
        k = k+1
        output = {}
        output["Sl No"] = k
        output["Name"] = nam.encode("utf-8")
        n = gp.classify(nam)
        output["Gender"] = n
        dat.append(output)
        print output
    print dat


    def WriteDictToCSV(csv_columns,dict_data):
        with open("nltk", 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
            for row in dict_data:
                # r = row.encode("utf-8")
                writer.writerow(row)


    csv_columns =['Sl No', 'Name','Gender']

    WriteDictToCSV(csv_columns,dat) 
     
