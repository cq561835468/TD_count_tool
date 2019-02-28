import wx
import os
import sys
import socket_data
import excel
import shutil
import ConfigParser 
import time
global usrname 
global passwd
global ip
class TDapp(wx.Panel):
    def __init__(self,parent):
        wx.Panel.__init__(self, parent)
        #==============记住用户名===============
        self.save = wx.CheckBox(self,-1,'记住用户名密码',(30,70),(100,-1))
        self.conf = ConfigParser.ConfigParser() 
        self.conf.read("conf.ini")         
        str_value = self.conf.get("Saveinfo", "value")
        str_name = self.conf.get("Saveinfo", "name")
        str_passwd = self.conf.get("Saveinfo", "passwd")
        if str_value == "1":
            self.save.SetValue(True)
        else:
            str_name = ""
            str_passwd = ""
        #=====================================        
        wx.StaticText(self,-1,"TD工具服务器IP地址",(30,10))
        self.ip = wx.TextCtrl(self, -1, "172.16.121.11", pos=(30,40),size=(120, -1))
        self.ip.Enable(enable=False)
        wx.StaticText(self,-1,"用户名",(190,10))
        self.usrname = wx.TextCtrl(self, -1, str_name, pos=(190,40),size=(100, -1))
        wx.StaticText(self,-1,"密码",(310,10))
        self.passwd = wx.TextCtrl(self, -1, str_passwd, pos=(310,40),size=(100, -1),style=wx.TE_PASSWORD)
        #==============功能1提示区=============#
        self.stat1=wx.StaticText(self,-1,"",(200,390)) 
        #-----------------获取的所有数据库名
        wx.StaticText(self,-1,"项目名",(30,90))
        wx.StaticText(self,-1,"搜索",(400,82))
        self.filtere = wx.TextCtrl(self, -1, "", pos=(435,80),size=(100, -1),style = wx.TE_PROCESS_ENTER)
        sampleList = []
        self.listBox1 = wx.ListBox(self, -1, (30, 110), (505, 100), sampleList,wx.LB_SINGLE)
        #-----------------获取的所有主轮次
        wx.StaticText(self,-1,"轮次",(30,220))
        sampleList2 = []
        self.listBox2 = wx.ListBox(self, -1, (30, 240), (230, 100), sampleList2,wx.LB_SINGLE)
        #-----------------获取所有子轮次
        wx.StaticText(self,-1,"轮次子项",(300,220))    
        self.tree = wx.TreeCtrl(self,pos=(300, 240),size=(230,100))   
        self.Bind(wx.EVT_TREE_SEL_CHANGED, self.thirdtimeget, self.tree)        
        #-----------------按钮1，获取数据库
        self.button1 = wx.Button(self, -1, "登陆", pos=(450,35))
        #-----------------按钮4，统计重复执行用例条数
        self.button4 = wx.Button(self, -1, "统计重复用例", pos=(30, 350))
        #-----------------按钮5，导出excel
        self.button5 = wx.Button(self, -1, "导出excel", pos=(200, 350))
        #-----------------按钮6，打开共享文件夹
        #self.button6 = wx.Button(self, -1, "打开共享文件夹", pos=(330, 350))  
        #-----------------按钮7，统计按照时间执行的STEP
        self.button7 = wx.Button(self, -1, "统计时间点用例执行情况", pos=(350, 350))        
        #-----------------按钮登陆bind
        self.Bind(wx.EVT_BUTTON,  self.login, self.button1)
        #-----------------列表数据库
        self.Bind(wx.EVT_LISTBOX,  self.timeget, self.listBox1)
        #-----------------列表轮次
        self.Bind(wx.EVT_LISTBOX,  self.sectimeget, self.listBox2)
        #-----------------按钮按钮统计重复
        self.Bind(wx.EVT_BUTTON,  self.statistics, self.button4)
        #-----------------按钮导出数据库
        self.Bind(wx.EVT_BUTTON,  self.excelout, self.button5)
        #-----------------按钮打开共享文件夹
        #self.Bind(wx.EVT_BUTTON,  self.communion, self.button6) 
        #-----------------统计按照时间执行的STEP
        self.Bind(wx.EVT_BUTTON,  self.timestatistics, self.button7)         
        #-----------------搜索
        self.Bind(wx.EVT_TEXT,self.filteres,self.filtere) 
        self.Bind(wx.EVT_TEXT_ENTER,self.filteres,self.filtere) 
        self.doyouwant = 0 #变量判断符
        #self.timeout = 5
    def  login(self,event):
        try:
            global usrname
            global passwd
            global ip                
            version = '1.3.4'
            self.init_msgbox()
            self.ips=self.ip.GetValue()
            name = self.usrname.GetValue()
            passwd = self.passwd.GetValue()    
            box_value = self.save.GetValue()          #获取复选框状态
            self.port = 31500
            msg = ['login']
            msg.append(name)
            msg.append(passwd)
            msg.append(version)
            strmsg = socket_data.listtostring(msg)
            returnmsg = socket_data.sendmsg(self.ips, self.port, strmsg)
            if returnmsg == 'fail':
                wx.FutureCall(1000,self.showfaillogin)
                usrname = self.usrname.GetValue()
                passwd = self.passwd.GetValue()                  
            elif returnmsg =='version':
                wx.FutureCall(1000,self.showfailversion) 
            elif returnmsg =='timeout':
                wx.FutureCall(1000,self.showtimeout)             
            else:
                #-------------------------------记住密码-------------------
                if box_value == True:
                    self.conf.set("Saveinfo", "value","1")
                    self.conf.set("Saveinfo", "name",name)
                    self.conf.set("Saveinfo", "passwd",passwd)
                    self.conf.write(open('conf.ini', "r+"))
                else:
                    self.conf.set("Saveinfo", "value","0")
                    #self.conf.set("Saveinfo", "name","")
                    #self.conf.set("Saveinfo", "passwd","")
                    self.conf.write(open('conf.ini', "r+"))                                    
                #------------------------遍历写入---------------------------
                self.msg1 = socket_data.stringtolist(returnmsg)#str转list
                usrname = self.usrname.GetValue()
                passwd = self.passwd.GetValue()     
                ip = self.ip.GetValue()
                for i in self.msg1:
                    if i[-3:] =="_db":
                        self.listBox1.Append(i[:-3])  
                    else:
                        self.listBox1.Append(i)  
        except:
            wx.FutureCall(1000,self.showfaillogin)
    def  treereset(self,arrw,arrwvalue):  #给予数组和关系数组生成树
        c = []
        d = []  
        lang = 7 
        #----------------max--------------
        maxlen = 0
        for tl in arrw:
            if len(tl) > maxlen:
                maxlen = len(tl)   
        #-----------------写入长度为5的元素-----------------
        for boss in arrw:
            if len(boss) == 5:
                c.append(boss)          #添加进d
                i = arrw.index(boss)   #i为数组中的位置，以此命名用于定位对象
                value_boss = arrwvalue[i]
                exec("self.child"+str(i) +"=" + "self.tree.AppendItem(self.root, value_boss)")
        #---------------------上位C与下位D之间的交互-------------------------------
        while maxlen > lang or maxlen == lang:    #当当前lang超过最大长度时停止
            #--------------------------写入D所有符合长度的值-------------------------
            for lenlang in arrw:                                 #循环获取数组中的值
                if len(lenlang) == lang:                        #计算值的长度是否符合要求
                    d.append(lenlang)                            #符合要求就写入D数组中
            #-----------------------------------------------------------------------
            #print d
            for boss_s in c:                                        #从C中循环获取上位的值
                for child_num in d:                              #从C中循环获取下位的值                 
                    if self.matchlen(boss_s, child_num, len(boss_s)) == "pass": #如果该下位中包含了上位的值，代表为其子项
                        i_boss = arrw.index(boss_s)          #计算该上级所在数组中的位置
                        i_child = arrw.index(child_num)          #计算该下级所在数组中的位置
                        value_child = arrwvalue[i_child]
                        exec("self.child"+str(i_child) +"=" + "self.tree.AppendItem("+"self.child"+str(i_boss)+", value_child)")
            c = d                                                         #将D的值给予C 清空D
            d = []
            lang = lang + 2
        
        
    def  matchlen(self,value1,value2,num):#给予两个关系值判断前者是否为后者的父项
        valuematch = value2[0:num]
        if value1 in valuematch:
            return "pass"
        else:
            return "fail"
            
    def timeget(self, event):#listbox1事件--获取数据库号--获取所有轮次--写入listbox2
        try:
            arrw = ["pilotscaleexperiment_pilotscal"]
            self.tree.DeleteAllItems()
            self.listBox2.Clear()#清空listbox2
            f =self.listBox1.GetSelection()#获取当前选择的数据库号
            self.mssql = self.listBox1.GetString(f) #通过号获取数据库名
            if self.mssql in arrw:
                self.mssqls = self.mssql
            else:
                self.mssqls = self.mssql + '_db'
            msg = ["time_td"]
            msg.append(self.mssqls)
            strmsg = socket_data.listtostring(msg) #list转str
            time_td =  socket_data.sendmsg(self.ips, self.port, strmsg) #发送&&接收
            if time_td =='timeout':
                wx.FutureCall(1000,self.showtimeout)                  
            else:
                msg1 = socket_data.stringtolist(time_td) #str转list
                for i in msg1:
                    self.listBox2.Append(i)
        except:
            print "error timeget"


    def  sectimeget(self, event):#listbox2事件--获取数据库号--获取顶级轮次--次级轮次--写入listbox3
        #try:
            self.tree.DeleteAllItems()
            self.root = self.tree.AddRoot("轮次子项")
            f =self.listBox2.GetSelection()#获取当前选择的顶级轮次号
            self.secmssql = self.listBox2.GetString(f)#通过号获取当前顶级轮次名
            self.doyouwant = 1
            msg = ["sectime_td"]
            msg.append(self.secmssql)
            strmsg = socket_data.listtostring(msg) #list转str
            time_td =  socket_data.sendmsg(self.ips, self.port, strmsg) #发送&&接收
            if time_td =='timeout':
                wx.FutureCall(1000,self.showtimeout)           
            else:
                msg1 = socket_data.stringtolist(time_td) #str转list
                msg_num = msg1.index("$")
                print msg_num
                self.msg_arrw1 = msg1[0:msg_num]
                self.msg_arrw2 = msg1[msg_num+1:]
                for i in self.msg_arrw1:
                    print i
                print len(self.msg_arrw1)
                print len(self.msg_arrw2)
                self.treereset(self.msg_arrw2,self.msg_arrw1)
        #except:
            #print "error sectimeget"
            
    def  thirdtimeget(self, event):#次级轮次
        #try:
            self.item = event.GetItem()
            self.thirdmssql = self.tree.GetItemText(self.item)
            self.thirdmssql_encode = self.thirdmssql.encode("gb2312")    
            if self.thirdmssql == "none_td" or cmp(self.thirdmssql_encode, "轮次子项") == 0:
                self.doyouwant = 1
            else:
                valuemsg = self.msg_arrw1.index(str(self.thirdmssql_encode))      
                #print valuemsg
                appendmsg = self.msg_arrw2[valuemsg]
                self.doyouwant = 0
                msg = ["thirdtime_td"]
                msg.append(appendmsg)
                strmsg = socket_data.listtostring(msg) #list转str
                #print strmsg
                time_td =  socket_data.sendmsg(self.ips, self.port, strmsg) #发送&&接收
                if time_td == "thok":
                    pass
                elif time_td =='timeout':
                    wx.FutureCall(1000,self.showtimeout)                       
        #except :
            #print "error thirdtimeget"
            
    def statistics(self, event): #统计次数按钮
        msg = "statistics"
        if self.doyouwant == 1:
            repeat_i = "非法的用例主轮次或次轮次"
            self.showvalue(repeat_i)
        else:
            time_td =  socket_data.sendmsg(self.ips, self.port, msg)  #发送&&接收
            if time_td == "fail":
                value = "获取用例次数失败!"
                wx.FutureCall(1000,self.showstatfail)   
            else:
                repeat='重复执行的用例数为%s条'% time_td
                wx.MessageBox(repeat,'Info',wx.OK|wx.ICON_INFORMATION)
    def excelout(self, event): #导出按钮1
        #try:
            if self.doyouwant == 1:
                repeat_i = "非法的用例主轮次或次轮次"
                self.showvalue(repeat_i)  
            else:
                msg = 'output'
                print "数据发送_标签"
                time_td =  socket_data.sendmsg(self.ips, self.port, msg) #发送&&接收
                print time_td
                if time_td == 'fail':
                    wx.FutureCall(1000,self.showfailbox) 
                else:
                    time_tds = time_td.replace(" ","_")                                 #过滤文件名中空格
                    self.doubletocsv_output(time_tds)
                    self.savedialog(event,time_tds)
                    wx.FutureCall(1000,self.showsusscebox) 
        #except:
            #wx.FutureCall(1000,self.showfailbox) 
            
    #def  communion(self,event):#打开共享文件夹
        #ipp = "\\172.16.0.25\share"
        #os.system("explorer.exe %s" % ipp) 
    
    def  timestatistics(self,event):#统计按照时间执行的STEP
        try:
            if self.doyouwant == 1:
                repeat_i = "非法的用例主轮次或次轮次"
                self.showvalue(repeat_i)     
            else:
                msg = 'output_picture'
                time_td =  socket_data.sendmsg(self.ips, self.port, msg) #发送&&接收
                #print "按钮2返回值"
                #print time_td
                if time_td == 'fail':
                    wx.FutureCall(1000,self.showfailbox) 
                else:
                    time_tds = time_td.replace(" ","_")                                 #过滤文件名中空格
                    self.doubletocsv(time_tds)
                    self.savedialog(event,time_tds)
                    self.excel_charts_out(self.pathdst_cvs_excel, self.excel_arrw)        #输出做好的excel图形文件
                    wx.FutureCall(1000,self.showsusscebox) 
        except:
            wx.FutureCall(1000,self.showfailbox) 
    def showsusscebox(self):  
        wx.MessageBox('用例已导出！','Info',wx.OK|wx.ICON_INFORMATION)
    def showfailbox(self):  
        wx.MessageBox('用例导出失败！','Info',wx.OK|wx.ICON_INFORMATION)  
    def showfaillogin(self):  
        wx.MessageBox('登陆失败','Info',wx.OK|wx.ICON_INFORMATION)      
    def showfailversion(self):  
        wx.MessageBox('当前版本过旧，请更新至最新版本！','Info',wx.OK|wx.ICON_INFORMATION)          
    def showtimeout(self):  
        wx.MessageBox('网络超时！','Info',wx.OK|wx.ICON_INFORMATION) 
    def showstatfail(self):  
        wx.MessageBox('获取用例次数失败！','Info',wx.OK|wx.ICON_INFORMATION)     
    def showvalue(self,value):  
        wx.MessageBox(value,'Info',wx.OK|wx.ICON_INFORMATION)        
    def  filteres(self,event):
        self.init_msgbox()
        self.text = self.filtere.GetValue()
        msgscr = socket_data.screening(self.msg1, self.text)
        for i in msgscr:
            if i[-3:] =="_db":
                self.listBox1.Append(i[:-3])  
            else:
                self.listBox1.Append(i)  

    #----------------------------------------------------------------------
    def  init_msgbox(self):
        self.listBox1.Clear()
        self.listBox2.Clear()
        self.tree.DeleteAllItems()
        
    def  doubletocsv(self,time_tds):   #txt逗号转换，写入csv文件
        pathcsv = r'\\172.16.0.25\share\%s.txt' % time_tds          #保存在0.25上的txt文件
        outcsv = r'\\172.16.0.25\share\%s.csv' % time_tds            #保存在0.25上的CSV文件
        arrw = self.doublereplace(pathcsv)
        #os.remove(pathcsv)
        self.excel_arrw = socket_data.timestat_excel(arrw)                                  #返回画图所需数据 时间 pass和fail次数
        self.spitetxt(arrw, outcsv)
        
    def  doubletocsv_output(self,time_tds):
        pathcsv = r'\\172.16.0.25\share\%s.txt' % time_tds          #保存在0.25上的txt文件
        outcsv = r'\\172.16.0.25\share\%s.csv' % time_tds            #保存在0.25上的CSV文件
        arrw = self.doublereplace(pathcsv)
        os.remove(pathcsv)
        self.spitetxt(arrw, outcsv)
        
    def  savedialog(self,event,srcpath):    #文件保存对话框
        dlg = wx.FileDialog(
                    self, message="Save file as ...", defaultDir=os.getcwd(), 
                    defaultFile="", style=wx.SAVE
                    )        
        dlg.SetFilterIndex(2)
        pathcsv = r'\\172.16.0.25\share\%s.csv' % srcpath        
        if dlg.ShowModal() == wx.ID_OK:
            pathdst = dlg.GetPath()
            #print pathdst
            if pathdst[-4:] == ".csv":
                self.pathdst_cvs_excel = pathdst + '_chart.xls'
                shutil.move(pathcsv, pathdst)          #移动到指定路径
            else:
                pathdst_cvs = pathdst + '.csv'
                self.pathdst_cvs_excel = pathdst + '_chart.xls'
                shutil.move(pathcsv, pathdst_cvs)          #移动到指定路径            
        else:
            os.remove(pathcsv)
            raise ERROR
        dlg.Destroy()
    def  doublereplace(self,path):   #逗号替换函数
        linearrw = []
        #print path
        r = open(path,'r')
        line = r.readline()
        while line :
            #----------------------------------替换逗号,放入数组
            linedo = line.replace(',','，')
            linedo2 = linedo.replace('<html>','')
            linedo3 = linedo2.replace('<body>','')
            linedo4 = linedo3.replace('</body>','')
            linedo5 = linedo4.replace('</html>','')
            linedo6 = linedo5.replace(' 12:00AM','')
            linedo7 = linedo6.replace('<br>','')
            linedo8 = linedo7.replace('</b>','')
            linedo9 = linedo8.replace('<b>','')
            linearrw.append(linedo9)
            #--------------------------------------------------------
            line = r.readline()
        return linearrw
        #----------------------------------------------------------------------      
    def  spitetxt(self,arrw,path):  #分割写入csv
        import csv
        with open(path, 'wb') as csvfile:
            for i in arrw:
                spamwriter = csv.writer(csvfile,dialect='excel')  
                spi = i.split('|')       
                spamwriter.writerow(spi)    
    #----------------------------------------------------------------------
    def  excel_charts_out(self,pathdst_cvs_excel,excel_arrw):
        f = open(pathdst_cvs_excel, 'w')
        print "excel_arrw is %s" % excel_arrw
        print "pathdst_cvs_excel is %s" % pathdst_cvs_excel
        excel.excelChart(self.excel_arrw, pathdst_cvs_excel)
        f.close()
        
