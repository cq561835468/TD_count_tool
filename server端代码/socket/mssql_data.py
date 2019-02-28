import sys
import pymssql
import os
reload(sys)
sys.setdefaultencoding('utf-8')
def mssqldata(ip,name,passwd):
    conn = pymssql.connect(host=ip,user=name,password=passwd,charset="utf8")
    cursor = conn.cursor()
    service = []
    sql = u"select name from master.sys.databases where name!='master' and name!='model' and name!='msdb' and name!='ReportServer$TDSQLSERVER' and name!='ReportServer$TDSQLSERVERTempDB' and name!='ReportServer$TDSQLSERVERTempDB' and name!='tempdb'"
    cursor.execute(sql)
    for row in cursor.fetchall():
        for r in row:
            service.append(r)
    conn.close()
    return service

def groupnumson(ip,name,passwd,data,fathertime,num):
    conn = pymssql.connect(host=ip,user=name,password=passwd,charset="utf8")
    cursor = conn.cursor()
    sql = u"select CF_ITEM_PATH from %s.dbo.CYCL_FOLD where CF_ITEM_PATH like '%s'  and CF_ITEM_NAME = '%s'" % (data,fathertime,num)
    cursor.execute(sql)
    sql2 = cursor.fetchone()[0]
    conn.close()
    return sql2

def timedata(ip,name,passwd,data):
    conn = pymssql.connect(host=ip,user=name,password=passwd,charset="utf8")
    cursor = conn.cursor()
    service = []
    print "select CF_ITEM_NAME from %s.dbo.CYCL_FOLD where len(CF_ITEM_PATH)=5" % data
    cursor.execute("select CF_ITEM_NAME from %s.dbo.CYCL_FOLD where len(CF_ITEM_PATH)=5" % data)
    for row in cursor.fetchall():
        for r in row:
            service.append(r)
    conn.close()
    return service

def timedatason(ip,name,passwd,data,sontime):
    conn = pymssql.connect(host=ip,user=name,password=passwd,charset="utf8")
    cursor = conn.cursor()
    service = []
    sql = "SELECT CF_ITEM_NAME FROM %s.dbo.CYCL_FOLD where CF_ITEM_PATH like '%s' order by CF_ITEM_PATH " % ( data,sontime)
    cursor.execute(sql)
    for row in cursor.fetchall():
        for r in row:
            service.append(r)
    return service

def timedatason_path(ip,name,passwd,data,sontime):
    conn = pymssql.connect(host=ip,user=name,password=passwd,charset="utf8")
    cursor = conn.cursor()
    service = []
    sql = "SELECT CF_ITEM_PATH FROM %s.dbo.CYCL_FOLD where CF_ITEM_PATH like '%s' order by CF_ITEM_PATH " % ( data,sontime)
    cursor.execute(sql)
    for row in cursor.fetchall():
        for r in row:
            service.append(r)  
    conn.close()
    return service

def groupnum(ip,name,passwd,data,num):
    conn = pymssql.connect(host=ip,user=name,password=passwd,charset="utf8")
    cursor = conn.cursor()
    cursor.execute("select CF_ITEM_PATH from %s.dbo.CYCL_FOLD where CF_ITEM_NAME = '%s' and LEN(CF_ITEM_PATH)=5 " % (data,num))
    sql = cursor.fetchone()[0]
    conn.close()
    return sql

def excelout(ip,name,passwd,databases,group):
    conn = pymssql.connect(host=ip,user=name,password=passwd,charset="utf8")
    cursor = conn.cursor()
    sql2 = "truncate table tmp4"
    cursor.execute("use %s" % databases)
    sql = "exec dbo.tdrepeart @n='%s',@m='%s'" % (databases,group)
    print sql
    cursor.execute(sql2)
    cursor.execute(sql)
    conn.commit()
    conn.close()

def excelout_rule2(ip,name,passwd,databases,group):
    conn = pymssql.connect(host=ip,user=name,password=passwd,charset="utf8")
    cursor = conn.cursor()
    sql2 = "truncate table tmp4"
    cursor.execute("use %s" % databases)
    sql = "exec dbo.tdrepeart_fail @m='%s'" % group
    #print sql
    cursor.execute(sql2)
    cursor.execute(sql)
    conn.commit()
    conn.close()

