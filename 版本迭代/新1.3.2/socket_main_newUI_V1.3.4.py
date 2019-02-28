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
        #==============��ס�û���===============
        self.save = wx.CheckBox(self,-1,'��ס�û�������',(30,70),(100,-1))
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
        wx.StaticText(self,-1,"TD���߷�����IP��ַ",(30,10))
        self.ip = wx.TextCtrl(self, -1, "172.16.121.11", pos=(30,40),size=(120, -1))
        self.ip.Enable(enable=False)
        wx.StaticText(self,-1,"�û���",(190,10))
        self.usrname = wx.TextCtrl(self, -1, str_name, pos=(190,40),size=(100, -1))
        wx.StaticText(self,-1,"����",(310,10))
        self.passwd = wx.TextCtrl(self, -1, str_passwd, pos=(310,40),size=(100, -1),style=wx.TE_PASSWORD)
        #==============����1��ʾ��=============#
        self.stat1=wx.StaticText(self,-1,"",(200,390)) 
        #-----------------��ȡ���������ݿ���
        wx.StaticText(self,-1,"��Ŀ��",(30,90))
        wx.StaticText(self,-1,"����",(400,82))
        self.filtere = wx.TextCtrl(self, -1, "", pos=(435,80),size=(100, -1),style = wx.TE_PROCESS_ENTER)
        sampleList = []
        self.listBox1 = wx.ListBox(self, -1, (30, 110), (505, 100), sampleList,wx.LB_SINGLE)
        #-----------------��ȡ���������ִ�
        wx.StaticText(self,-1,"�ִ�",(30,220))
        sampleList2 = []
        self.listBox2 = wx.ListBox(self, -1, (30, 240), (230, 100), sampleList2,wx.LB_SINGLE)
        #-----------------��ȡ�������ִ�
        wx.StaticText(self,-1,"�ִ�����",(300,220))    
        self.tree = wx.TreeCtrl(self,pos=(300, 240),size=(230,100))   
        self.Bind(wx.EVT_TREE_SEL_CHANGED, self.thirdtimeget, self.tree)        
        #-----------------��ť1����ȡ���ݿ�
        self.button1 = wx.Button(self, -1, "��½", pos=(450,35))
        #-----------------��ť4��ͳ���ظ�ִ����������
        self.button4 = wx.Button(self, -1, "ͳ���ظ�����", pos=(30, 350))
        #-----------------��ť5������excel
        self.button5 = wx.Button(self, -1, "����excel", pos=(200, 350))
        #-----------------��ť6���򿪹����ļ���
        #self.button6 = wx.Button(self, -1, "�򿪹����ļ���", pos=(330, 350))  
        #-----------------��ť7��ͳ�ư���ʱ��ִ�е�STEP
        self.button7 = wx.Button(self, -1, "ͳ��ʱ�������ִ�����", pos=(350, 350))        
        #-----------------��ť��½bind
        self.Bind(wx.EVT_BUTTON,  self.login, self.button1)
        #-----------------�б����ݿ�
        self.Bind(wx.EVT_LISTBOX,  self.timeget, self.listBox1)
        #-----------------�б��ִ�
        self.Bind(wx.EVT_LISTBOX,  self.sectimeget, self.listBox2)
        #-----------------��ť��ťͳ���ظ�
        self.Bind(wx.EVT_BUTTON,  self.statistics, self.button4)
        #-----------------��ť�������ݿ�
        self.Bind(wx.EVT_BUTTON,  self.excelout, self.button5)
        #-----------------��ť�򿪹����ļ���
        #self.Bind(wx.EVT_BUTTON,  self.communion, self.button6) 
        #-----------------ͳ�ư���ʱ��ִ�е�STEP
        self.Bind(wx.EVT_BUTTON,  self.timestatistics, self.button7)         
        #-----------------����
        self.Bind(wx.EVT_TEXT,self.filteres,self.filtere) 
        self.Bind(wx.EVT_TEXT_ENTER,self.filteres,self.filtere) 
        self.doyouwant = 0 #�����жϷ�
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
            box_value = self.save.GetValue()          #��ȡ��ѡ��״̬
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
                #-------------------------------��ס����-------------------
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
                #------------------------����д��---------------------------
                self.msg1 = socket_data.stringtolist(returnmsg)#strתlist
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
    def  treereset(self,arrw,arrwvalue):  #��������͹�ϵ����������
        c = []
        d = []  
        lang = 7 
        #----------------max--------------
        maxlen = 0
        for tl in arrw:
            if len(tl) > maxlen:
                maxlen = len(tl)   
        #-----------------д�볤��Ϊ5��Ԫ��-----------------
        for boss in arrw:
            if len(boss) == 5:
                c.append(boss)          #��ӽ�d
                i = arrw.index(boss)   #iΪ�����е�λ�ã��Դ��������ڶ�λ����
                value_boss = arrwvalue[i]
                exec("self.child"+str(i) +"=" + "self.tree.AppendItem(self.root, value_boss)")
        #---------------------��λC����λD֮��Ľ���-------------------------------
        while maxlen > lang or maxlen == lang:    #����ǰlang������󳤶�ʱֹͣ
            #--------------------------д��D���з��ϳ��ȵ�ֵ-------------------------
            for lenlang in arrw:                                 #ѭ����ȡ�����е�ֵ
                if len(lenlang) == lang:                        #����ֵ�ĳ����Ƿ����Ҫ��
                    d.append(lenlang)                            #����Ҫ���д��D������
            #-----------------------------------------------------------------------
            #print d
            for boss_s in c:                                        #��C��ѭ����ȡ��λ��ֵ
                for child_num in d:                              #��C��ѭ����ȡ��λ��ֵ                 
                    if self.matchlen(boss_s, child_num, len(boss_s)) == "pass": #�������λ�а�������λ��ֵ������Ϊ������
                        i_boss = arrw.index(boss_s)          #������ϼ����������е�λ��
                        i_child = arrw.index(child_num)          #������¼����������е�λ��
                        value_child = arrwvalue[i_child]
                        exec("self.child"+str(i_child) +"=" + "self.tree.AppendItem("+"self.child"+str(i_boss)+", value_child)")
            c = d                                                         #��D��ֵ����C ���D
            d = []
            lang = lang + 2
        
        
    def  matchlen(self,value1,value2,num):#����������ϵֵ�ж�ǰ���Ƿ�Ϊ���ߵĸ���
        valuematch = value2[0:num]
        if value1 in valuematch:
            return "pass"
        else:
            return "fail"
            
    def timeget(self, event):#listbox1�¼�--��ȡ���ݿ��--��ȡ�����ִ�--д��listbox2
        try:
            arrw = ["pilotscaleexperiment_pilotscal"]
            self.tree.DeleteAllItems()
            self.listBox2.Clear()#���listbox2
            f =self.listBox1.GetSelection()#��ȡ��ǰѡ������ݿ��
            self.mssql = self.listBox1.GetString(f) #ͨ���Ż�ȡ���ݿ���
            if self.mssql in arrw:
                self.mssqls = self.mssql
            else:
                self.mssqls = self.mssql + '_db'
            msg = ["time_td"]
            msg.append(self.mssqls)
            strmsg = socket_data.listtostring(msg) #listתstr
            time_td =  socket_data.sendmsg(self.ips, self.port, strmsg) #����&&����
            if time_td =='timeout':
                wx.FutureCall(1000,self.showtimeout)                  
            else:
                msg1 = socket_data.stringtolist(time_td) #strתlist
                for i in msg1:
                    self.listBox2.Append(i)
        except:
            print "error timeget"


    def  sectimeget(self, event):#listbox2�¼�--��ȡ���ݿ��--��ȡ�����ִ�--�μ��ִ�--д��listbox3
        #try:
            self.tree.DeleteAllItems()
            self.root = self.tree.AddRoot("�ִ�����")
            f =self.listBox2.GetSelection()#��ȡ��ǰѡ��Ķ����ִκ�
            self.secmssql = self.listBox2.GetString(f)#ͨ���Ż�ȡ��ǰ�����ִ���
            self.doyouwant = 1
            msg = ["sectime_td"]
            msg.append(self.secmssql)
            strmsg = socket_data.listtostring(msg) #listתstr
            time_td =  socket_data.sendmsg(self.ips, self.port, strmsg) #����&&����
            if time_td =='timeout':
                wx.FutureCall(1000,self.showtimeout)           
            else:
                msg1 = socket_data.stringtolist(time_td) #strתlist
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
            
    def  thirdtimeget(self, event):#�μ��ִ�
        #try:
            self.item = event.GetItem()
            self.thirdmssql = self.tree.GetItemText(self.item)
            self.thirdmssql_encode = self.thirdmssql.encode("gb2312")    
            if self.thirdmssql == "none_td" or cmp(self.thirdmssql_encode, "�ִ�����") == 0:
                self.doyouwant = 1
            else:
                valuemsg = self.msg_arrw1.index(str(self.thirdmssql_encode))      
                #print valuemsg
                appendmsg = self.msg_arrw2[valuemsg]
                self.doyouwant = 0
                msg = ["thirdtime_td"]
                msg.append(appendmsg)
                strmsg = socket_data.listtostring(msg) #listתstr
                #print strmsg
                time_td =  socket_data.sendmsg(self.ips, self.port, strmsg) #����&&����
                if time_td == "thok":
                    pass
                elif time_td =='timeout':
                    wx.FutureCall(1000,self.showtimeout)                       
        #except :
            #print "error thirdtimeget"
            
    def statistics(self, event): #ͳ�ƴ�����ť
        msg = "statistics"
        if self.doyouwant == 1:
            repeat_i = "�Ƿ����������ִλ���ִ�"
            self.showvalue(repeat_i)
        else:
            time_td =  socket_data.sendmsg(self.ips, self.port, msg)  #����&&����
            if time_td == "fail":
                value = "��ȡ��������ʧ��!"
                wx.FutureCall(1000,self.showstatfail)   
            else:
                repeat='�ظ�ִ�е�������Ϊ%s��'% time_td
                wx.MessageBox(repeat,'Info',wx.OK|wx.ICON_INFORMATION)
    def excelout(self, event): #������ť1
        #try:
            if self.doyouwant == 1:
                repeat_i = "�Ƿ����������ִλ���ִ�"
                self.showvalue(repeat_i)  
            else:
                msg = 'output'
                print "���ݷ���_��ǩ"
                time_td =  socket_data.sendmsg(self.ips, self.port, msg) #����&&����
                print time_td
                if time_td == 'fail':
                    wx.FutureCall(1000,self.showfailbox) 
                else:
                    time_tds = time_td.replace(" ","_")                                 #�����ļ����пո�
                    self.doubletocsv_output(time_tds)
                    self.savedialog(event,time_tds)
                    wx.FutureCall(1000,self.showsusscebox) 
        #except:
            #wx.FutureCall(1000,self.showfailbox) 
            
    #def  communion(self,event):#�򿪹����ļ���
        #ipp = "\\172.16.0.25\share"
        #os.system("explorer.exe %s" % ipp) 
    
    def  timestatistics(self,event):#ͳ�ư���ʱ��ִ�е�STEP
        try:
            if self.doyouwant == 1:
                repeat_i = "�Ƿ����������ִλ���ִ�"
                self.showvalue(repeat_i)     
            else:
                msg = 'output_picture'
                time_td =  socket_data.sendmsg(self.ips, self.port, msg) #����&&����
                #print "��ť2����ֵ"
                #print time_td
                if time_td == 'fail':
                    wx.FutureCall(1000,self.showfailbox) 
                else:
                    time_tds = time_td.replace(" ","_")                                 #�����ļ����пո�
                    self.doubletocsv(time_tds)
                    self.savedialog(event,time_tds)
                    self.excel_charts_out(self.pathdst_cvs_excel, self.excel_arrw)        #������õ�excelͼ���ļ�
                    wx.FutureCall(1000,self.showsusscebox) 
        except:
            wx.FutureCall(1000,self.showfailbox) 
    def showsusscebox(self):  
        wx.MessageBox('�����ѵ�����','Info',wx.OK|wx.ICON_INFORMATION)
    def showfailbox(self):  
        wx.MessageBox('��������ʧ�ܣ�','Info',wx.OK|wx.ICON_INFORMATION)  
    def showfaillogin(self):  
        wx.MessageBox('��½ʧ��','Info',wx.OK|wx.ICON_INFORMATION)      
    def showfailversion(self):  
        wx.MessageBox('��ǰ�汾���ɣ�����������°汾��','Info',wx.OK|wx.ICON_INFORMATION)          
    def showtimeout(self):  
        wx.MessageBox('���糬ʱ��','Info',wx.OK|wx.ICON_INFORMATION) 
    def showstatfail(self):  
        wx.MessageBox('��ȡ��������ʧ�ܣ�','Info',wx.OK|wx.ICON_INFORMATION)     
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
        
    def  doubletocsv(self,time_tds):   #txt����ת����д��csv�ļ�
        pathcsv = r'\\172.16.0.25\share\%s.txt' % time_tds          #������0.25�ϵ�txt�ļ�
        outcsv = r'\\172.16.0.25\share\%s.csv' % time_tds            #������0.25�ϵ�CSV�ļ�
        arrw = self.doublereplace(pathcsv)
        #os.remove(pathcsv)
        self.excel_arrw = socket_data.timestat_excel(arrw)                                  #���ػ�ͼ�������� ʱ�� pass��fail����
        self.spitetxt(arrw, outcsv)
        
    def  doubletocsv_output(self,time_tds):
        pathcsv = r'\\172.16.0.25\share\%s.txt' % time_tds          #������0.25�ϵ�txt�ļ�
        outcsv = r'\\172.16.0.25\share\%s.csv' % time_tds            #������0.25�ϵ�CSV�ļ�
        arrw = self.doublereplace(pathcsv)
        os.remove(pathcsv)
        self.spitetxt(arrw, outcsv)
        
    def  savedialog(self,event,srcpath):    #�ļ�����Ի���
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
                shutil.move(pathcsv, pathdst)          #�ƶ���ָ��·��
            else:
                pathdst_cvs = pathdst + '.csv'
                self.pathdst_cvs_excel = pathdst + '_chart.xls'
                shutil.move(pathcsv, pathdst_cvs)          #�ƶ���ָ��·��            
        else:
            os.remove(pathcsv)
            raise ERROR
        dlg.Destroy()
    def  doublereplace(self,path):   #�����滻����
        linearrw = []
        #print path
        r = open(path,'r')
        line = r.readline()
        while line :
            #----------------------------------�滻����,��������
            linedo = line.replace(',','��')
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
    def  spitetxt(self,arrw,path):  #�ָ�д��csv
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
        
