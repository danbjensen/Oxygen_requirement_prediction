#Additional file 10
#Evaluate predictive performance of predicter.py
#Percentvise correct predections of each type
import string, math, os
import sys

inp = sys.argv
if len(inp) > 1:
    predictions = open(sys.argv[1]).readlines()
else:
    predictions = open('All_top_predictions.txt').readlines()
output = open('predictive_evaluations.txt','a')

typelist = []
for lineA in predictions:
    lineA = lineA.split('_')
    #print lineA[0], typelist.count(lineA[0]), typelist
    if typelist.count(lineA[0]) == 0:
        typelist.append(lineA[0])

MCC_list = []
N_list = []
correct_list = []
for typ in typelist:
    N_list.append(0)
    correct_list.append(0)
    MCC_list.append(0)

for typ in typelist:
    for line in predictions:
        if line.startswith(typ) == True:
            N_list[typelist.index(typ)] += 1

   
for line in predictions:
    words = string.split(line)
    if words[0].count(words[1]) > 0:
        correct_list[typelist.index(words[1])] += 1

print correct_list
print N_list

count = -1
print '\n'
for i in correct_list:
    count += 1
    percent = (float(i)/N_list[count])*100
    print percent
    output.write(typelist[count])
    output.write('\t')
    output.write(str(percent))
    output.write(' %')
    output.write('\n')
output.write('\n')
print '\n', '\n'

#Mathews correlation coefficient    
TP_list = []
FP_list = []
TN_list = []
FN_list = []

for i in typelist:
    TP_list.append(0)
    FP_list.append(0)
    TN_list.append(0)
    FN_list.append(0)    
    
    
for line in predictions: #Caluculate the TP, FP, TN and TN values of each type
    line = line.replace('"','')
    words = line.split()
    for typ in typelist:
        if words[0].startswith(typ) == True and words[1].startswith(typ) == True: # true positive
            TP_list[typelist.index(typ)] += 1
        elif words[0].startswith(typ) == False and words[1].startswith(typ) == True: # false positive
            FP_list[typelist.index(typ)] += 1
        elif words[0].startswith(typ) == False and words[1].startswith(typ) == False: # true negtive
            TN_list[typelist.index(typ)] += 1
        elif words[0].startswith(typ) == True and words[1].startswith(typ) == False: # false negative
            FN_list[typelist.index(typ)] += 1


#Do the Mathews evaluation
for typ in typelist:
    TP = TP_list[typelist.index(typ)]
    FP = FP_list[typelist.index(typ)]
    TN = TN_list[typelist.index(typ)]
    FN = FN_list[typelist.index(typ)]

    if (TP+FP)*(TP+FN)*(TN+FP)*(TN+FN) == 0:
        print 'ZERO OVERHERE!'
        MCC = (TP*TN - FP*FN)/1
    else:
        MCC = (TP*TN - FP*FN)/math.sqrt( (TP+FP)*(TP+FN)*(TN+FP)*(TN+FN) )
    MCC_list[typelist.index(typ)] += MCC

print 'Mathews correlation coefficients'
for typ in typelist:
    print typ, MCC_list[typelist.index(typ)]
    output.write(typ)
    output.write('\t')
    output.write(str(MCC_list[typelist.index(typ)]))
    output.write('\n')

#end = input('')
#os.startfile('predictive_evaluations.txt')
output.close()