class  TDsec(wx.Panel): #功能2
    def __init__(self,parent):
        wx.Panel.__init__(self, parent)
        #[控件]==================TD服务器IP,用户名密码
        self.stat1=wx.StaticText(self,-1,"",(200,450))#功能1提示区        
        self.stat4=wx.StaticText(self,-1,"项目名",(110,200))#项目名提示区
        self.stat5=wx.StaticText(self,-1,"该用户执行的用例数",(265,200))#执行的用例数提示区
        self.stat6=wx.StaticText(self,-1,"该用户重复执行的用例数",(410,200))#重复的用例数提示区        
        #-----------------按钮6，打开共享文件夹
        #self.button6 = wx.Button(self, -1, "打开共享文件夹", pos=(30, 150))          
        #----------------按钮7，功能2
        self.button7 = wx.Button(self, -1, "确认", pos=(30,70))
        #----------------按钮8，功能2
        self.button8 = wx.Button(self, -1, "导出excel", pos=(30,110))        
        #-----------------功能二获取TD用户
        wx.StaticText(self,-1,"测试人员",(30,20))
        self.peo = wx.TextCtrl(self, -1, "", pos=(30,40),size=(130, -1))
        #-----------------功能二获取数据库
        wx.StaticText(self,-1,"项目名",(200,20))
        sampleList = []
        self.listBox5 = wx.CheckListBox (self, -1, (200, 40), (330, 140), sampleList,wx.LB_EXTENDED)     
        #-----------------功能二输出提示区
        self.listBox6 = wx.ListBox (self, -1, (30, 220), (200, 100), sampleList,wx.LB_SINGLE) 
        self.listBox7 = wx.ListBox (self, -1, (240, 220), (150, 100), sampleList,wx.LB_SINGLE) 
        self.listBox8 = wx.ListBox (self, -1, (400, 220), (150, 100), sampleList,wx.LB_SINGLE)         
        #=============================功能2函数关联
        #-----------------列表数据库
        #self.Bind(wx.EVT_LISTBOX,  self.timegetson, self.listBox4)
        #-----------------确认按钮
        self.Bind(wx.EVT_BUTTON,  self.repeoname, self.button7)   
        #-----------------列表6、7、8bink
        self.Bind(wx.EVT_LISTBOX,  self.CheckListBox6, self.listBox6)
        self.Bind(wx.EVT_LISTBOX,  self.CheckListBox7, self.listBox7)
        self.Bind(wx.EVT_LISTBOX,  self.CheckListBox8, self.listBox8)
        #-----------------按钮导出
        self.Bind(wx.EVT_BUTTON,  self.excelout2, self.button8)      
        #-----------------按钮打开共享文件夹
        #self.Bind(wx.EVT_BUTTON,  self.communion, self.button6)       
        #-----------------自动登陆
        self.Bind(wx.EVT_PAINT,  self.autologin)   
        
    def  autologin(self,event):
        global usrname
        global passwd
        global ip
        version = '1.3.4'
        self.listBox5.Clear()
        self.listBox6.Clear()
        self.listBox7.Clear()
        self.listBox8.Clear()
        self.stat1.SetLabel('')
        self.ips=ip
        self.port = 31500
        msg = ['login']
        msg.append(usrname)
        msg.append(passwd)
        msg.append(version)
        strmsg = socket_data.listtostring(msg)
        returnmsg = socket_data.sendmsg(self.ips, self.port, strmsg)
        if returnmsg == 'fail':
            pass
        else:
            msg1 = socket_data.stringtolist(returnmsg)#str转list                
            for i in msg1:
                self.listBox5.Append(i[:-3])  
    
    def  repeoname(self,event):
        msg = ['time_count']
        self.listBox6.Clear()
        self.listBox7.Clear()
        self.listBox8.Clear()
        self.testname = self.peo.GetValue ()
        self.poke = self.listBox5.GetCheckedStrings()        
        msg.append(self.testname)
        if self.poke == ():#未选择数据库
            self.stat1.SetLabel('请选择数据库!')
            wx.FutureCall(1000,self.showdata)  
        else:
            for i in self.poke:
                i_db = i + "_db"
                msg.append(i_db)
            strmsg = socket_data.listtostring(msg) #list转str
            #print strmsg
            time_td =  socket_data.sendmsg(self.ips, self.port, strmsg) #发送&&接收
            #print time_td
            time_td_list = socket_data.stringtolist(time_td) 
            new_msg = msg[2:]#删除前2个元素的列表
            for i in new_msg:
                if time_td_list[0] == 'none':
                    self.listBox6.Append(i)
                    self.listBox7.Append('none')
                    self.listBox8.Append('none')
                    del time_td_list[0]
                else:
                    self.listBox6.Append(i)
                    self.listBox7.Append(time_td_list[0])
                    self.listBox8.Append(time_td_list[1])
                    del time_td_list[0]
                    del time_td_list[0]
                
    def excelout2(self, event):       
        tdapp_n = TDapp(self)  #实例化类
        msg = 'output_two'
        time_td =  socket_data.sendmsg(self.ips, self.port, msg) #发送&&接收
        print time_td
        if time_td == 'fail':
            wx.FutureCall(1000,self.showfailbox) 
        else:
            time_tds = time_td.replace(" ","_")                                 #过滤文件名中空格
            tdapp_n.doubletocsv_output(time_tds)
            tdapp_n.savedialog(event, time_tds)
            #tdapp_n.doubletocsv(time_td)
            #tdapp_n.savedialog(event, time_td)
            wx.FutureCall(1000,self.showsusscebox)  
    #================功能二=checklist======================
    def  CheckListBox6(self,event):
        f =self.listBox6.GetSelection()
        self.listBox7.SetSelection(f)
        self.listBox8.SetSelection(f)
    def  CheckListBox7(self,event):
        f =self.listBox7.GetSelection()
        self.listBox6.SetSelection(f)
        self.listBox8.SetSelection(f)
    def  CheckListBox8(self,event):
        f =self.listBox8.GetSelection()
        self.listBox6.SetSelection(f)
        self.listBox7.SetSelection(f)           
    
    def showsusscebox(self):  
        wx.MessageBox('用例已导出！','Info',wx.OK|wx.ICON_INFORMATION)

    def showfailbox(self):  
        wx.MessageBox('用例导出失败','Info',wx.OK|wx.ICON_INFORMATION)  

    def showdata(self):  
        wx.MessageBox('请选择数据库!','Info',wx.OK|wx.ICON_INFORMATION)
        
