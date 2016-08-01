# -*- coding: utf-8 -*-

import csv
import nltk
csv.register_dialect(
    'mydialect',
    delimiter = ',',
    quotechar = '"',
    doublequote = True,
    skipinitialspace = True,
    lineterminator = '\r\n',
    quoting = csv.QUOTE_MINIMAL)

from nameparser import HumanName

# f = open("context.txt","w")
# with open('context_temp_1.csv', 'rb') as mycsvfile:
# 		thedata = csv.reader(mycsvfile, dialect='mydialect')
# 		for row in thedata:
# 			f.write(str(row[1]))
# 		f.close()


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
for name in names: