import pandas as pd
import numpy as np
import csv
from itertools import zip_longest
import datetime
import copy
#invert_index 在 original() 和 compare()中分别是两个table的 record number index
#invert_index1 在 original() 是 origintable 的 attribute index
#invert_index2 在 compare() 是 comparetable 的 attribute index
#invert_index3 在 original() 是 comparetable 的 record number&attribute index
#invert_index4 在 compare() 是 comparetable 的 record number&attribute index

##hash值sort可以获得元素一定排列顺序的tuple 可以直接获得检测IND？
##检测都用hash，如何确定原始数据？


filepath1="/Users/shenmengfei/Desktop/IND/csv/originaltable1.csv"

def original():
    df1 = pd.read_csv(filepath1)
    columnTitles = list(df1)
    listOfResults = []

    for eachCol in columnTitles:
        listOfResults.append(df1[eachCol].tolist())
    name,nationality,gender=listOfResults[:len(listOfResults)]
    name_hash=[]
    nationality_hash=[]
    gender_hash=[]
    tuple=[]
    #####################hash##################################
    # for x,y,z in zip(name, nationality, gender):
    #     name_hash.append(hash(x))
    #     nationality_hash.append(hash(y))
    #     gender_hash.append(hash(z))
    # #print(name_hash,nationality_hash, gender_hash)
    #     a=[hash(x), hash(y), hash(z)]
    #     a.sort()
    #     tuple.append(a)
    ###################################原来英语单词
    tupleo=[]
    for x, y, z in zip(name, nationality, gender):
        name_hash.append(x)
        nationality_hash.append(y)
        gender_hash.append(z)
    #print(name_hash,nationality_hash, gender_hash)
        tupleo.append([x,y,z])
    #print(tupleo)
    #print(tuple)
    # Algorithm 1
    # s = 9
    name_sampledValues=[]
    nationality_sampledValues=[]
    gender_sampledValues=[]
    sampledValues=[]
    s = 9

    def addToSample():
        if x not in name_sampledValues:
            name_sampledValues.append(x)
        if y not in nationality_sampledValues:
            nationality_sampledValues.append(y)
        if z not in gender_sampledValues:
            gender_sampledValues.append(z)
        sampledValues.append([x, y, z])

    for x,y,z in zip(name_hash, nationality_hash, gender_hash):
        if (len(name_sampledValues) < s and x not in name_sampledValues):
            addToSample()
        elif (len(nationality_sampledValues) < s and y not in nationality_sampledValues):
            addToSample()
        elif (len(gender_sampledValues) < s and z not in gender_sampledValues):
            addToSample()



    # print(name_sampledValues)
    # print(nationality_sampledValues)
    # print(gender_sampledValues)
    print(sampledValues)
    convertedsampledValue=list(map(list,zip(*sampledValues)))
    #print(convertedsampledValue)
    ###########

    #################################################################################
    #Algorithm 2
    #################################################################################
    #column combination指的是各列的组合吗。在此例中，我们要找的是某个人，如果缺少nationality或gender任何一个属性则不是IND，
    #所以还有必要combination吗，难道不该是直接检测所有tuple？
    #要检测的另外两个table，可能有相同的value在hashedtable中，此时update它的inverted index。如果没有则直接hll。
    #但即使有一个相同value也不能代表这个tuple为ind，所以有后续检查
    #如hashedtable中为Mary,England,Female. 检测的table中是Mary,Norway,Female.

    numbers = list(range(1,len(sampledValues)+1))
    convertedsampledValue.insert(0,numbers)
    #print(convertedsampledValue)
    d = {k: v for k, *v in zip(*convertedsampledValue)} #create dictionary
    #print(d)

    ###将set中的列表转化为字符串以便创建字典
    for k, v in d.items():
        d[k] = " ".join('%s' %id for id in v)
    #print(d)

    ####获得所有单个hash value
    all_words = []
    for i in d.values():
        #    cut = jieba.cut(i)
        cut = i.split()
        all_words.extend(cut)

    set_all_words = set(all_words)
    #print(set_all_words)

    ###得到每个hash value的inverted index
    invert_index = dict()
    for b in set_all_words:
        temp = []
        for j in d.keys():

            field = d[j]

            split_field = field.split()

            if b in split_field:
                temp.append(j)
        invert_index[b] = temp
    #print(invert_index)

    ################创建inverted index attribute
    sampledValues.insert(0,['name','nationality','gender'])
    d1 = {k: v for k, *v in zip(*sampledValues)}
    for k, v in d1.items():
        d1[k] = " ".join('%s' % id for id in v)
    #

    all_words1 = []
    for i in d1.values():
        #    cut = jieba.cut(i)
        cut = i.split()
        all_words1.extend(cut)

    set_all_words1 = set(all_words1)
    # print(set_all_words)

    ###得到每个hash value的inverted index
    invert_index1 = dict()
    for b in set_all_words1:
        temp = []
        for j in d1.keys():

            field = d1[j]

            split_field = field.split()

            if b in split_field:
                temp.append(j)
        invert_index1[b] = temp
    #print(invert_index1)

    def combinedic(invert_index,invert_index3): ##行列inverted index
        for key in invert_index:

            if invert_index3.get(key):

                invert_index3[key].append(invert_index[key])

            else:

                invert_index3[key] = [invert_index[key]]

        return invert_index3

    invert_index3 = {}
    invert_index3 = combinedic(invert_index,invert_index3)
    invert_index3 = combinedic(invert_index1, invert_index3)
    #print(invert_index3)

    return (set_all_words1,invert_index3,len(numbers),tuple,tupleo)
