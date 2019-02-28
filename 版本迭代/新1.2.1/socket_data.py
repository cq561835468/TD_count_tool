import socket 
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
#----------------------------------------------------------------------
def  sendmsg(IP,port,msg):
    try:
        address = (IP, port)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
        s.settimeout(30)
        s.connect(address)
        s.send(msg)
        data = s.recv(8192)
        print data
        s.close() 
        return data
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
    for i in arrw: #2015/8/7/17_1.2.1
        if len(i) == 1:    
            continue
        num = 0
        spi = i.split('|') 
        time_num = spi[2]
        #print time_num
        if spi[1] =="Passed":
            passedvalue = passedvalue +1
        elif spi[1] == "Failed":
            failedvalue = failedvalue + 1
        if passedvalue !=0 or failedvalue != 0:
            if len(timearrw) == 0:
                timearrw.append(time_num)
                timearrw.append(passedvalue)
                timearrw.append(failedvalue)        
                passedvalue = 0
                failedvalue = 0             
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
    return timearrw

