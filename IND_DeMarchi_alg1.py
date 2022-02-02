# all based on Efficient Algorithms for Mining Inclusion Dependencies Alg1
import pandas as pd
import numpy as np
import csv
from itertools import zip_longest

filepath1="/Users/shenmengfei/Desktop/A.csv"
filepath2="/Users/shenmengfei/Desktop/B.csv"

#################################### A
df1 = pd.read_csv(filepath1)
int1=df1[['A','C','D']]
columnTitles1 = list(int1)
listOfResults1 = []

labels1 = list(int1.columns.values)
rhs=[]
rhs.append(['A','C','D'])
print(rhs[0]) ## line1

for eachCol in columnTitles1:
    listOfResults1.append(int1[eachCol].tolist())
A_A,A_C,A_D=listOfResults1[:3]

A_a=[]
A_c=[]
A_d=[]
for x,y,z in zip(A_A,A_C,A_D):
    A_a.append((x,'A'))
    A_c.append((y,'C'))
    A_d.append((z,'D'))
#print(A_a,A_c,A_d) ##line3

#################################### B
df2 = pd.read_csv(filepath2)
int2=df2[['A','C','D']]
columnTitles2 = list(int2)
listOfResults2 = []

labels2 = list(df2.columns.values)
for eachCol in columnTitles2:
    listOfResults2.append(int2[eachCol].tolist())
B_A,B_C,B_D=listOfResults2[:3]

B_a=[]
B_c=[]
B_d=[]
for x,y,z in zip(B_A,B_C,B_D):
    B_a.append((x,'A'))
    B_c.append((y,'C'))
    B_d.append((z,'D'))
# print(B_a)
##############

same_a = [x for x in A_a if x in B_a]
same_c = [x for x in A_c if x in B_c]
same_d = [x for x in A_d if x in B_d] ##line4

if same_a == A_a:
    print("There's IND between attributeA in TableA and TableB")
else:
    print("There's no IND between attributeA in TableA and TableB")

if same_c == A_c:
    print("There's IND between attributeB in TableA and TableB")
else:
    print("There's no IND between attributeB in TableA and TableB")

if same_d == A_d:
    print("There's IND between attributeC in TableA and TableB")
else:
    print("There's no IND between attributeC in TableA and TableB")


