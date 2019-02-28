#coding=utf-8
import socket
import sys
import mssql_data
import socket_lamp
import thread
import ConfigParser 
import time
conf = ConfigParser.ConfigParser() 
conf.read("conf.ini") 
str_name = conf.get("Serverparameter", "sqlname")  
str_ip = conf.get("Serverparameter", "serverip")  
str_passwd = conf.get("Serverparameter", "sqlpasswd")  
int_port = conf.getint("Serverparameter", "serverport")  
int_listen = conf.getint("Serverparameter", "listen") 
version_one = conf.getint("Version", "version_one") 
version_two = conf.getint("Version", "version_two") 
version_three = conf.getint("Version", "version_three") 
#==========================================
address = ('', int_port)  
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
s.bind(address)  
s.listen(int_listen) 
#===========================================================
def journal(time,name,act):
    path_file = sys.path[0] + '\\journal.txt'
    paths_jor = '%s' % path_file    
    fileopen = open(paths_jor,'a')
    fileopen.writelines(['\n',time,' ',name,' ',act])
    fileopen.close()    
#==========================判断是否合法用户======
def decide(name,passwd):
    name_item = conf.items("UserName")
    for i in name_item:
        if i[1] == name:
            pass_item = conf.get("UserPasswd",i[0])
            if pass_item == passwd:
                return "pass"
    return "fail"

def versionget():
    conf = ConfigParser.ConfigParser() 
    conf.read("conf.ini")     
    version_one = conf.getint("Version", "version_one") 
    version_two = conf.getint("Version", "version_two") 
    version_three = conf.getint("Version", "version_three")     
    
def removersame(a): #处理同名数据
    count = 1
    for m in range(0,len(a)):
        for n in range(m+1,len(a)):
            if a[m] == a[n]:
                a[n] = a[n] + '('+str(count) + ')'
                count = count + 1
        count = 1
    return a

#----------------------------------------------------------------------
def  rec_file(txt):
    """获取文件内容"""
    file_object = open(txt)
    try:
         all_the_text = file_object.read()
    finally:
         file_object.close()        
         return all_the_text
#----------------------------------------------------------------------
def  send_msg(msg):
    """发送数据"""
    msg=msg+'*end*'
    ss.send(msg)

def mainaction(str_ip,str_name,str_passwd,ra):
#============================主循环=========
    global database
    global path_third_new    
    global path_new
    global data_third
    global count_name
    global nowtime
    global databasegb
    global path_req
#======================当前时间======================
    nowtime = time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time()))
    print "本次获取信息为：%s" % ra
