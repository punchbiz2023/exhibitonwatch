import time

current_year = time.strftime("%Y")

#fetching date and validating 
def get_date(date_str):

    try:
        #Date = res[0]
        Date = date_str
        s1 = Date[0:5]
        s2 = Date[0:2]+Date[3:5]
        s3 = Date[0:2]+Date[2:4]
    except:
        print('not able to fetch date from extracted data')
    #print(s2)
    year = '2022'
    final_date = ''
    try:
        if s1.isdigit()==True:
            #print(s1)
            s1 = s1.replace('z', '2')
            if int(s2[0:2])<32 and int(s2[2:4])<13:
                #print('fetched date: ',s2[0:2]+'-'+s2[2:4]+'-'+year)
                final_date = s2[0:2]+'-'+s2[2:4]+'-'+ current_year
                return final_date
        elif s2.isdigit()==True:
            #print(s2)
            if int(s2[0:2])<32 and int(s2[2:4])<13:
                #print('fetched date: ',s2[0:2]+'-'+s2[2:4]+'-'+year)
                final_date = s2[0:2]+'-'+s2[2:4]+'-'+ current_year
                return final_date
        elif s3.isdigit()==True:
            if int(s3[0:2])<32 and int(s3[2:4])<13:
                #print('fetched date: ',s2[0:2]+'-'+s2[2:4]+'-'+year)
                final_date = s3[0:2]+'-'+s3[2:4]+'-'+ current_year
                return final_date
    except:
        print('not able to process date....bcz of  too messy data')

    # try:
    #     # print('length of date is: ', len(final_date))
    #     # print('length of day is: ', len(final_day))
    #     # print('length of HMS is: ', len(final_hms))
    #     print('final date is: ', final_date)
    #     print('final day is: ', final_day)
    #     print('final HMS is: ', final_hms)
    # except:
    #     pass