def excelout_rule3(ip,name,passwd,databases,group):
    conn = pymssql.connect(host=ip,user=name,password=passwd,charset="utf8")
    cursor = conn.cursor()
    sql2 = "truncate table tmp4"
    cursor.execute("use %s" % databases)
    sql = "exec dbo.td_rule_3 @m='%s'" % group
    cursor.execute(sql2)
    cursor.execute(sql)
    conn.commit()
    conn.close()

def excelout_rule4(ip,name,passwd,databases,group):
    conn = pymssql.connect(host=ip,user=name,password=passwd,charset="utf8")
    cursor = conn.cursor()
    sql2 = "truncate table tmp4"
    cursor.execute("use %s" % databases)
    sql = "exec dbo.td_rule_4 @m='%s'" % group
    cursor.execute(sql2)
    cursor.execute(sql)
    conn.commit()
    conn.close()

def excelout_rule5(ip,name,passwd,databases,group):
    conn = pymssql.connect(host=ip,user=name,password=passwd,charset="utf8")
    cursor = conn.cursor()
    sql2 = "truncate table tmp_rule5"
    cursor.execute("use %s" % databases)
    sql = "exec dbo.td_rule_5 @a='%s'" % group
    print sql
    cursor.execute(sql2)
    cursor.execute(sql)
    conn.commit()
    conn.close()
    
def excelout_rule6(ip,name,passwd,databases,group):
    conn = pymssql.connect(host=ip,user=name,password=passwd,charset="utf8")
    cursor = conn.cursor()
    sql2 = "truncate table tmp_rule6"
    cursor.execute("use %s" % databases)
    sql = "exec dbo.td_rule_6 @m='%s'" % group
    print sql
    cursor.execute(sql2)
    cursor.execute(sql)
    conn.commit()
    conn.close()    
    
def excelout_feature4(ip,name,passwd,path,databases):
    conn = pymssql.connect(host=ip,user=name,password=passwd,charset="utf8")
    cursor = conn.cursor()
    sql2 = "truncate table tmp7"
    cursor.execute("use %s" % databases)
    sql = "exec dbo.td_echo @path='%s',@table='%s'" % (path,databases)
    print sql
    cursor.execute(sql2)
    cursor.execute(sql)
    conn.commit()
    conn.close()
  
def excelout_feature4_alltest(ip,name,passwd,path,databases):
    conn = pymssql.connect(host=ip,user=name,password=passwd,charset="utf8")
    cursor = conn.cursor()
    sql2 = "truncate table tmp_alltest"
    cursor.execute("use %s" % databases)
    sql = "exec dbo.td_test_out @m='%s'" % path
    print sql
    cursor.execute(sql2)
    cursor.execute(sql)
    conn.commit()
    conn.close()
    
def excelout_pic(ip,name,passwd,databases,group):
    conn = pymssql.connect(host=ip,user=name,password=passwd,charset="utf8")
    cursor = conn.cursor()
    sql2 = "truncate table tmp4"
    cursor.execute("use %s" % databases)
    sql = "exec dbo.td_picture_all @m='%s'" % group
    print sql
    cursor.execute(sql2)
    cursor.execute(sql)
    conn.commit()
    conn.close()
    
def output(ip,name,passwd,databases,groupname,databasename):
    conn = pymssql.connect(host=ip,user=name,password=passwd,charset="utf8")   
    cursor = conn.cursor()
    databasename = databasename.replace(" ","_")
    groupname = groupname.replace(" ","_")     
    cursor.execute("use %s" % databases)
    sql = "EXEC master..xp_cmdshell 'BCP \"select * from %s.dbo.tmp4\" queryout C:\share\\%s.%s.txt -t \"|\" -c -U\"chenqi\" -P\"56183568\" -S\"172.16.0.25\\TDSQLSERVER\"'" % (databases,databasename,groupname)
    print sql
    sql2 = "truncate table tmp4"
    cursor.execute(sql)
    cursor.execute(sql2)
    conn.close()

def output_rule_5(ip,name,passwd,databases,groupname,databasename):
    conn = pymssql.connect(host=ip,user=name,password=passwd,charset="utf8")   
    cursor = conn.cursor()
    databasename = databasename.replace(" ","_")
    groupname = groupname.replace(" ","_")     
    cursor.execute("use %s" % databases)
    sql = "EXEC master..xp_cmdshell 'BCP \"select * from %s.dbo.tmp_rule5\" queryout C:\share\\%s.%s.txt -t \"|\" -c -U\"chenqi\" -P\"56183568\" -S\"172.16.0.25\\TDSQLSERVER\"'" % (databases,databasename,groupname)
    print sql
    sql2 = "truncate table tmp_rule5"
    cursor.execute(sql)
    cursor.execute(sql2)
    conn.close()
    