#=============================================
    if ra == "statistics":
        try:
            arrw_table = []
            arrw_save = ["tdcount"]
            #print str_ip,str_name,str_passwd,database
            journal(nowtime, str_name, "用例重复统计")
            mssql_data.initialise(arrw_table, arrw_save,str_ip, str_name, str_passwd, databasegb,database)       #初始化函数   
            mssql_data.insertdatabases(str_ip, str_name, str_passwd, databasegb, "tdcount.sql")
            count = mssql_data.statistics(str_ip, str_name, str_passwd, database, path_third_new)
            mssql_data.initialise(arrw_table, arrw_save,str_ip, str_name, str_passwd, databasegb,database)       #初始化函数  
            count_str = str(count)
            send_msg(count_str)
        except:
            send_msg("fail")

    elif ra == "output_two":
        try:
            journal(nowtime, str_name, "功能2导出")
            mssql_data.output2(str_ip, str_name, str_passwd, "testadmin_test_db", "testadmin_test_db", count_name)
            returnmsg = 'testadmin_test_db.%s.sec' % count_name
            send_msg(returnmsg)
        except:
            send_msg("fail")    
    elif ra == "output_picture":  #图表导出
        try:
            arrw_table = ['tmp4']                        #放入需要判断的表名
            arrw_save = ['tablecreattmp4','td_picture_all']   #放入需要判断的存储过程名
            journal(nowtime, str_name, "功能1导出_规则2")          
            mssql_data.initialise(arrw_table, arrw_save,str_ip, str_name, str_passwd, databasegb,database)       #初始化函数   
            mssql_data.insertdatabases(str_ip, str_name, str_passwd, databasegb, "tablecreattmp4.sql")#导入tdrepearttmp存储过程
            mssql_data.insertdatabases(str_ip, str_name, str_passwd, databasegb, "td_picture_all.sql")#导入tdrepeart_fail存储过程
            mssql_data.resepo2(str_ip, str_name, str_passwd, database, 'tmp4')                   #创建表tmp4运行存储过程
            print 'test0'
            mssql_data.excelout_pic(str_ip, str_name, str_passwd, database, path_third_new)         #运行存储过程
            print 'test'
            mssql_data.output(str_ip, str_name, str_passwd, database, data_third, database)         #导出tmp4表
            print 'test2'
            mssql_data.initialise(arrw_table, arrw_save,str_ip, str_name, str_passwd, databasegb,database)       #初始化函数
            data_third_gb = data_third.encode('gb2312')
            returnmsg = '%s.%s' % (databasegb,data_third_gb)
            print returnmsg
            send_msg(returnmsg) 
        except:
            send_msg("fail") 
    elif ra == "output_feature3":
        try:
            print "功能3======点击out输出" 
            arrw_table = ['tmp7']                                  #需要删除的表 没有就空
            arrw_feature4_second = ["tablecreattmp7","td_echo"]   #需要删除的存储过程 根据下方上传的            
            #----------------初始化函数,删除表和存储过程-------------------------
            mssql_data.initialise(arrw_table, arrw_feature4_second,str_ip, str_name, str_passwd, databasegb,database)       
            #------------------------导入存储过程-------------------
            mssql_data.insertdatabases(str_ip, str_name, str_passwd, databasegb, "tablecreattmp7.sql")  
            mssql_data.insertdatabases(str_ip, str_name, str_passwd, databasegb, "td_echo.sql")  
            #------------------------处理数据----------------------
            #print "test"
            mssql_data.resepo3(str_ip, str_name, str_passwd, database, 'tmp7')                   #创建表tmp7
            print "%s,%s" % (path_req,database) 
            mssql_data.excelout_feature4(str_ip, str_name, str_passwd, path_req, database)         #运行存储过程
            mssql_data.output_feature4(str_ip, str_name, str_passwd, database, path_req, database)         #导出tmp4表
            #feature4_second_name = mssql_data.feature4_second_name(str_ip, str_name, str_passwd, database, point_name)      #功能4 获取name
            #feature4_second_path = mssql_data.feature4_second_path(str_ip, str_name, str_passwd, database, point_name)      #功能4 获取path
            #------------------------------------------------------
            mssql_data.initialise(arrw_table, arrw_feature4_second,str_ip, str_name, str_passwd, databasegb,database)  #初始化函数,删除表和存储过程
            print "功能3======点击out输出======完成" 
            req_msg_path = '%s.%s_feature4' % (database,path_req)
            send_msg(req_msg_path.encode('gb2312'))
        except:
            send_msg("fail")     
    elif ra == "output_feature3_alltest":
        try:
            print "功能3======点击out输出2" 
            arrw_table = ['tmp_alltest']                                  #需要删除的表 没有就空
            arrw_feature4_second = ["tablecreattmp_alltest","td_test_out"]   #需要删除的存储过程 根据下方上传的            
            #----------------初始化函数,删除表和存储过程-------------------------
            mssql_data.initialise(arrw_table, arrw_feature4_second,str_ip, str_name, str_passwd, databasegb,database)       
            #------------------------导入存储过程-------------------
            mssql_data.insertdatabases(str_ip, str_name, str_passwd, databasegb, "tablecreattmp_alltest.sql")  
            mssql_data.insertdatabases(str_ip, str_name, str_passwd, databasegb, "td_test_out.sql")  
            #------------------------处理数据----------------------
            mssql_data.resepo3_alltest(str_ip, str_name, str_passwd, database)                             #创建表tmp_alltest
            print "%s,%s" % (path_req,database) 
            mssql_data.excelout_feature4_alltest(str_ip, str_name, str_passwd, path_req, database)         #运行存储过程
            print "1"
            mssql_data.output_feature4_alltest(str_ip, str_name, str_passwd, database, path_req, database)         #导出tmp4表
            print "2"
            #feature4_second_name = mssql_data.feature4_second_name(str_ip, str_name, str_passwd, database, point_name)      #功能4 获取name
            #feature4_second_path = mssql_data.feature4_second_path(str_ip, str_name, str_passwd, database, point_name)      #功能4 获取path
            #------------------------------------------------------
            mssql_data.initialise(arrw_table, arrw_feature4_second,str_ip, str_name, str_passwd, databasegb,database)  #初始化函数,删除表和存储过程
            print "功能3======点击out输出所有测试用例======完成" 
            req_msg_path = '%s.%s_feature4_alltest' % (database,path_req)
            send_msg(req_msg_path.encode('gb2312'))
        except:
            send_msg("fail")       