##########################################################################################################original()


    ###通过xor创建column combinations的hash value
    # name_nationality = []
    # name_gender = []
    # nationality_gender = []
    # for name, nationality, gender in zip(convertedsampledValue[1],convertedsampledValue[2],convertedsampledValue[3]):
    #     name_nationality.append(name^nationality)
    #     name_gender.append(name^gender)
    #     nationality_gender.append(nationality^gender)

    # print(name_nationality)
    # print(name_gender)
    # print(nationality_gender)

###############################################################################################需要对比的表 compare1.csv

filepath2="/Users/shenmengfei/Desktop/case2.csv"

def compare():
    df2 = pd.read_csv(filepath2)
    columnTitles = list(df2)
    listOfResults = []

    for eachCol in columnTitles:
        listOfResults.append(df2[eachCol].tolist())
    c1,c2,c3=listOfResults[:len(listOfResults)]
    c1_hash=[]
    c2_hash=[]
    c3_hash=[]

    tuples=[]

    for x,y,z in zip(c1, c2, c3):
        c1_hash.append(x)
        c2_hash.append(y)
        c3_hash.append(z)
        #tuples.append([x,y,z]) ##hash值变换
        tuples.append([hash(x), hash(y), hash(z)])  ##hash值变换

    #print(tuples)
    rownumber=list(range(1,len(c1)+1))
    columnnumber = list(range(1,len(listOfResults)+1))
    convertedtuples = list(map(list, zip(*tuples)))
    convertedtuples.insert(0,rownumber)
    d = {k: v for k, *v in zip(*convertedtuples)} #create dictionary
    #print(d) ##%


    ###将set中的列表转化为字符串以便创建字典
    for k, v in d.items():
        d[k] = " ".join('%s' %id for id in v)
    #print(d)

    ####获得所有单个hash value
    all_words = []
    for i in d.values():
        #    cut = jieba.cut(i)
        cut = i.split()
        all_words.extend(cut)

    set_all_words = set(all_words)
    #print(set_all_words)

    ###得到每个hash value的inverted index
    invert_index = dict()
    for b in set_all_words:
        temp = []
        for j in d.keys():

            field = d[j]

            split_field = field.split()

            if b in split_field:
                temp.append(j)
        invert_index[b] = temp
    #print(invert_index) ##%

    ################创建inverted index attribute
    tuples.insert(0, ['c1','c2','c3'])
    #print(tuples)
    d2 = {k: v for k, *v in zip(*tuples)}  # create dictionary
    for k, v in d2.items():
        d2[k] = " ".join('%s' %id for id in v)
    #print(d2)

    all_words2 = []
    for i in d2.values():
        #    cut = jieba.cut(i)
        cut = i.split()
        all_words2.extend(cut)

    set_all_words2 = set(all_words2)
    #print(set_all_words2)

    ###得到每个hash value的inverted index
    invert_index2 = dict()
    for b in set_all_words2:
        temp = []
        for j in d2.keys():

            field = d2[j]

            split_field = field.split()

            if b in split_field:
                temp.append(j)
        invert_index2[b] = temp
    #print(invert_index2)

    def combinedic(invert_index,invert_index4): ##行列inverted index
        for key in invert_index:

            if invert_index4.get(key):

                invert_index4[key].append(invert_index[key])

            else:

                invert_index4[key] = [invert_index[key]]

        return invert_index4

    invert_index4 = {}
    invert_index4 = combinedic(invert_index,invert_index4)
    invert_index4 = combinedic(invert_index2, invert_index4)
    #print(invert_index4) ##%
    return (set_all_words2,invert_index4,len(c1),tuples)