def output_rule_6(ip,name,passwd,databases,groupname,databasename):
    conn = pymssql.connect(host=ip,user=name,password=passwd,charset="utf8")   
    cursor = conn.cursor()
    databasename = databasename.replace(" ","_")
    groupname = groupname.replace(" ","_")     
    cursor.execute("use %s" % databases)
    sql = "EXEC master..xp_cmdshell 'BCP \"select * from %s.dbo.tmp_rule6\" queryout C:\share\\%s.%s.txt -t \"|\" -c -U\"chenqi\" -P\"56183568\" -S\"172.16.0.25\\TDSQLSERVER\"'" % (databases,databasename,groupname)
    print sql
    sql2 = "truncate table tmp_rule6"
    cursor.execute(sql)
    cursor.execute(sql2)
    conn.close()    

def output_feature4(ip,name,passwd,databases,groupname,databasename):
    conn = pymssql.connect(host=ip,user=name,password=passwd,charset="utf8")   
    cursor = conn.cursor()
    databasename = databasename.replace(" ","_")
    groupname = groupname.replace(" ","_")     
    cursor.execute("use %s" % databases)
    sql = "EXEC master..xp_cmdshell 'BCP \"select * from %s.dbo.tmp7\" queryout C:\share\\%s.%s_feature4.txt -t \"|\" -c -U\"chenqi\" -P\"56183568\" -S\"172.16.0.25\\TDSQLSERVER\"'" % (databases,databasename,groupname)
    sql2 = "truncate table tmp7"
    cursor.execute(sql)
    cursor.execute(sql2)
    conn.close()
    
def output_feature4_alltest(ip,name,passwd,databases,groupname,databasename):
    conn = pymssql.connect(host=ip,user=name,password=passwd,charset="utf8")   
    cursor = conn.cursor()
    databasename = databasename.replace(" ","_")
    groupname = groupname.replace(" ","_")     
    cursor.execute("use %s" % databases)
    sql = "EXEC master..xp_cmdshell 'BCP \"select * from %s.dbo.tmp_alltest\" queryout C:\share\\%s.%s_feature4_alltest.txt -t \"|\" -c -U\"chenqi\" -P\"56183568\" -S\"172.16.0.25\\TDSQLSERVER\"'" % (databases,databasename,groupname)
    sql2 = "truncate table tmp_alltest"
    cursor.execute(sql)
    cursor.execute(sql2)
    conn.close()
    
def statistics(ip,name,passwd,databases,group):
    conn = pymssql.connect(host=ip,user=name,password=passwd,charset="utf8")
    cursor = conn.cursor()
    cursor.execute("use %s" % databases)
    sqlsv = "exec dbo.tdcount @n='%s',@m='%s'" % (databases,group)
    cursor.execute(sqlsv)
    sql = cursor.fetchone()[0]
    conn.commit()
    conn.close()
    return sql

def  repeonaoop(ip,name,passwd,databases,names):
    conn = pymssql.connect(host=ip,user=name,password=passwd,charset="utf8")
    cursor = conn.cursor()
    cursor.execute("select US_USERNAME from %s.dbo.USERS where US_USERNAME = '%s'" % (databases,names))
    sql = cursor.fetchone()
    conn.close()
    return sql
    
def  repeonnapop(ip,name,passwd,databases,names):
    conn = pymssql.connect(host=ip,user=name,password=passwd,charset="utf8")
    cursor = conn.cursor()
    cursor.execute("use %s" % databases)
    sql = "exec dbo.tdpap @n='%s',@testname='%s'" % (databases,names)
    #print sql
    sql2 = "truncate table tmp5"
    cursor.execute(sql2)
    cursor.execute(sql)
    sqll = cursor.fetchone()[0]
    conn.commit()
    conn.close()
    return sqll

def restep(ip,name,passwd,databases,names):
    conn = pymssql.connect(host=ip,user=name,password=passwd,charset="utf8")
    cursor = conn.cursor()
    cursor.execute("use %s" % databases)
    sql = "exec dbo.tdcount2 @n='%s',@testname='%s'" % (databases,names)
    cursor.execute(sql)
    sqll = cursor.fetchone()[0]
    conn.commit()
    conn.close()
    return sqll