#========================================================@判断
    elif '@' in ra:
        data = socket_lamp.stringtolist(ra)
        pass_data = data[0]   #标示字符
#=====================================登陆返回数据
        if pass_data == "login":
            print "登陆"
            journal(nowtime, data[1], "登陆")
            return_vl = decide(data[1],data[2] )   
            version = data[3]
            version_split = version.split('.')
            version_send_one = int(version_split[0])
            version_send_two = int(version_split[1])
            version_send_three = int(version_split[2])
            versionget()
            #===================版本判断===========
            ver_txt = rec_file("update.txt")
            if version_one > version_send_one:  #大版本号
                ver_txt_f = "version"+ver_txt 
                send_msg(ver_txt_f)
            else:
                if version_two > version_send_two: #中版本号
                    ver_txt_s = "version"+ver_txt 
                    send_msg(ver_txt_s)
                else:
                    print return_vl
                    if return_vl == "pass":
                        print str_ip
                        print str_name
                        print str_passwd
                        msg_login = mssql_data.mssqldata(str_ip,str_name,str_passwd)
                        msg_login_str = socket_lamp.listtostring(msg_login)
                        msg_login_str_encode = msg_login_str.encode("gb2312")
                        print msg_login_str_encode
                        send_msg(msg_login_str_encode)
                    else:
                        send_msg("fail")
#====================================第一box返回数据
        elif pass_data == "time_td":
            journal(nowtime, str_name, "项目控件点击")       
            database = data[1]
            #print database
            databasegb = data[1].encode("gb2312")
            #print databasegb
            msg_time = mssql_data.timedata(str_ip,str_name,str_passwd,database)
            if msg_time == []:
                send_msg("none_td")
                #print "time_None"
            msg_time_str = socket_lamp.listtostring(msg_time)
            msg_time_str_encode = msg_time_str.encode("ISO-8859-1")
            send_msg(msg_time_str_encode)
            #print "time_pass"
#===================================第二box返回数据
        elif pass_data == "sectime_td":
            journal(nowtime, str_name, "主轮次控件点击")           
            data_sec = data[1]
            #print data_sec
            path_sec = mssql_data.groupnum(str_ip, str_name, str_passwd, database, data_sec)
            path_new = path_sec + '%'
            msg_sectime = mssql_data.timedatason(str_ip, str_name, str_passwd, database, path_new)
            msg_sectime_path = mssql_data.timedatason_path(str_ip, str_name, str_passwd, database, path_new)
            msg_sectime.append("$")
            msg_sectime_all = msg_sectime + msg_sectime_path
            #print msg_sectime_all
            msg_sectime_remove = removersame(msg_sectime_all)
            msg_sectime_str = socket_lamp.listtostring(msg_sectime_remove)
            msg_sectime_str_encode = msg_sectime_str.encode("ISO-8859-1")
            send_msg(msg_sectime_str_encode)
            #print "sectime_pass"