####################################################################################################compare()


####################################################################################################valuecheck()

def valuecheck():
    allwords_original=original()[0]
    allwords_compare=compare()[0]
    dic_original= original()[1]
    dic_compare = compare()[1]
    #print(allwords_original)
    #print(allwords_compare)
    # print(dic_original)
    # print(dic_compare)
    samevalue = list(allwords_original&allwords_compare)
    #print(samevalue)
    # print(samevalue[1])
    samevaluedic_original=[] #         在 original 中
    samevaluedic_compare=[] #samevalue 在 compare 中的行列索引（列表形式）

    row_original_set=[]
    row_compare_set=[]

    final_samevalue=[]

    #######检测original中的 same tuple
    for i in range(len(samevalue)):
        samevaluedic=dic_original[samevalue[i]]
        single_samevaluedic_original=[[[samevalue[i]]],samevaluedic]

        def splitlist(valuelist):

            alist = []
            a = 0

            for sublist in valuelist:
                try:  # 用try来判断是列表中的元素是不是可迭代的，可以迭代的继续迭代
                    for i in sublist:
                        alist.append(i)
                except TypeError:  # 不能迭代的就是直接取出放入alist
                    alist.append(sublist)
            for i in alist:
                if type(i) == type([]):  # 判断是否还有列表
                    a = + 1
                    break
            if a == 1:
                return splitlist(alist)  # 还有列表，进行递归
            if a == 0:
                return alist

        valuelist = splitlist(single_samevaluedic_original)
        #print(valuelist)
        samevaluedic_original.append(valuelist)
        #print(samevaluedic_original)

    # 通过检索record number找到有相同record number的值
    row_original = [[] for i in range(original()[2] + 1)]  # 创建有序空列表
    for i in range(1, original()[2] + 1):
        # print(i)
        for j in range(len(samevaluedic_original)):
            if i in samevaluedic_original[j]:
                row_original[i].append(samevaluedic_original[j])
        #print(row_original[i])
        if len(row_original[i]) == 3:  # 如果一个record number对应了三个值，则说明整个tuple都属于samevalue，找出这些tuple
            #print(i)
            # print(row_original[i])
            row_original_set.append(row_original[i])
            for k in range(len(row_original_set)):
                for m in range(3):
                    final_samevalue.append(row_original_set[k][m][0])
    final_samevalue=list(set(final_samevalue))

    #print(final_samevalue) ##一开始的samevalue只是两张表单纯比较，最终得到的是属于相同tuple的各vlaue
    #print(row_original_set)

    #######检测compare中的 same tuple
    for i in range(len(samevalue)):
        samevaluedic=dic_compare[samevalue[i]]
        #print(samevaluedic)
        single_samevaluedic_compare=[[[samevalue[i]]],samevaluedic]
        #print(single_samevaluedic_compare)

        def splitlist(valuelist):

            alist = []
            a = 0

            for sublist in valuelist:
                try:  # 用try来判断是列表中的元素是不是可迭代的，可以迭代的继续迭代
                    for i in sublist:
                        alist.append(i)
                except TypeError:  # 不能迭代的就是直接取出放入alist
                    alist.append(sublist)
            for i in alist:
                if type(i) == type([]):  # 判断是否还有列表
                    a = + 1
                    break
            if a == 1:
                return splitlist(alist)  # 还有列表，进行递归
            if a == 0:
                return alist

        valuelist = splitlist(single_samevaluedic_compare)
        #print(valuelist)
        samevaluedic_compare.append(valuelist) #给samevalue[i]加了多重[], 因为后续splitlist拆列表会拆开单词
    #print(samevaluedic_compare)

    #通过检索record number找到有相同record number的值
    row_compare=[[] for i in range(compare()[2]+1)] #创建有序空列表
    for i in range(1,compare()[2]+1):
        # print(i)
        for j in range(len(samevaluedic_compare)):
            if i in samevaluedic_compare[j]:
                row_compare[i].append(samevaluedic_compare[j])
        # print(row_compare[i])
        if len(row_compare[i])==3: #如果一个record number对应了三个值，则说明整个tuple都属于samevalue，找出这些tuple
            # print(i)
            # print(row_compare[i])
            row_compare_set.append(row_compare[i])
    #print(row_compare_set)

    # print(samevaluedic_original)
    # print(samevaluedic_compare) #得到samevalue在两张表里的行列索引

    ##现在record number 是数字， attribute不是，但有些情况都是数字则无法分辨，最好有分别的索引

    #接下来看attribute是否一一对应
    #在此relevant表格的情况下，默认已知哪些列该两两对应

    # for i in range(len(row_compare_set)):
    #     print(row_compare_set[i])
    #     for j in range(len(row_compare_set[i])):
    #         print((row_compare_set[i][j]))
    # for a in range(len(row_original_set)):
    #     print(row_original_set[a])
    #     for b in range(len(row_original_set[a])):
    #         print((row_original_set[a][b]))

    # tuple_number_original = len(row_original_set)
    # tuple_number_compare = len(row_compare_set)

    # for i in range(len(row_original_set)):
    #     for a in range(len(row_compare_set)):
    #         for j in range(len(row_original_set[i])):
    #             for b in range(len(row_compare_set[a])):
    #                 word1=[x for x in row_original_set[i][j] if x in row_compare_set[a][b]]
    #                 print(word1)

    # for i in range(len(row_original_set)):
    #
    #     for j in range(3):
    #         # for k in final_samevalue:
    #             # print(k)
    #         word = [ k for k in final_samevalue if k in row_original_set[i][0][0]]
    #         print(word)
            # for index, value in enumerate(row_original_set[i][j][0]):
            #     print (index, value)

    ########提取tuple value

    # value_original_set = []
    # for i in range(len(row_original_set)):
    #     wordset = row_original_set[i]
    #     # print(wordset)
    #     for j in range(3):
    #         word = wordset[j][0]
    #         value_original_set.append(word)
    # # print(value_original_set)
    # step = 3
    # value_original_set = [value_original_set[i:i + step] for i in range(0, len(value_original_set), step)]
    # print(value_original_set)  ###同下获得original的value
    #
    # value_compare_set=[]
    # for i in range(len(row_compare_set)):
    #     wordset=row_compare_set[i]
    #     #print(wordset)
    #     for j in range(3):
    #         word = wordset[j][0]
    #         value_compare_set.append(word)
    # # print(value_compare_set)
    # step=3
    # value_compare_set = [value_compare_set[i:i + step] for i in range(0, len(value_compare_set), step)]
    # print(value_compare_set) ###获得compare里每个tuple的value list（因为不知道怎么提取嵌套列表中的第一个元素，所以先得到所有的值再三三拆分）

    print(row_compare_set)
    value_original_set=[[t[0] for t in l] for l in row_original_set]
    value_compare_set=[[t[0] for t in l] for l in row_compare_set]
    #print(value_original_set)
    #print(value_compare_set)

    attribute_original_set=[[t[-1] for t in l] for l in row_original_set]
    attribute_compare_set=[[t[-1] for t in l] for l in row_compare_set]
    #print(attribute_original_set)
    #print(attribute_compare_set)


    # def attribute_check(combinations): ##创建规则，检查列是否对应，对应则为true ##问题是若一个值在多列中出现，无法确定inverted index，会造成false negative
    #     for i in range(len(combinations)):
    #         for j in range(3):
    #             if combinations[i][j] != ('c1', 'name') or ('c2', 'nationality') or ('c3', 'gender'):
    #                 return (combinations[i])

    attribute_combinations=[]
    for i in range(len(value_compare_set)):
        for j in range(len(value_original_set)):
            if value_compare_set[i] == value_original_set[j]:
                #print(row_compare_set[i],i,attribute_compare_set[i])
                #print(row_original_set[j],j,attribute_original_set[j])
                # attribute_combination=(attribute_compare_set[i],attribute_original_set[j])
                # print(attribute_combination)
                #print(row_compare_set[i],row_original_set[j])
                attribute_combination=list(zip(attribute_compare_set[i],attribute_original_set[j]))
                attribute_combinations.append(attribute_combination)
    #print(attribute_combinations)
    # print(attribute_check(attribute_combinations)

    ###不是IND的tuple
    # flag=0
    # for i in range(len(attribute_combinations)): ##创建规则，检查列是否对应，对应则为true ##问题是若一个值在多列中出现，无法确定inverted index，会造成false negative
    #     for j in range(3):
    #         if attribute_combinations[i][j] == ('c1', 'name'):
    #             flag=1
    #         elif attribute_combinations[i][j] == ('c2', 'nationality'):
    #             flag=1
    #         elif attribute_combinations[i][j] == ('c3', 'gender'):
    #             flag=1
    #         else:
    #             print(attribute_combinations[i],i) ##因为得到attribute_combinations的forloop最外圈是compare，所以是compare里的顺序
    #             print(row_compare_set[i])

    ###是IND的tuple
    ##此处用了子集包含与否来检测是否attribute对应
    IND_tuple=[]
    compare_not_IND_tuple=[]
    compare_all_tuples=compare()[3]
    del(compare_all_tuples[0])
    #print(compare_all_tuples)
    corect_attributes=[('c1', 'name'), ('c2', 'nationality'), ('c3', 'gender')]
    for i in range(len(attribute_combinations)):
       if set(attribute_combinations[i])<=set(corect_attributes):
           # print(row_compare_set[i])
           #  print(value_compare_set[i])
           value_compare_set[i]=[int(x) for x in value_compare_set[i]] #####换成hash记得取消comment！！！！！！##此处最初的hash值是字符串，转化成int后续比较
           value_compare_set[i].sort()
           IND_tuple.append(value_compare_set[i])
    for x in compare_all_tuples:
        x.sort() ##列表中元素顺序会被打乱，用sort排序后续才能检测出相同与不同
        if x not in IND_tuple:
            compare_not_IND_tuple.append(x)

    #print(IND_tuple)
    #print(compare_not_IND_tuple)

    return(IND_tuple,compare_not_IND_tuple)

