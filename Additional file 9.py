#Additional file 9
#! /tools/bin/python2.7

import string, os, random, math
import subprocess

#path = raw_input('State working directorey: ')
#path = 'D:\DTU-studier\Master speciale\myShare\test\Ny mappe (2)'

print 'PRIDICTIONS INITIATED!!!!'

pseudocount = 0.1


all_top = open('All_top_predictions.txt','a')

likelihood = open('likelihoods.txt').readlines()
print 'Families included: ', len(likelihood)
output = open('predictions_.txt','w')
output_true = open('predictions.txt','w')
output1 = open('All_predictions.txt','a')
parse_results = open('Test-matrix.txt').readlines()
#parse_likelihoods = open('used_likelihoods.txt','w')
#parselikelist = []
#struct_based = open('struct-based_predictions.txt').readlines()

typelist = []
for i in range(1,len(likelihood[0].split())):
    typelist.append(likelihood[0].split()[i])

output1.write('Genome')
output1.write('\t')
p_list = []
for typ in typelist:
    p_list.append(float(1)/len(typelist))
    output1.write(typ)
    output1.write('\t')
output1.write('\n')

families = []
for line in likelihood:
    words = string.split(line)
    families.append((words[0]))


fams = string.split(parse_results[0])
abe = 0
for i in range(1,len(parse_results)):
    abe += 1
    print abe, i
    line = parse_results[i]
    presentlist = string.split(line)
    actualclass = presentlist[0].split('_')[0]
    #print presentlist[0]
    output1.write(presentlist[0])
    output1.write('\t')
    obscount = -1

    p_obs_list = []
    for p in p_list:
        p_obs_list.append(p)

    #print 1, p_obs_list
    
    for obs in presentlist:
        obscount += 1
	#print obscount, fams[obscount], families.count(fams[obscount])
        if families.count(fams[obscount]) > 0:
            likelihood_freqs = likelihood[families.index(fams[obscount])].replace(',','.')
	    #print fams[obscount]
            words = string.split(likelihood_freqs)
                   
            if int(obs) > 0:     #p_obs_hyp = p(precense/absence-observationer|hyp)
                count = 0
                for i in range(len(p_obs_list)):
                    count += 1
                    p_obs_list[i] *= (float(words[count])+pseudocount)
     
            else:
                count = 0
                for i in range(len(p_obs_list)):
                    count += 1
                    p_obs_list[i] *= (1-float(words[count])+pseudocount)

    #print 2, p_obs_list
                
    #print p_obs_list
    """for i in range(len(p_obs_list)):
        p_obs = p_obs_list[i]
        print p_obs_list[i]
        p_obs_list[i] = math.exp(p_obs)
        print p_obs_list[i]
        print '\n'
    #print 3, p_obs_list
    #print '\n'"""
        
   
    p_obs_total = sum(p_obs_list) # Same as "evidence"
    #print 'p_obs_total', p_obs_total
    #p_obs_total = math.log(p_obs_total)
    #print 'New p_obs_total', p_obs_total

    predlist = []
    for p_obs in p_obs_list:
        predlist.append(p_obs/p_obs_total)
        
    if sum(predlist) != 1.0:
        print 'Sum', sum(predlist)

    #for i in range(len(predlist)):
    #    pred = predlist[i]
    #    predlist[i] = math.exp(pred)
    
    

    print 'Predlist', predlist

    # Print results to file
    #print genomename.replace('\t','')
    output.write(presentlist[0])
    output.write('\t')
    all_top.write(presentlist[0])
    all_top.write('\t')
    rescount = -1
    printpreds = [actualclass,'|']
    for h in predlist:
        rescount += 1
        if h == max(predlist):
            output.write(typelist[rescount])
            output.write('\t')
            all_top.write(typelist[rescount])
            all_top.write('\t')
            printpreds.append(typelist[rescount])

    output.write(str(max(predlist)))
    all_top.write(str(max(predlist)))

    #output.write(answers[pancore.index(pancore[int(genomename1)])])
    output.write('\n')
    all_top.write('\n')

    for i in predlist:
        output1.write(str(i))
        output1.write('\t')
    output1.write('\n')



#for i in parselikelist:
#    parse_likelihoods.write(i)
#parse_likelihoods.close()


# Total evaluation:

output.close()
output1.close()
all_top.close()
#print 'Evaluating predictions'
#subprocess.Popen('python predictive_evaluation_new.py')

#print abe, len(parse_results)
inp = open('predictions_.txt').readlines()
for line in inp:
    output_true.write(line)

output_true.close()