class  TDsec(wx.Panel): #����2
    def __init__(self,parent):
        wx.Panel.__init__(self, parent)
        #[�ؼ�]==================TD������IP,�û�������
        self.stat1=wx.StaticText(self,-1,"",(200,450))#����1��ʾ��        
        self.stat4=wx.StaticText(self,-1,"��Ŀ��",(110,200))#��Ŀ����ʾ��
        self.stat5=wx.StaticText(self,-1,"���û�ִ�е�������",(265,200))#ִ�е���������ʾ��
        self.stat6=wx.StaticText(self,-1,"���û��ظ�ִ�е�������",(410,200))#�ظ�����������ʾ��        
        #-----------------��ť6���򿪹����ļ���
        #self.button6 = wx.Button(self, -1, "�򿪹����ļ���", pos=(30, 150))          
        #----------------��ť7������2
        self.button7 = wx.Button(self, -1, "ȷ��", pos=(30,70))
        #----------------��ť8������2
        self.button8 = wx.Button(self, -1, "����excel", pos=(30,110))        
        #-----------------���ܶ���ȡTD�û�
        wx.StaticText(self,-1,"������Ա",(30,20))
        self.peo = wx.TextCtrl(self, -1, "", pos=(30,40),size=(130, -1))
        #-----------------���ܶ���ȡ���ݿ�
        wx.StaticText(self,-1,"��Ŀ��",(200,20))
        sampleList = []
        self.listBox5 = wx.CheckListBox (self, -1, (200, 40), (330, 140), sampleList,wx.LB_EXTENDED)     
        #-----------------���ܶ������ʾ��
        self.listBox6 = wx.ListBox (self, -1, (30, 220), (200, 100), sampleList,wx.LB_SINGLE) 
        self.listBox7 = wx.ListBox (self, -1, (240, 220), (150, 100), sampleList,wx.LB_SINGLE) 
        self.listBox8 = wx.ListBox (self, -1, (400, 220), (150, 100), sampleList,wx.LB_SINGLE)         
        #=============================����2��������
        #-----------------�б����ݿ�
        #self.Bind(wx.EVT_LISTBOX,  self.timegetson, self.listBox4)
        #-----------------ȷ�ϰ�ť
        self.Bind(wx.EVT_BUTTON,  self.repeoname, self.button7)   
        #-----------------�б�6��7��8bink
        self.Bind(wx.EVT_LISTBOX,  self.CheckListBox6, self.listBox6)
        self.Bind(wx.EVT_LISTBOX,  self.CheckListBox7, self.listBox7)
        self.Bind(wx.EVT_LISTBOX,  self.CheckListBox8, self.listBox8)
        #-----------------��ť����
        self.Bind(wx.EVT_BUTTON,  self.excelout2, self.button8)      
        #-----------------��ť�򿪹����ļ���
        #self.Bind(wx.EVT_BUTTON,  self.communion, self.button6)       
        #-----------------�Զ���½
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
            msg1 = socket_data.stringtolist(returnmsg)#strתlist                
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
        if self.poke == ():#δѡ�����ݿ�
            self.stat1.SetLabel('��ѡ�����ݿ�!')
            wx.FutureCall(1000,self.showdata)  
        else:
            for i in self.poke:
                i_db = i + "_db"
                msg.append(i_db)
            strmsg = socket_data.listtostring(msg) #listתstr
            #print strmsg
            time_td =  socket_data.sendmsg(self.ips, self.port, strmsg) #����&&����
            #print time_td
            time_td_list = socket_data.stringtolist(time_td) 
            new_msg = msg[2:]#ɾ��ǰ2��Ԫ�ص��б�
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
        tdapp_n = TDapp(self)  #ʵ������
        msg = 'output_two'
        time_td =  socket_data.sendmsg(self.ips, self.port, msg) #����&&����
        print time_td
        if time_td == 'fail':
            wx.FutureCall(1000,self.showfailbox) 
        else:
            time_tds = time_td.replace(" ","_")                                 #�����ļ����пո�
            tdapp_n.doubletocsv_output(time_tds)
            tdapp_n.savedialog(event, time_tds)
            #tdapp_n.doubletocsv(time_td)
            #tdapp_n.savedialog(event, time_td)
            wx.FutureCall(1000,self.showsusscebox)  
    #================���ܶ�=checklist======================
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
        wx.MessageBox('�����ѵ�����','Info',wx.OK|wx.ICON_INFORMATION)

    def showfailbox(self):  
        wx.MessageBox('��������ʧ��','Info',wx.OK|wx.ICON_INFORMATION)  

    def showdata(self):  
        wx.MessageBox('��ѡ�����ݿ�!','Info',wx.OK|wx.ICON_INFORMATION)
        
