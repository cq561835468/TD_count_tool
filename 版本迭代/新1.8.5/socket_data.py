import socket 
import sys
import time
reload(sys)
sys.setdefaultencoding('utf-8')
#----------------------------------------------------------------------
def  sendmsg(IP,port,msg):
    try:
        datas = ''
        address = (IP, port)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
        s.settimeout(500)
        s.connect(address)
        s.send(msg)
        while True:
            data = s.recv(16384)
            #print data
            #print len(data)
            
            if '*end*' not in data:
                datas = datas + data
                #print "not end"
            
            elif '*end*'  in data:
                datas = datas + data
                #print "end"
                break
            
        s.close() 
        datas = datas[:-5]
        #print "data is %s" % datas
        return datas
    except:
        return "timeout"    
#----------------------------------------------------------------------
def  base64en(str):
    encoded = base64.b64encode(str)
    return encoded

#----------------------------------------------------------------------
def  base64de(str):
    decoded = base64.b64decode(str)
    return decoded 


#----------------------------------------------------------------------
def  listtostring(a):
    stringb ='@'.join(a)
    return stringb

#----------------------------------------------------------------------
def  stringtolist(a):
    listd = a.split('@')
    return listd

#----------------------------------------------------------------------
def  showtolist(a):
    listd = a.split('_')
    return listd

#----------------------------------------------------------------------
def  screening(arrw,value):    
    arrwscreed = []
    valutf = value.encode("gbk")
    for i in arrw: 
        i_big = i.lower()
        valutf_big = valutf.lower()
        if valutf_big in i_big:
            arrwscreed.append(i)
    return arrwscreed 

#-----------------------------------------------------------------------

def  timestat_excel(arrw):
    # return one arrw
    # one time 
    # two passed
    # three failed 
    timearrw = []
    passedvalue = 0
    failedvalue = 0
    del arrw[0]
    for i in arrw: #2015/8/7/17_1.2.1
        if len(i) == 1:    
            continue
        num = 0
        spi = i.split('|') 
        time_num = spi[5]  #date
        if spi[4] =="Passed":
            passedvalue = passedvalue +1
        elif spi[4] == "Failed":
            failedvalue = failedvalue + 1
        if passedvalue !=0 or failedvalue != 0:
            if len(timearrw) == 0:
                timearrw.append(time_num)
                timearrw.append(passedvalue)
                timearrw.append(failedvalue)        
                passedvalue = 0
                failedvalue = 0 
                print timearrw
            elif  time_num == timearrw[-3]:                             #same time
                timearrw[-2] = timearrw[-2] + passedvalue
                timearrw[-1] = timearrw[-1] + failedvalue
                passedvalue = 0
                failedvalue = 0
            else:
                timearrw.append(time_num)
                timearrw.append(passedvalue)
                timearrw.append(failedvalue)        
                passedvalue = 0
                failedvalue = 0   
    print timearrw
    return timearrw

#----------------------------------------------------------------------
def  feature4_pass_and_fail(arrw,title):
    """"""
    all_arrw = []
    max_n = 0
    all_arrw.append(title)
    arrw_new = arrw[1:]
    for i in arrw_new: #2016/3/1
        if len(i) == 1:    
            continue
        spi = i.split('|')
    #===================
        test_project = spi[0]          #need
        test_point = spi[1]             #need
        test_step = spi[3]               #need
        test_status = spi[4]
        test_time_data = spi[5]      #need
        test_time_time = spi[6]      #need
        test_step = spi[7]               #need
        test_exp = spi[8]                #need
        test_step_id = spi[9]
        test_id = str(int(spi[10]))
    #===================
        test_pass = 0                     #need
        test_fail = 0                       #need
        return_arrw = []
    #===================
        return_arrw = step_id_and_test_id(arrw_new, test_step_id, test_id)
        pass_and_fail = pass_fail_tongji(arrw_new, return_arrw)
        print "pass_and_fail is: %s" % pass_and_fail
        print "return_arrw is : %s" % return_arrw
        del return_arrw[0]
        for i in return_arrw:
            arrw_new[i] = 'x'
        return_value = test_project+'|'+test_point+'|'+test_step+'|'+test_time_data+'|'+test_time_time+'|'+test_step+'|'+test_exp+'|'+str(pass_and_fail[0])+'|'+str(pass_and_fail[1])
        all_arrw.append(return_value)
        
    return all_arrw
#----------------------------------------------------------------------
def  step_id_and_test_id(arrw,step_id,test_id):
    """"""
    arrw_step_id_re= []
    for i,element in enumerate(arrw): #2016/3/1
        ii = arrw[i]
        if len(ii) == 1:    
            continue
        spi = ii.split('|')
        test_step_id_local = spi[9]
        test_id_local = str(int(spi[10]))        
        #print "test_id_local is:(%s)" %  test_id_local
        #print "test_id is:(%s)" % test_id
        if test_id_local == test_id:
            #print "test_step_id_local is:%s" %  test_step_id_local
            #print "step_id is:%s" % step_id
            if step_id == test_step_id_local:
                arrw_step_id_re.append(i)
                
    return arrw_step_id_re
    
def  pass_fail_tongji(arrw,arrw2):
    """"""
    arrw_step_id_re= []
    pass_value = 0
    failed_value = 0            
    for i in arrw2:
        spi = arrw[i].split('|')
        #=====================
        test_status = spi[4] 
        #=====================
        if spi[4] == 'Passed':
            pass_value = pass_value + 1
        elif spi[4] == 'Failed':
            failed_value = failed_value + 1
    arrw_step_id_re.append(pass_value)
    arrw_step_id_re.append(failed_value)
    return arrw_step_id_re