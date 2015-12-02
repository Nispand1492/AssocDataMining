__author__ = 'Nispand'
import pymysql

db = pymysql.connect("localhost","root","root")
cur = db.cursor()
print "Here"
def load_dataset(cur):
    "Load the sample dataset."
    cur.execute("use associationrulemining")
    cur.execute("select * from locations")
    data = cur.fetchall()
    return data
#new

def null_values(cur):
    print "Got into null_values"
    cur.execute("use associationrulemining")
    cur.execute("select * from locations where City is Null or State is Null or Zip is Null")
    null=cur.fetchall()
    print "Tuples with Null Values in database::\n" ,null
    return null


def Tuples_Null_Set(Null_Record):
    "Create a list of candidate item sets of size one corresponding to null values."
    n1 = []
    a = []
    for transaction in Null_Record:
        print transaction
        for item in transaction:
            print item
            if (not [item] in n1) and (item != None):
                a.append(item)
        print a
        n1.append(a)
        a = []

    n1.sort()
    #frozenset because it will be a ket of a dictionary.
    return map(frozenset, n1)

def createC1(dataset):
    "Create a list of candidate item sets of size one."
    c1 = []
    for transaction in dataset:
        for item in transaction:
            if not [item] in c1:
                c1.append([item])
    c1.sort()
    #frozenset because it will be a ket of a dictionary.
    return map(frozenset, c1)

def scanD(Null_Record, candidates, min_support):
    "Returns all candidates that meets a minimum support level"
    sscnt = {}
    for tid in Null_Record:
        for can in candidates:
            if can.issubset(tid):
                sscnt.setdefault(can, 0)
                sscnt[can] += 1

    num_items = float(len(Null_Record))
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
    "Generate a list of candidate item sets"
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

def generateRules(L, support_data, min_confidence=0.8):
    """Create the association rules
    L: list of frequent item sets
    support_data: support data for those itemsets
    min_confidence: minimum confidence threshold
    """
    rules = []
    for i in range(1, len(L)):
        for freqSet in L[i]:
            H1 = [frozenset([item]) for item in freqSet]
            #print "freqSet", freqSet, 'H1', H1
            if (i > 1):
                rules_from_conseq(freqSet, H1, support_data, rules, min_confidence)
            else:
                calc_confidence(freqSet, H1, support_data, rules, min_confidence)

    return rules


def calc_confidence(freqSet, H, support_data, rules, min_confidence=0.0):
    "Evaluate the rule generated"
    pruned_H = []
    for conseq in H:
        try :
            conf = support_data[freqSet] / support_data[freqSet - conseq]
        except :
            pass
        if conf >= min_confidence:
            #print freqSet - conseq, '--->', conseq, 'conf:', conf
            rules.append((freqSet - conseq, conseq, conf))
            pruned_H.append(conseq)

    return pruned_H


def rules_from_conseq(freqSet, H, support_data, rules, min_confidence=0.0):
    "Generate a set of candidate rules"
    m = len(H[0])
    if (len(freqSet) > (m + 1)):
        Hmp1 = aprioriGen(H, m + 1)
        Hmp1 = calc_confidence(freqSet, Hmp1,  support_data, rules, min_confidence)
        if len(Hmp1) > 1:
            rules_from_conseq(freqSet, Hmp1, support_data, rules, min_confidence)

def search_results(x,result):
    d_l=[]
    for y in result:
        if x in y:
            d_l.append(y)
    return d_l

dataset = load_dataset(cur)
a,b = apriori(dataset)

result = generateRules(a,b)
Null_Record=null_values(cur)
n1=Tuples_Null_Set(Null_Record)
a_r=[]
for x in n1:
    r= search_results(x,result)
    a_r.append(r)
for a in a_r:
    print frozenset(a)


