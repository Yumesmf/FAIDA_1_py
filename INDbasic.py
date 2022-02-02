import pandas as pd
import numpy as np
import csv
from itertools import zip_longest

filepath1="/Users/shenmengfei/Desktop/originaltable.csv"
filepath2="/Users/shenmengfei/Desktop/compare.csv"

####################################1
df1 = pd.read_csv(filepath1)
columnTitles1 = list(df1)
listOfResults1 = []

for eachCol in columnTitles1:
    listOfResults1.append(df1[eachCol].tolist())
name1,nationality1,residence1=listOfResults1[:3]
name1_hash=[]
nationality1_hash=[]
residence1_hash=[]

####################################2
df2 = pd.read_csv(filepath2)
columnTitles2 = list(df2)
listOfResults2 = []

for eachCol in columnTitles2:
    listOfResults2.append(df2[eachCol].tolist())
name2,nationality2,residence2=listOfResults2[:3]
name2_hash=[]
nationality2_hash=[]
residence2_hash=[]

##################1
for x,y,z in zip(name1, nationality1, residence1):
    name1_hash.append(x)
    nationality1_hash.append(y)
    residence1_hash.append(z)

##################2
for x, y, z in zip(name2, nationality2, residence2):
    name2_hash.append(x)
    nationality2_hash.append(y)
    residence2_hash.append(z)

# print(name1_hash,nationality1_hash,residence1_hash)
# print(name2_hash,nationality2_hash,residence2_hash)

table1=[]
table1.append(name1_hash)
table1.append(nationality1_hash)
table1.append(residence1_hash)
table2=[]
table2.append(name2_hash)
table2.append(nationality2_hash)
table2.append(residence2_hash)
# print(table1)
# print(table2)

convertedtable1=list(map(list,zip(*table1)))
convertedtable2=list(map(list,zip(*table2)))
# print(convertedtable1)

######1
labels1 = list(df1.columns.values)
convertedtable1.insert(0,labels1)
# print(convertedtable1)
d1 = {k: v for k, *v in zip(*convertedtable1)}
# print(d1)

for k, v in d1.items():
    d1[k] = " ".join('%s' %id for id in v)
#print(d1)

all_words1 = []
for i in d1.values():
    cut = i.split()
    all_words1.extend(cut)
set_all_words1 = set(all_words1)
#print(set_all_words1)

invert_index1 = dict()
for b in set_all_words1:
    temp1 = []
    for j in d1.keys():

        field1 = d1[j]

        split_field1 = field1.split()

        if b in split_field1:
            temp1.append(j)
    invert_index1[b] = ','.join(temp1)
#print(invert_index1)

######2
labels2 = list(df2.columns.values)
convertedtable2.insert(0,labels2)
# print(convertedtable2)
d2 = {k: v for k, *v in zip(*convertedtable2)}
#print(d2)

for k, v in d2.items():
    d2[k] = " ".join('%s' %id for id in v)
# print(d2)

all_words2 = []
for i in d2.values():
    cut = i.split()
    all_words2.extend(cut)
set_all_words2 = set(all_words2)
# print(set_all_words2)

invert_index2 = dict()
for b in set_all_words2:
    temp2 = []
    for j in d2.keys():

        field2 = d2[j]

        split_field2 = field2.split()

        if b in split_field2:
            temp2.append(j)
    invert_index2[b] = ','.join(temp2)
#print(invert_index2)


samevalue1={x:invert_index1[x] for x in invert_index1 if x in invert_index2}
samevalue2={x:invert_index2[x] for x in invert_index1 if x in invert_index2}
# print(samevalue1)
# print(samevalue2)

####
s11=set()
s21=set()
#
for key1, val1 in samevalue1.items():
        if 'Name1' in val1:
            s11.add(key1)
for key2, val2 in samevalue2.items():
        if 'Name2' in val2:
            s21.add(key2)
s1=s11&s21
print("The IND in 'Name1' between 'Name2' is",s1)
#
s12=set()
s22=set()
for key1, val1 in samevalue1.items():
        if 'Nationality1' in val1:
            s12.add(key1)
for key2, val2 in samevalue2.items():
        if 'Nationality2' in val2:
            s22.add(key2)
s2=s12&s22
print("The IND in 'Nationality1' between 'Nationality2' is",s2)
#
s13=set()
s23=set()
for key1, val1 in samevalue1.items():
        if 'Residence1' in val1:
            s13.add(key1)
for key2, val2 in samevalue2.items():
        if 'Residence2' in val2:
            s23.add(key2)
s3=s13&s23
print("The IND in 'Residence1' between 'Residence2' is",s3)
#
s14=set()
s24=set()
for key1, val1 in samevalue1.items():
        if 'Nationality1' in val1:
            s14.add(key1)
for key2, val2 in samevalue2.items():
        if 'Residence2' in val2:
            s24.add(key2)
s4=s14&s24
print("The IND in 'Nationality1' between 'Residence2' is",s4)
#