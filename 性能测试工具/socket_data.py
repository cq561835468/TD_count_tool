import socket 
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
#----------------------------------------------------------------------
def  sendmsg(IP,port,msg):
    address = (IP, port)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
    s.connect(address)
    s.send(msg)
    data = s.recv(8192)
    #print data
    return data
    s.close() 
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
        if valutf in i:
            arrwscreed.append(i)
    return arrwscreed 
