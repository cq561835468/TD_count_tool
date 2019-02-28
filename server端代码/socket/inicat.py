import sys
import os
import ConfigParser 

conf = ConfigParser.ConfigParser() 
conf.read("conf.ini") 
#--------------------------------------------------------------
sections = conf.sections() 
#print sections
#options = conf.options("Serverparameter") 
#print options 
str_name = conf.get("Serverparameter", "sqlname")  
str_ip = conf.get("Serverparameter", "serverip")  
str_passwd = conf.get("Serverparameter", "sqlpasswd")  
int_port = conf.getint("Serverparameter", "serverport")  
int_listen = conf.getint("Serverparameter", "listen") 

#print str_name,str_ip,str_passwd,int_port,int_listen

def decide(name,passwd):
    name_item = conf.items("UserName")
    print name_item
    for i in name_item:
        if i[1] == name:
            #print "pass_name"
            pass_item = conf.get("UserPasswd",i[0])
            #print pass_item
            if pass_item == passwd:
                #print "pass_passwd"
                return "pass"
    return fail

decide("chenqi", "123456")