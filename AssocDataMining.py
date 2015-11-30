__author__ = 'Nispand'
import pymysql

def load_dataset():
    "Load the sample dataset."
    db = pymysql.connect("localhost","root","root")
    cur = db.cursor()
    cur.execute("use associationrulemining")
    cur.execute("select * from student")
    data=cur.fetchall()
    return data
    #return [[1, 'Jim', 'pecanst'], [2, 'Dominic', 'pecanst'], [3, 'sang', 'null'], [4,'Bryan' ,'Mitchelle st'],[5,'Siddhant','null'],[6,'Aisha','pecan st'],[7,'Simran','mitchelle st'],[8,'Palak','null'][3,'Sang','cooperst'],[8,'null','cooperst']]

def createC1(dataset):
    "Create a list of candidate item sets of size one."
    c1 = []
    for transaction in dataset:
        for item in transaction:
            if not [item] in c1:
                c1.append([str(item)])
    c1.sort()
    #frozenset because it will be a ket of a dictionary.
    return map(frozenset, c1)

def scanD(dataset, candidates, min_support):
    "Returns all candidates that meets a minimum support level"
    sscnt = {}
    print(type(candidates))
    for tid in dataset:
        candidates = candidates
        for can in candidates:
            if can.issubset(tid):
                sscnt.setdefault(can, 0)
                sscnt[can] += 1
        can = "null"

    num_items = float(len(dataset))
    retlist = []
    support_data = {}
    for key in sscnt:
        support = sscnt[key] / num_items
        if support >= min_support:
            retlist.insert(0, key)
        support_data[key] = support
    return retlist, support_data


def aprioriGen(freq_sets, k):
    "Generate the joint transactions from candidate sets"
    retList = []
    lenLk = len(freq_sets)
    for i in range(lenLk):
        for j in range(i + 1, lenLk):
            L1 = list(freq_sets[i])[:k - 2]
            L2 = list(freq_sets[j])[:k - 2]
            L1.sort()
            L2.sort()
            if L1 == L2:
                retList.append(freq_sets[i] | freq_sets[j])
    return retList

def apriori(dataset, minsupport=0.0):
    #"Generate a list of candidate item sets"
    C1 = createC1(dataset)
    D = list(map(set, dataset))
    L1, support_data = scanD(D, C1, minsupport)
    L = [L1]
    k = 2
    while (len(L[k - 2]) > 0):
        Ck = aprioriGen(L[k - 2], k)
        Lk, supK = scanD(D, Ck, minsupport)
        support_data.update(supK)
        L.append(Lk)
        k += 1
    return L, support_data

dataset = load_dataset()
print (dataset)
freq,sup = apriori(dataset)


