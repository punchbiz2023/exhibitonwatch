import time
import re




def day_match(ss):
    """
    This function will get a string and try to match with possible string and will return a day name.
    """
    #print('ss is: ',ss)
    #print('inside the day matching function')
    list_mon = ['Mor','Mov','Mop']
    list_mon2 = ['on','Mo']
    list_tue = ['Iue','Hue','Vue']
    list_tue2 = ['Tu','ue']
    list_wed = ['Wcd','Wcy','Wad','Wcs','Wcu','Wcx','Wca',
                'Wex','Wes','Wci','Wej']
    list_wed2 = ['We','Wc','Wa','Wd']

    list_thu = ['Thv']
    list_thu2 = ['Th']
    list_fri = ['Fgi','Frl','Fti','Fci','Fxi','F','Fxi','Fr','Fvj','Fui']
    list_fri2 = ['F','Fr','Fv','Ftt']

    if len(ss) >= 3:
        ss = ss[0:3]
        
        if ss[0]=='M' and ss[2]=='n':
            return 'Mon'
        elif ss[0]=='M' and ss[1]=='o':
            return 'Mon'

        elif ss[0]=='T' and ss[2]=='e':
            return 'Tue'
        elif ss[0]=='T' and ss[1]=='u':
            return 'Tue'

        elif ss[0]=='W' and ss[2]=='d':
            return 'Wed'
        elif ss[0]=='W' and ss[1]=='e':
            return 'Wed'

        elif ss[0]=='T' and ss[2]=='u':
            return 'Thu'
        elif ss[0]=='T' and ss[1]=='h':
            return 'Thu'

        elif ss[0]=='F' and ss[2]=='i':
            return 'Fri'
        elif ss[0]=='F' and ss[1]=='r':
            return 'Fri'

        elif ss[0]=='S' and ss[2]=='t':
            return 'Sat'
        elif ss[0]=='S' and ss[1]=='a':
            return 'Sat'

        elif ss[0]=='S' and ss[2]=='n':
            return 'Sun'
        elif ss[0]=='S' and ss[1]=='u':
            return 'Sun'

        elif ss in list_mon:
            #print('Mon')
            
            return 'Mon'
            
        elif ss in list_tue:
            #print('Tue')
            return 'Tue'
            
        elif ss in list_wed:
            #print('Wed')
            return 'Wed'
            
        elif ss in list_thu:
            #print('Thu')
            return 'Thu'
            
        elif ss in list_fri:
            #print('Fri')
            return 'Fri'
        else:
            print(ss,' is not matching')
    else:

        if ss in list_mon2:
            return 'Mon'
        elif ss in list_tue2:
            return 'Tue'
        elif ss in list_wed2:
            return 'Wed'
        elif ss in list_thu2:
            return 'Thu'
        elif ss in list_fri2:    
            return 'Fri'


final_day = ''
def get_day(day_name):    # fetching day name
    global final_day
    d_string = re.findall(r"(\D{5})", day_name)
    #print('d_string is: ', d_string)
    if len(d_string)!=0:
        #print('fetched raw Day 1: ',d_string)
        sd = ''
        try:
            for i in d_string[0]:
                if i.isalpha()==True:
                    sd = sd+i
            #print('fetched Day: ',sd)
            final_day = day_match(sd)  #calling day matching fun
            #print('returned final day: ',final_day)
            return final_day
        except:
            pass
    elif len(d_string)==0:
        d_string_1 = re.findall(r"(\D{4})", day_name)
        #print('fetched raw Day 2: ',d_string_1)
        if len(d_string_1) != 0:
            sd = ''
            try:
                for i in d_string_1[0]:
                    if i.isalpha()==True:
                        sd = sd+i
                #print('fetched Day: ',sd)
                final_day = day_match(sd) #calling day matching fun
                return final_day
                #print('returned final day: ',final_day)
            except:
                pass
        else:
            pass