def HLL():
    original_hash_tuples = original()[3]
    compare_not_IND_tuple=valuecheck()[1]
    IND_tuple=valuecheck()[0]
    #print(original_hash_tuples)
    #print(compare_not_IND_tuple) #######
    original_not_IND_tuple=[]
    for x in original_hash_tuples:
        x.sort()
        if x not in IND_tuple:
            original_not_IND_tuple.append(x)
    #print(original_not_IND_tuple) ######

    ######论文HLL法
    # sub='0'
    # compare_not_IND_tuple_hll=[]
    # for x in compare_not_IND_tuple:
    #     for i in range(3):
    #         x[i]='{:b}'.format(x[i])
    #         #print(x[i])
    #         if int(x[i])<0: #如果是负数
    #             x[i]=x[i][:5]
    #             #print(x[i])
    #             # if x[i][1]=='1': #如果首位是1
    #             x[i]=x[i][:2]+str(x[i].count(sub,2))
    #             # if x[i][1] == '0':  # 如果首位是0
    #             #     x[i] = x[i][:2] + str(x[i].count(sub, 2))
    #         else:
    #             x[i] = x[i][:4]
    #             x[i] = x[i][:1] + str(x[i].count(sub, 1))
    #     # x=[str(i) for i in x]
    #     x=''.join(x)

    ##如果将得到的结果连成一串字符串对比 1000 0001 0101
    compare_not_IND_tuple_hll=[]
    for x in compare_not_IND_tuple:
        for i in range(3):
            x[i]='{:b}'.format(x[i])
            #print(x[i])
            if int(x[i])<0: #如果是负数
                x[i]=x[i][:5]
                #print(x[i])
                # if x[i][1]=='1': #如果首位是1
                #x[i]=x[i][:2]+str(x[i].count(sub,2))
                # if x[i][1] == '0':  # 如果首位是0
                #     x[i] = x[i][:2] + str(x[i].count(sub, 2))
            else:
                x[i] = x[i][:4]
                #x[i] = x[i][:1] + str(x[i].count(sub, 1))
        # x=[str(i) for i in x]
        x=''.join(x)
        compare_not_IND_tuple_hll.append(x)
    #print(compare_not_IND_tuple)

    #print(compare_not_IND_tuple_hll)

    original_not_IND_tuple_hll = []
    original_not_IND_tuple_split=copy.deepcopy(original_not_IND_tuple)

    ######论文HLL法
    # for x in original_not_IND_tuple_split:
    #     for i in range(3):
    #         x[i]='{:b}'.format(x[i])
    #         if int(x[i])<0:
    #             x[i]=x[i][:5]
    #             x[i] = x[i][:2] + str(x[i].count(sub, 2))
    #         else:
    #             x[i] = x[i][:4]
    #             x[i] = x[i][:1] + str(x[i].count(sub, 1))
    #     x = ''.join(x)
    #     original_not_IND_tuple_hll.append(x)

    ##如果将得到的结果连成一串字符串对比 1000 0001 0101
    for x in original_not_IND_tuple_split:
        for i in range(3):
            x[i]='{:b}'.format(x[i])
            if int(x[i])<0:
                x[i]=x[i][:5]
                # x[i] = x[i][:2] + str(x[i].count(sub, 2))
            else:
                x[i] = x[i][:4]
                # x[i] = x[i][:1] + str(x[i].count(sub, 1))
        x = ''.join(x)
        original_not_IND_tuple_hll.append(x)

    #print(original_not_IND_tuple_hll)

    b=set(compare_not_IND_tuple_hll)&set(original_not_IND_tuple_hll)
    blist=list(b)
    #print(b)
    #print(blist)
    print(IND_tuple)