def output2(ip,name,passwd,databases,databasesname,testnames):
    conn = pymssql.connect(host=ip,user=name,password=passwd,charset="utf8")
    cursor = conn.cursor()
    databasesname = databasesname.replace(" ","_")
    testnames = testnames.replace(" ","_")
    cursor.execute("use %s" % databases)
    sql = "EXEC master..xp_cmdshell 'BCP \"select * from testadmin_test_db.dbo.tmp5\" queryout C:\share\\%s.%s.sec.txt -t \"|\" -c -U\"chenqi\" -P\"56183568\"'" % (databasesname,testnames)
    #print sql
    sql2 = "truncate table testadmin_test_db.dbo.tmp5"
    cursor.execute(sql)
    cursor.execute(sql2)
    conn.commit()
    conn.close()

def outputtmp6(ip,name,passwd,databases,groupname,databasename):
    conn = pymssql.connect(host=ip,user=name,password=passwd,charset="utf8")   
    cursor = conn.cursor()
    databasename = databasename.replace(" ","_")
    groupname = groupname.replace(" ","_")     
    cursor.execute("use %s" % databases)
    sql = "EXEC master..xp_cmdshell 'BCP \"select * from %s.dbo.tmp6\" queryout C:\share\\%s.%s.picture.txt -t \"|\" -c -U\"chenqi\" -P\"56183568\"'" % (databases,databasename,groupname)
    sql2 = "truncate table tmp6"
    cursor.execute(sql)
    cursor.execute(sql2)
    conn.close()
    
def insertdatabases(ip,name,passwd,databases,sqlname):
    ses = 'sqlcmd -U %s -P %s -S %s -d %s -i"D:/TD/%s"' % (name,passwd,ip,databases,sqlname)
    print ses
    os.system('sqlcmd -U %s -P %s -S %s -d %s -i"D:/TD/%s"' % (name,passwd,ip,databases,sqlname))

#----------------------------------------------------------------------
def droppro(ip,name,passwd,databases,dropname):
    conn = pymssql.connect(host=ip,user=name,password=passwd,charset="utf8")
    cursor = conn.cursor()
    cursor.execute("use %s" % databases)
    sql = "drop Procedure dbo.%s" % dropname
    cursor.execute(sql)
    conn.commit()
    conn.close()

def resepo(ip,name,passwd,databases,tablename):
    conn = pymssql.connect(host=ip,user=name,password=passwd,charset="utf8")
    cursor = conn.cursor()
    cursor.execute("use %s" % databases)
    sql = "exec dbo.tablecreat @data='%s',@tmp='%s'" % (databases,tablename)
    cursor.execute(sql)
    conn.commit()
    conn.close()

def resepo2(ip,name,passwd,databases,tablename):
    conn = pymssql.connect(host=ip,user=name,password=passwd,charset="utf8")
    cursor = conn.cursor()
    cursor.execute("use %s" % databases)
    sql = "exec dbo.tablecreattmp4 @data='%s',@tmp='%s'" % (databases,tablename)
    #print sql
    cursor.execute(sql)
    conn.commit()
    conn.close()

def resepo3(ip,name,passwd,databases,tablename):
    conn = pymssql.connect(host=ip,user=name,password=passwd,charset="utf8")
    cursor = conn.cursor()
    cursor.execute("use %s" % databases)
    sql = "exec dbo.tablecreattmp7 @data='%s',@tmp='%s'" % (databases,tablename)
    #print sql
    cursor.execute(sql)
    conn.commit()
    conn.close()
    
def resepo3_alltest(ip,name,passwd,databases):
    conn = pymssql.connect(host=ip,user=name,password=passwd,charset="utf8")
    cursor = conn.cursor()
    cursor.execute("use %s" % databases)
    sql = "exec dbo.tablecreattmp_alltest"
    cursor.execute(sql)
    conn.commit()
    conn.close()
    
def resepo_rule_5(ip,name,passwd,databases):
    conn = pymssql.connect(host=ip,user=name,password=passwd,charset="utf8")
    cursor = conn.cursor()
    cursor.execute("use %s" % databases)
    sql = "exec dbo.tablecreate_tmp_rule5"
    cursor.execute(sql)
    conn.commit()
    conn.close()

