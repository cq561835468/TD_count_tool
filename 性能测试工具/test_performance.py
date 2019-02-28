import socket_data 
import ConfigParser 
import threading
import time

conf = ConfigParser.ConfigParser() 
conf.read("conf.ini") 
str_login = conf.get("sortchoose", "login") 
str_statistic = conf.get("sortchoose", "statistic")  
str_excelout = conf.get("sortchoose", "excelout")  
str_output_picture = conf.get("sortchoose", "output_picture")  
str_ip= conf.get("server_info", "ip")  
str_port = conf.get("server_info", "port")  
str_name = conf.get("server_info", "name")  
str_passwd = conf.get("server_info", "passwd")  
str_arrw_go = []
str_arrw_go.append(str_login)
str_arrw_go.append(str_statistic)
str_arrw_go.append(str_excelout)
str_arrw_go.append(str_output_picture)

#------------------------------向server发送信息----------------------------------------
########################################################################
class  send_msg(threading.Thread):
    def __init__(self, arrw, str_ip,str_port,str_name,str_passwd): 
        threading.Thread.__init__(self)
        self.arrw = arrw
        self.str_ip = str_ip
        self.str_port = str_port
        self.str_name = str_name
        self.str_passwd = str_passwd
        self.thread_stop = False  
    def  run(self): 
        while not self.thread_stop: 
            if self.arrw[0] == '1':
                msg = ['login'] 
                int_port = int(self.str_port)                           #端口转int
                msg.append(self.str_name)
                msg.append(self.str_passwd)        
                strmsg = socket_data.listtostring(msg)
                returnmsg = socket_data.sendmsg(self.str_ip, int_port, strmsg)
                if returnmsg == 'error':
                    print "login error"
                else:
                    print "login pass"
                    strmsg1 = "time_td@testadmin_test_db"
                    strmsg2 = "sectime_td@xxxx"
                    strmsg3 = "thirdtime_td@AAAAA"
                    returnmsg1 = socket_data.sendmsg(self.str_ip, int_port, strmsg1)
                    print returnmsg1
                    returnmsg2 = socket_data.sendmsg(self.str_ip, int_port, strmsg2)
                    print returnmsg2
                    returnmsg3 = socket_data.sendmsg(str_ip, int_port, strmsg3)
                    print returnmsg3
            if self.arrw[1] == '1':
                msg2 = "statistics"
                returnmsg4 = socket_data.sendmsg(self.str_ip, self.int_port, msg2)
                print returnmsg4
            if self.arrw[2] == '1':
                print "excelout"
            if self.arrw[3] == '1':
                print "output_picture"
            
    def stop(self):  
            self.thread_stop = True 
            
if __name__ == "__main__":
    thread1 = send_msg(str_arrw_go,str_ip,str_port,str_name,str_passwd)
    thread1.start()  
    time.sleep(30) 
    thread1.stop()  