#Additional file 8
from scipy import stats
import numpy

pvalue = 0.05
topvalue = 0.65

output1 = open('likelihoods.txt', 'w')

parse_results = open('Train-matrix.txt').readlines()
fams = parse_results[0].split()
output = open('likelihoods_.txt', 'w')

#Define the different types, we're dealing with (e.g. Hyp, Meso, Psy, Ther)
#by looking at the first part of the name
typelist = []
for lineA in parse_results:
    if lineA != parse_results[0]:
        lineA = lineA.split('_')
        #print lineA[0], typelist.count(lineA[0]), typelist
        if typelist.count(lineA[0]) == 0:
            typelist.append(lineA[0])

#For each of the types, a list is made of legth corresponding to the number of gene-
#families in the input. For each gene family, we see how many of each type holds a member
#or more of that family
numlist = []
for i in range(len(typelist)):
    numlist.append(float(0))

type_likes = []
for typ in typelist:
    temp_likes = []
    for i in range(len(fams)):
        temp_likes.append(0)
    for line in parse_results:
        if line.startswith(typ) == True:
            numlist[typelist.index(typ)] += 1
            presentlist = line.split()
            count = 0
            #print presentlist[0], len(presentlist)
            for k in range(1,len(presentlist)):
                j = presentlist[k]
                count += 1
                if int(j) > 0:
                    temp_likes[count] += 1
                #print temp_likes[count]
    type_likes.append(temp_likes)

output.write('Family')
output.write('\t')
for typ in typelist:
    output.write(typ)
    output.write('\t')
output.write('\n')

count = float(-1)
for i in range(1,len(fams)):
    count += 1
    print count/len(fams)*100, '%'
    fam = fams[i]
    #output.write(fam)

    freqlist = []
    freqlist1 = []
    for j in range(len(typelist)):
        freqlist.append(type_likes[j][fams.index(fam)]/numlist[j])

    for h in freqlist:
        freqlist1.append(h)
    freqlist1.sort()
    freqlist1.reverse()

    
    top = freqlist[freqlist.index(freqlist1[0])]
    #nexttop = freqlist[freqlist.index(freqlist1[1])]
    #nextlowest = freqlist[freqlist.index(freqlist1[2])]
    #lowest = freqlist[freqlist.index(freqlist1[3])]

    #Prepare for t-tests

    #Make a binary list representingg the type with highest frequency of the gene family
    toplist = []    
    for i in range(type_likes[freqlist.index(top)][fams.index(fam)]):
        toplist.append(1)
    for i in range(int(numlist[freqlist.index(top)]-type_likes[freqlist.index(top)][fams.index(fam)])):
        toplist.append(0)

    #Make a binary list representingg all types with repect to the frequency of the gene family
    nextlistslist = []
    for x in range(len(freqlist)):          
        templist = []
        for i in range(type_likes[x][fams.index(fam)]):
            templist.append(1)
        for i in range(int(numlist[x]-type_likes[x][fams.index(fam)])):
            templist.append(0)
        nextlistslist.append(templist)

   

    bacclass = typelist[freqlist.index(max(freqlist))]
    #Tjek if family lives up to demands
    
    if freqlist1[0] >= topvalue:
        score = 0
        for liste in nextlistslist:
            if stats.ttest_ind(toplist,liste)[1] < pvalue:
                score += 1
        
        if score >= len(nextlistslist)-1: #If the higest type-dependent frequency of the gene family  is significantly higher than the frequency in all other types, it is accepted

            freqlist.append(bacclass)
            freqlist.insert(0,str(fam))

            for i in freqlist:
                output.write(str(i))
                output.write('\t')
            output.write('\n')
        


output.close()

inp = output = open('likelihoods_.txt').readlines()
for line in inp:
    output1.write(line)

output1.close()

