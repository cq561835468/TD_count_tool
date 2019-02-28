# -*- coding: cp936 -*-
import mssql_data
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
def  listtostring(a):
    stringb ='@'.join(a)
    #stringb = len(len(stringb))+stringb
    return stringb

def  stringtolist(a):
    listd = a.split('@')
    return listd

def unicokill(msg1):
    arr = []
    for i in range(len(msg1)):
        a=eval(repr(msg1[i])[1:])
        arr.append(a)
    return arr
