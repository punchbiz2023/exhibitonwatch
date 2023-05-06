import time



#----------------------- hours minutes and second
def get_hms(res):

	d2 = []
	for i in res:
	    #print(i.split('-',2))
	    for j in i:
	        d2.append(j)
	#print('d2: ',d2)
	l = d2[-9:]
	#print('l is: ',l)
	hms1 = ''    # it will store only hours:minute:seconds
	for i in l:
	    
	    if i.isdigit() == True:
	        hms1 += str(i)
	    
	    if len(hms1)==2 or len(hms1)==5:
	        hms1+=':'
	#print('hms1 is: ',hms1)
	#-----------------------------------
	l1 = d2[-8:]
	hms2 = ''
	for i in l1:
	    if i.isdigit() == True:
	        hms2 += str(i)
	    
	    if len(hms2)==2 or len(hms2)==5:
	        hms2+=':'
	#print('hms2 is: ',hms2)
	final_hms = ''
	try:
	    if int(hms1[0:2]) < int(24) and int(hms1[3:5]) <= int(59) and int(hms1[6:8])<= int(59):
	        #final_hms +=hms1
	        final_hms = hms1[0:2]+':'+hms1[3:5]+':'+hms1[6:8]
	        return final_hms
	    elif int(hms2[0:2]) < int(24) and int(hms2[3:5]) <= int(59) and int(hms2[6:8])<= int(59):
	        #final_hms +=hms2
	        final_hms = hms2[0:2]+':'+hms2[3:5]+':'+hms2[6:8]
	        return final_hms
	    else:
	        print('hours:minutes:seconds format are not matching.')

	except:
	    pass