#===================================第三box操作
        elif pass_data == "thirdtime_td":
            journal(nowtime, str_name, "下级控件轮次点击")         
            data_third = data[1]
            #path_third = mssql_data.groupnumson(str_ip, str_name, str_passwd, database, path_new, data_third)
            path_third_new = data_third + '%'
            #print path_third_new
            send_msg("thok")
#==================================功能2===确认====
        elif pass_data == "time_count":
            #print data
            journal(nowtime, str_name, "功能2确认")        
            count_name = data[1]
            returnlist_count = []
            for i in data[2:]:
                data_count_gb = i.encode("gb2312")
                data_poken = mssql_data.repeonaoop(str_ip, str_name, str_passwd, i, count_name)
                if data_poken == None:                   
                    returnlist_count.append("none")                
                else:
                    arrw_table = ['tmp5']
                    arrw_table_twp = ['']
                    arrw_save = ["tdpap",'tdcount2','tablecreat']                       
                    mssql_data.initialise(arrw_table, arrw_save,str_ip, str_name, str_passwd, data_count_gb,i)       #初始化函数,删除表和存储过程 data_count_gb为gb2312转码后数据库名 i为未转的
                    mssql_data.insertdatabases(str_ip, str_name, str_passwd, data_count_gb, "tdpap.sql") 
                    mssql_data.insertdatabases(str_ip, str_name, str_passwd, data_count_gb, "tdcount2.sql")
                    mssql_data.insertdatabases(str_ip, str_name, str_passwd, data_count_gb, "tablecreat.sql")
                    mssql_data.resepo(str_ip, str_name, str_passwd, i, 'tmp5')                                            #新建tmp5
                    step = mssql_data.repeonnapop(str_ip, str_name, str_passwd, i, count_name)                             #功能2写入tmp5该项目的测试用例step数，获取返回值
                    restep = mssql_data.restep(str_ip, str_name, str_passwd, i, count_name)                                #统计重复用例个数，获取返回值
                    mssql_data.initialise(arrw_table_twp, arrw_save,str_ip, str_name, str_passwd, data_count_gb,i)       #初始化函数  
                    returnlist_count.append(str(step))
                    returnlist_count.append(str(restep))
            returnlist_count_str = socket_lamp.listtostring(returnlist_count)
            print returnlist_count_str
            send_msg(returnlist_count_str)
        #功能3======================================
        elif pass_data == "feature4_first":  
            '''通过项目名称获取该项目下所有测试用例最高类'''
            database = data[1]
            databasegb = database.encode("gb2312")
            #print databasegb
            #print database
            print "功能3======第一次点击获取信息为：%s" % databasegb
            arrw_table = ['']                                  #需要删除的表 没有就空
            arrw_feature4_first = ["feature4_AL_DESCRIPTION"]   
            mssql_data.initialise(arrw_table, arrw_feature4_first,str_ip, str_name, str_passwd, databasegb,database)       #初始化函数,删除表和存储过程
            mssql_data.insertdatabases(str_ip, str_name, str_passwd, databasegb, "feature4_AL_DESCRIPTION.sql")  #导入存储过程
            AL_DESCRIPTION_req = mssql_data.feature4_AL_DESCRIPTION(str_ip, str_name, str_passwd, database, database)      #功能4 获取AL_DESCRIPTION列
            mssql_data.initialise(arrw_table, arrw_feature4_first,str_ip, str_name, str_passwd, databasegb,database)  #初始化函数,删除表和存储过程
            req_all = AL_DESCRIPTION_req
            req_all = removersame(req_all)
            req_all = socket_lamp.listtostring(req_all)
            req_all_str_encode = req_all.encode("ISO-8859-1")     
            print "功能3======第一次返回信息为：%s" % req_all_str_encode
            send_msg(req_all_str_encode)
        elif pass_data == "feature4_second":  
            '''通过最高类别获取该类别下所有子测试项'''
            #-------feature4_second@V1R5新功能----实例数据
            point_name = data[1]
            #print "databasegb is %s" % databasegb
            #print "测试项是：%s" % point_name.encode("gb2312")
            print "功能3======第二次点击获取信息为：表为 %s , 测试项为：%s" % (databasegb,point_name.encode("gb2312"))
            arrw_table = ['']                                  #需要删除的表 没有就空
            arrw_feature4_second = ["feature4_second_name","feature4_second_path"]   #需要删除的存储过程 根据下方上传的
            #----------------初始化函数,删除表和存储过程-------------------------
            mssql_data.initialise(arrw_table, arrw_feature4_second,str_ip, str_name, str_passwd, databasegb,database)       
            #------------------------导入存储过程-------------------
            mssql_data.insertdatabases(str_ip, str_name, str_passwd, databasegb, "feature4_second_name.sql")  
            mssql_data.insertdatabases(str_ip, str_name, str_passwd, databasegb, "feature4_second_path.sql")  
            #------------------------处理数据----------------------
            feature4_second_name = mssql_data.feature4_second_name(str_ip, str_name, str_passwd, database, point_name)      #功能4 获取name
            feature4_second_path = mssql_data.feature4_second_path(str_ip, str_name, str_passwd, database, point_name)      #功能4 获取path
            #------------------------------------------------------
            mssql_data.initialise(arrw_table, arrw_feature4_second,str_ip, str_name, str_passwd, databasegb,database)  #初始化函数,删除表和存储过程
            feature4_second_name.append('$')
            req_all = feature4_second_name + feature4_second_path
            req_all = removersame(req_all)
            req_all = socket_lamp.listtostring(req_all)
            req_all_str_encode = req_all.encode("ISO-8859-1")     
            #print "feature4_second返回值为：%s" % req_all_str_encode
            print "功能3======第二次返回信息为：%s" % req_all_str_encode
            send_msg(req_all_str_encode)        
        elif pass_data == "feature4_thrid":  
            '''通过最高类别获取该类别下所有子测试项'''
            #-------feature4_second@V1R5新功能----实例数据
            point_name = data[1]
            print "功能3======第三次点击获取信息为：表为 %s , 测试项为：%s" % (databasegb,point_name.encode("gb2312"))
            #path_req = mssql_data.req_path_3(str_ip, str_name, str_passwd, database, point_name) + '%'
            path_req = point_name + '%'
            print "功能3======返回路径为：%s" % path_req.encode("gb2312")
            print "功能3======第三次返回信息为：thok" 
            send_msg("thok")   
        elif pass_data == "output":
            try:
                choice  = data[1]
                if choice == 'rule_1':
                    arrw_table = ['tmp4']                        #放入需要判断的表名
                    arrw_save = ['tablecreattmp4','tdrepeart']   #放入需要判断的存储过程名
                    journal(nowtime, str_name, "功能1导出_规则1")          
                    mssql_data.initialise(arrw_table, arrw_save,str_ip, str_name, str_passwd, databasegb,database)       #初始化函数   
                    mssql_data.insertdatabases(str_ip, str_name, str_passwd, databasegb, "tablecreattmp4.sql")#导入tdrepearttmp存储过程
                    mssql_data.insertdatabases(str_ip, str_name, str_passwd, databasegb, "tdrepeart.sql")#导入tablecreat存储过程
                    mssql_data.resepo2(str_ip, str_name, str_passwd, database, 'tmp4')                   #创建表tmp4
                    mssql_data.excelout(str_ip, str_name, str_passwd, database, path_third_new)         #运行存储过程
                    mssql_data.output(str_ip, str_name, str_passwd, database, data_third, database)         #导出tmp4表
                    mssql_data.initialise(arrw_table, arrw_save,str_ip, str_name, str_passwd, databasegb,database)       #初始化函数
                    data_third_gb = data_third.encode('gb2312')
                    returnmsg = '%s.%s' % (databasegb,data_third_gb)
                    print "导出成功"
                    send_msg(returnmsg)
                elif choice == 'rule_2':
                    arrw_table = ['tmp4']                        #放入需要判断的表名
                    arrw_save = ['tablecreattmp4','tdrepeart_fail']   #放入需要判断的存储过程名
                    journal(nowtime, str_name, "功能1导出_规则2")          
                    mssql_data.initialise(arrw_table, arrw_save,str_ip, str_name, str_passwd, databasegb,database)       #初始化函数   
                    mssql_data.insertdatabases(str_ip, str_name, str_passwd, databasegb, "tablecreattmp4.sql")#导入tdrepearttmp存储过程
                    mssql_data.insertdatabases(str_ip, str_name, str_passwd, databasegb, "tdrepeart_fail.sql")#导入tdrepeart_fail存储过程
                    mssql_data.resepo2(str_ip, str_name, str_passwd, database, 'tmp4')                   #创建表tmp4
                    mssql_data.excelout_rule2(str_ip, str_name, str_passwd, database, path_third_new)         #运行存储过程
                    mssql_data.output(str_ip, str_name, str_passwd, database, data_third, database)         #导出tmp4表
                    mssql_data.initialise(arrw_table, arrw_save,str_ip, str_name, str_passwd, databasegb,database)       #初始化函数
                    data_third_gb = data_third.encode('gb2312')
                    returnmsg = '%s.%s' % (databasegb,data_third_gb)
                    print "导出成功"
                    send_msg(returnmsg)           
                elif choice == 'rule_3':
                    arrw_table = ['tmp4']                        #放入需要判断的表名
                    arrw_save = ['tablecreattmp4','td_rule_3']   #放入需要判断的存储过程名
                    journal(nowtime, str_name, "功能1导出_规则3")          
                    mssql_data.initialise(arrw_table, arrw_save,str_ip, str_name, str_passwd, databasegb,database)       #初始化函数   
                    mssql_data.insertdatabases(str_ip, str_name, str_passwd, databasegb, "tablecreattmp4.sql")#导入tdrepearttmp存储过程
                    mssql_data.insertdatabases(str_ip, str_name, str_passwd, databasegb, "td_rule_3.sql")#导入tdrepeart_fail存储过程
                    mssql_data.resepo2(str_ip, str_name, str_passwd, database, 'tmp4')                   #创建表tmp4
                    mssql_data.excelout_rule3(str_ip, str_name, str_passwd, database, path_third_new)         #运行存储过程
                    mssql_data.output(str_ip, str_name, str_passwd, database, data_third, database)         #导出tmp4表
                    mssql_data.initialise(arrw_table, arrw_save,str_ip, str_name, str_passwd, databasegb,database)       #初始化函数
                    data_third_gb = data_third.encode('gb2312')
                    returnmsg = '%s.%s' % (databasegb,data_third_gb)
                    print "导出成功"
                    send_msg(returnmsg)     
                elif choice == 'rule_4':
                    arrw_table = ['tmp4']                        #放入需要判断的表名
                    arrw_save = ['tablecreattmp4','td_rule_4']   #放入需要判断的存储过程名
                    journal(nowtime, str_name, "功能1导出_规则4")          
                    mssql_data.initialise(arrw_table, arrw_save,str_ip, str_name, str_passwd, databasegb,database)       #初始化函数   
                    mssql_data.insertdatabases(str_ip, str_name, str_passwd, databasegb, "tablecreattmp4.sql")#导入tdrepearttmp存储过程
                    mssql_data.insertdatabases(str_ip, str_name, str_passwd, databasegb, "td_rule_4.sql")#导入tdrepeart_fail存储过程
                    mssql_data.resepo2(str_ip, str_name, str_passwd, database, 'tmp4')                   #创建表tmp4
                    mssql_data.excelout_rule4(str_ip, str_name, str_passwd, database, path_third_new)         #运行存储过程
                    mssql_data.output(str_ip, str_name, str_passwd, database, data_third, database)         #导出tmp4表
                    mssql_data.initialise(arrw_table, arrw_save,str_ip, str_name, str_passwd, databasegb,database)       #初始化函数
                    data_third_gb = data_third.encode('gb2312')
                    returnmsg = '%s.%s' % (databasegb,data_third_gb)
                    print "导出成功"
                    send_msg(returnmsg)       
                elif choice == 'rule_5':
                    arrw_table = ['tmp_rule5']                        #放入需要判断的表名
                    arrw_save = ['tablecreate_tmp_rule5','td_rule_5']   #放入需要判断的存储过程名
                    journal(nowtime, str_name, "功能1导出_规则5")          
                    mssql_data.initialise(arrw_table, arrw_save,str_ip, str_name, str_passwd, databasegb,database)       #初始化函数   
                    mssql_data.insertdatabases(str_ip, str_name, str_passwd, databasegb, "tablecreate_tmp_rule5.sql")#导入tdrepearttmp存储过程
                    mssql_data.insertdatabases(str_ip, str_name, str_passwd, databasegb, "td_rule_5.sql")#导入tdrepeart_fail存储过程
                    mssql_data.resepo_rule_5(str_ip, str_name, str_passwd, database)                   #创建表tmp_rule5
                    mssql_data.excelout_rule5(str_ip, str_name, str_passwd, database, path_third_new)         #运行存储过程
                    mssql_data.output_rule_5(str_ip, str_name, str_passwd, database, data_third, database)         #导出tmp_rule5表
                    mssql_data.initialise(arrw_table, arrw_save,str_ip, str_name, str_passwd, databasegb,database)       #初始化函数
                    data_third_gb = data_third.encode('gb2312')
                    returnmsg = '%s.%s' % (databasegb,data_third_gb)
                    print "rule_5_导出成功"
                    send_msg(returnmsg)
                elif choice == 'rule_6':
                    arrw_table = ['tmp_rule6']                        #放入需要判断的表名
                    arrw_save = ['tablecreattmp_rule6','td_rule_6']   #放入需要判断的存储过程名
                    journal(nowtime, str_name, "功能1导出_规则6")          
                    mssql_data.initialise(arrw_table, arrw_save,str_ip, str_name, str_passwd, databasegb,database)       #初始化函数   
                    mssql_data.insertdatabases(str_ip, str_name, str_passwd, databasegb, 'tablecreattmp_rule6.sql')#导入tdrepearttmp存储过程
                    mssql_data.insertdatabases(str_ip, str_name, str_passwd, databasegb, 'td_rule_6.sql')#导入tdrepeart_fail存储过程
                    print 1
                    mssql_data.resepo_rule_6(str_ip, str_name, str_passwd, database)                   #创建表tmp_rule6
                    print 2
                    mssql_data.excelout_rule6(str_ip, str_name, str_passwd, database, path_third_new)         #运行存储过程
                    print 3
                    mssql_data.output_rule_6(str_ip, str_name, str_passwd, database, data_third, database)         #导出tmp_rule6表
                    print 4
                    mssql_data.initialise(arrw_table, arrw_save,str_ip, str_name, str_passwd, databasegb,database)       #初始化函数
                    data_third_gb = data_third.encode('gb2312')
                    returnmsg = '%s.%s' % (databasegb,data_third_gb)
                    print "rule_6_导出成功"
                    send_msg(returnmsg)                   
            except:
                send_msg("fail")        
        else:
            print "error1"
            send_msg('error')            
    else:
        print "error2"
        send_msg('error')
    
while True:
    print"begin"
    ss, addr = s.accept()  
    ra = ss.recv(16384)     
    thread.start_new_thread(mainaction, (str_ip,str_name,str_passwd,ra))