##如果根据索引找原列表？
    original_originalvalue_tuples=original()[4]
    for m in IND_tuple:
        for i, v in enumerate(original_hash_tuples):
            if v == m:
                #print(i)
                print(original_originalvalue_tuples[i]) ###inverted index 获得的IND

    for m in blist:
        for i, v in enumerate(original_not_IND_tuple_hll):
            if v == m:
                #print(i)
                #print(original_not_IND_tuple[i])
                for x, y in enumerate(original_hash_tuples):
                    if y == original_not_IND_tuple[i]:
                        #print(x)
                        print(original_originalvalue_tuples[x])


if __name__ == "__main__":
    starttime = datetime.datetime.now()
    original()
    compare()
    valuecheck() ##看compare里的值在不在original里
    HLL()
    endtime = datetime.datetime.now()
    print('Running time: %s Seconds' % (endtime - starttime))


    # 1000 0001 0101
    # 0111000 -> 00
    # 0110000 -> 00
    # 0000001 -> 05


## 1
## 无法返回原始值
## 找index  (ok)

## 2
## 现阶段消除HLL false positive
## (因为用了sort，无法准确检测value与对应的attribute，比如mary australia female会被列成IND)

## 3
## 先应用HLL to 所有tuple， 然后用inverted index去除false positive

## 对于少数量column的table，不用inverted index？ 只要比对binary hash
## 对于多数量，。。。

## 分开讨论 inverted index 和 HLL