class aboutUI(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, '关于',pos=(700, 250),size=(300, 300),style=wx.DEFAULT_FRAME_STYLE ^(wx.RESIZE_BORDER | wx.MINIMIZE_BOX|wx.MAXIMIZE_BOX))
        self.panel = wx.ScrolledWindow(self, -1)
        self.stat7=wx.StaticText(self.panel,-1,"  版本: 1.3.4.20151211",(80,80))
        self.stat8=wx.StaticText(self.panel,-1,"  作者: 中试部 陈琪",(80,110))
        self.stat8=wx.StaticText(self.panel,-1,"  邮箱: chen_qi@kedacom.com",(80,140))
        self.stat8=wx.StaticText(self.panel,-1,"  分机: 7776",(80,170))
        
class NotebookDemo(wx.Notebook):
    def __init__(self, parent):
        wx.Notebook.__init__(self, parent, id=wx.ID_ANY, style=
                             wx.BK_DEFAULT
                             #wx.BK_TOP 
                             #wx.BK_BOTTOM
                             #wx.BK_LEFT
                             #wx.BK_RIGHT
                             )
 
        tabOne = TDapp(self)
        tabOne.SetBackgroundColour("#B0E0E6")
        self.AddPage(tabOne, "功能1")
 
        tabTwo = TDsec(self)
        tabTwo.SetBackgroundColour("#B0E0E6")
        self.AddPage(tabTwo, "功能2")
        
        self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.OnPageChanged)
        self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGING, self.OnPageChanging)
 
    def OnPageChanged(self, event):
        pass
    def OnPageChanging(self, event):
        pass
    
 
class DemoFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, 'TD系统数据统计分析工具1.3.4',pos=(500, 50),size=(600, 500),style=wx.DEFAULT_FRAME_STYLE ^(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))
        panel = NotebookDemo(self)
        menuBar = wx.MenuBar()   #创建菜单栏
        filemenu = wx.Menu()         #项目1
        filemenu2 = wx.Menu()       #项目2
        filemenu3 = wx.Menu()       #项目3
        menuBar.Append(filemenu,"&关于")         #菜单1添加
        fitem = filemenu.Append(-1,"信息")          #项目1添加
        self.SetMenuBar(menuBar) #显示菜单        
        self.Bind(wx.EVT_MENU, self.about, fitem)
    
    def  about(self,event):
        frameabout = aboutUI()
        frameabout.Show()      

class logo(wx.Frame):   #logo图片类
    def __init__(self):
        wx.Frame.__init__(self, None, -1, '',pos=(500, 100),size=(200, 200),style =wx.FRAME_SHAPED|wx.SIMPLE_BORDER|wx.FRAME_NO_TASKBAR|wx.STAY_ON_TOP) 
        self.png = wx.Image('image\drag.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        w, h = self.png.GetWidth(), self.png.GetHeight()
        self.SetClientSize( (w, h) )     
        self.Bind(wx.EVT_PAINT,self.OnPaint)
        
    def OnPaint(self, evt):
        dc = wx.PaintDC(self)
        dc.DrawBitmap(self.png, 0,0, True)    
        time.sleep(3)
        self.OnExit()
        #-------------------输出功能界面
        frame = DemoFrame()
        frame.Center()
        frame.Show()        
    def OnExit(self):
        self.Close()    
if __name__ == "__main__":
    app = wx.App()
    frame2 = logo()
    frame2.Center()
    #time.sleep(3)
    frame2.Show()
    app.MainLoop()