class aboutUI(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, '����',pos=(700, 250),size=(300, 300),style=wx.DEFAULT_FRAME_STYLE ^(wx.RESIZE_BORDER | wx.MINIMIZE_BOX|wx.MAXIMIZE_BOX))
        self.panel = wx.ScrolledWindow(self, -1)
        self.stat7=wx.StaticText(self.panel,-1,"  �汾: 1.3.4.20151211",(80,80))
        self.stat8=wx.StaticText(self.panel,-1,"  ����: ���Բ� ����",(80,110))
        self.stat8=wx.StaticText(self.panel,-1,"  ����: chen_qi@kedacom.com",(80,140))
        self.stat8=wx.StaticText(self.panel,-1,"  �ֻ�: 7776",(80,170))
        
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
        self.AddPage(tabOne, "����1")
 
        tabTwo = TDsec(self)
        tabTwo.SetBackgroundColour("#B0E0E6")
        self.AddPage(tabTwo, "����2")
        
        self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.OnPageChanged)
        self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGING, self.OnPageChanging)
 
    def OnPageChanged(self, event):
        pass
    def OnPageChanging(self, event):
        pass
    
 
class DemoFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, 'TDϵͳ����ͳ�Ʒ�������1.3.4',pos=(500, 50),size=(600, 500),style=wx.DEFAULT_FRAME_STYLE ^(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))
        panel = NotebookDemo(self)
        menuBar = wx.MenuBar()   #�����˵���
        filemenu = wx.Menu()         #��Ŀ1
        filemenu2 = wx.Menu()       #��Ŀ2
        filemenu3 = wx.Menu()       #��Ŀ3
        menuBar.Append(filemenu,"&����")         #�˵�1���
        fitem = filemenu.Append(-1,"��Ϣ")          #��Ŀ1���
        self.SetMenuBar(menuBar) #��ʾ�˵�        
        self.Bind(wx.EVT_MENU, self.about, fitem)
    
    def  about(self,event):
        frameabout = aboutUI()
        frameabout.Show()      

class logo(wx.Frame):   #logoͼƬ��
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
        #-------------------������ܽ���
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