def resepotmp6(ip,name,passwd,databases,tablename):
    conn = pymssql.connect(host=ip,user=name,password=passwd,charset="utf8")
    cursor = conn.cursor()
    cursor.execute("use %s" % databases)
    sql = "exec dbo.tablecreattmp6 @data='%s',@tmp='%s'" % (databases,tablename)
    cursor.execute(sql)
    conn.commit()
    conn.close()
    
def resepo_rule_6(ip,name,passwd,databases):
    conn = pymssql.connect(host=ip,user=name,password=passwd,charset="utf8")
    cursor = conn.cursor()
    cursor.execute("use %s" % databases)
    sql = "exec dbo.tablecreattmp_rule6"
    cursor.execute(sql)
    conn.commit()
    conn.close()
    
def tablelive(ip,name,passwd,databases,tablename):
    conn = pymssql.connect(host=ip,user=name,password=passwd,charset="utf8")
    cursor = conn.cursor()
    service = []
    cursor.execute("use %s" % databases)
    cursor.nextset()
    sql = "exec dbo.ifrelivetable @data='%s',@tablename ='%s'" % (databases,tablename)
    cursor.execute(sql)
    sql2 = cursor.fetchone()
    service.append(sql2)
    if service != [None]:
        sql3 = "drop table %s" % tablename
        cursor.execute(sql3)
        #print "drop %s" % tablename
    conn.commit()
    conn.close()
    
def savelive(ip,name,passwd,databases,savename):
    conn = pymssql.connect(host=ip,user=name,password=passwd,charset="utf8")
    cursor = conn.cursor()
    service = []
    cursor.execute("use %s" % databases)
    cursor.nextset()
    sql = "exec dbo.ifsaverelive @save ='%s'" % savename
    cursor.execute(sql)
    sql2 = cursor.fetchone()
    service.append(sql2)
    if service != [None]:
        sql3 = "drop Procedure dbo.%s" % savename
        cursor.execute(sql3)
    conn.commit()
    conn.close()
 
def initialise(a,b,ip, name, passwd, databasesgb,databases):
    insertdatabases(ip, name, passwd, databasesgb, "ifrelivetable.sql")
    insertdatabases(ip, name, passwd, databasesgb, "ifsaverelive.sql")
    for i in a:
        tablelive(ip, name, passwd, databases, i)
    for n in b:
        savelive(ip, name, passwd, databases, n)
    droppro(ip, name, passwd, databases, "ifrelivetable")
    droppro(ip, name, passwd, databases, "ifsaverelive")
    
    
def  feature4_AL_DESCRIPTION(ip,name,passwd,databases,names):
    conn = pymssql.connect(host=ip,user=name,password=passwd,charset="utf8")
    service = []
    cursor = conn.cursor()
    cursor.execute("use %s" % databases)
    sql = "exec dbo.feature4_AL_DESCRIPTION @tablebase ='%s'" % names
    #print sql
    cursor.execute(sql)
    for row in cursor.fetchall():
        for r in row:
            service.append(r)
    return service

def  feature4_second_name(ip,name,passwd,databases,names):
    conn = pymssql.connect(host=ip,user=name,password=passwd,charset="utf8")
    service = []
    cursor = conn.cursor()
    cursor.execute("use %s" % databases)
    sql = "exec dbo.feature4_second_name @tablebase ='%s',@name='%s'" % (databases,names)
    cursor.execute(sql)
    for row in cursor.fetchall():
        for r in row:
            service.append(r)
    return service

def  feature4_second_path(ip,name,passwd,databases,names):
    conn = pymssql.connect(host=ip,user=name,password=passwd,charset="utf8")
    service = []
    cursor = conn.cursor()
    cursor.execute("use %s" % databases)
    sql = "exec dbo.feature4_second_path @tablebase ='%s',@name='%s'" % (databases,names)
    cursor.execute(sql)
    for row in cursor.fetchall():
        for r in row:
            service.append(r)
    return service

def req_path_3(ip,name,passwd,data,names):
    conn = pymssql.connect(host=ip,user=name,password=passwd,charset="utf8")
    cursor = conn.cursor()
    sql = u"SELECT [AL_ABSOLUTE_PATH] FROM %s.[dbo].[ALL_LISTS] where AL_DESCRIPTION = '%s'" % (data,names)
    cursor.execute(sql)
    sql2 = cursor.fetchone()[0]
    conn.close()
    return sql2