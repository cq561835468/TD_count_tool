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
        sampleList1 = ['����1','����2','����3','����4','����5']
        self.choice_rule = wx.Choice(self, -1, (270, 352), choices=sampleList1) 
        self.choice_rule.SetSelection(0) 
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
        self.button5 = wx.Button(self, -1, "����excel", pos=(170, 350))
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
            version = '1.8.6'
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
            print returnmsg
            if returnmsg == 'fail':                            #��½ʧ��
                wx.FutureCall(1000,self.showfaillogin)
                usrname = self.usrname.GetValue()
                passwd = self.passwd.GetValue()                  
            elif returnmsg[:7] =='version':                #�汾̫��
                wx.FutureCall(1000,self.showfailversion) 
                returnmsg = returnmsg[7:]
                time.sleep(1)
                wx.MessageBox(returnmsg,'���°汾������Ϣ',wx.OK|wx.ICON_INFORMATION)        
            elif returnmsg =='timeout':                   #��ʱ
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
        #----------------ͳ��·�������Ԫ�س���--------------
        maxlen = 0
        for tl in arrw:
            if len(tl) > maxlen:
                maxlen = len(tl)   
        #-----------------д�볤��Ϊ5��Ԫ��-----------------
        for boss in arrw:
            if len(boss) == 5:
                c.append(boss)          #��ӽ�d
                i = arrw.index(boss)   #iΪ��Ԫ���������е�λ�ã��Դ����ڶ�λ����
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
                for child_num in d:                              #��D��ѭ����ȡ��λ��ֵ                 
                    if self.matchlen(boss_s, child_num, len(boss_s)) == "pass": #�������λ�а�������λ��ֵ������Ϊ������
                        i_boss = arrw.index(boss_s)          #������ϼ����������е�λ��
                        i_child = arrw.index(child_num)          #������¼����������е�λ��
                        value_child = arrwvalue[i_child]           #��ȡ�������ֵ
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
            arrw = ["pilotscaleexperiment_pilotscal","�������Ʒ��_�����������_moon50_1080p��Ƶ����","�������Ʒ��_�����������_moon50_4k�����������_","�������Ʒ��_�����������_moon50_4k�������������","�������Ʒ��_�����������_moon70_1080p��Ƶ����"]
            self.tree.DeleteAllItems()
            self.listBox2.Clear()#���listbox2
            f =self.listBox1.GetSelection()#��ȡ��ǰѡ������ݿ��
            self.mssql = self.listBox1.GetString(f) #ͨ���Ż�ȡ���ݿ���
            #print type(self.mssql )
            #print type(self.mssql)
            #print self.mssql
            #print type(arrw[1])
            #s = unicode(arrw[1], "gb2312")
            #print s
            #print self.mssql == s
            if self.mssql.encode("gb2312") in arrw:
                self.mssqls = self.mssql
            else:
                self.mssqls = self.mssql+ '_db'
            msg = ["time_td"]
            msg.append(self.mssqls)
            strmsg = socket_data.listtostring(msg) #listתstr
            print strmsg
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
            #print strmsg
            #wx.MessageBox(strmsg,'Info',wx.OK|wx.ICON_INFORMATION) 
            time_td =  socket_data.sendmsg(self.ips, self.port, strmsg) #����&&����
            #wx.MessageBox(time_td,'Info',wx.OK|wx.ICON_INFORMATION) 
            if time_td =='timeout':
                wx.FutureCall(1000,self.showtimeout)           
            else:
                msg1 = socket_data.stringtolist(time_td) #strתlist
                msg_num = msg1.index("$")
                self.msg_arrw1 = msg1[0:msg_num]
                self.msg_arrw2 = msg1[msg_num+1:]
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
                print strmsg
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
                self.select = self.choice_rule.GetSelection()
                msg = ['output']
                if self.select == 0:
                    msg.append('rule_1')
                elif self.select == 1:
                    msg.append('rule_2')
                elif self.select == 2:
                    msg.append('rule_3')                    
                elif self.select == 3:
                    msg.append('rule_4')  
                elif self.select == 4:
                    msg.append('rule_5')                      
                    self.button7.Enable()
                strmsg = socket_data.listtostring(msg)
                #print strmsg
                time_td =  socket_data.sendmsg(self.ips, self.port, strmsg) #����&&����
                print time_td
                if time_td == 'fail':
                    wx.FutureCall(1000,self.showfailbox) 
                else:
                    time_tds = time_td.replace(" ","_")                                 #�����ļ����пո�
                    self.doubletocsv_output(time_tds)
                    self.savedialog(event,time_tds)
                    wx.FutureCall(1000,self.showsusscebox) 
                    
    def  timestatistics(self,event):#ͳ�ư���ʱ��ִ�е�STEP
        try:
            if self.doyouwant == 1:
                repeat_i = "�Ƿ����������ִλ���ִ�"
                self.showvalue(repeat_i)     
            else:
                if self.select == 4:
                    self.button7.Enable()
                    wx.FutureCall(1000,self.showfailbox_nouse) 
                else:
                    msgs = 'output_picture'
                    #select = self.choice_rule.GetSelection()
                    #msg = ['output']
                    #if select == 0:
                        #msg.append('rule_1')
                    #elif select == 1:
                        #msg.append('rule_2')
                    #strmsgs = socket_data.listtostring(msg)
                    time_td =  socket_data.sendmsg(self.ips, self.port, msgs) #����&&����
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
    def showfailbox_nouse(self):  
        wx.MessageBox('�ù���Ŀǰ�����ã�','Info',wx.OK|wx.ICON_INFORMATION)          
    def showfaillogin(self):  
        wx.MessageBox('��½ʧ��','Info',wx.OK|wx.ICON_INFORMATION)      
    def showfailversion(self):  
        wx.MessageBox('��ǰ�汾���ɣ�����ϵ������Ա��ȡ���°汾��','Info',wx.OK|wx.ICON_INFORMATION)          
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
        
    def  doubletocsv(self,time_tds):   #txt����ת����д��csv�ļ� ͳ�ư���ʱ��ִ�е�STEP
        pathcsv = r'\\172.16.0.25\share\%s.txt' % time_tds          #������0.25�ϵ�txt�ļ�
        outcsv = r'\\172.16.0.25\share\%s.csv' % time_tds            #������0.25�ϵ�CSV�ļ�
        arrw = self.doublereplace(pathcsv)                                  #�滻�ر��ַ�
        os.remove(pathcsv)                                                         #ɾ��ԭ�ļ�
        self.excel_arrw = socket_data.timestat_excel(arrw)                                  #���ػ�ͼ�������� ʱ�� pass��fail����
        self.spitetxt(arrw, outcsv)
        
    def  doubletocsv_output(self,time_tds): #txt����ת����д��csv�ļ� ��������
        pathcsv = r'\\172.16.0.25\share\%s.txt' % time_tds          #������0.25�ϵ�txt�ļ�
        outcsv = r'\\172.16.0.25\share\%s.csv' % time_tds            #������0.25�ϵ�CSV�ļ�
        arrw = self.doublereplace(pathcsv)                                  #�滻�ر��ַ�
        os.remove(pathcsv)                                                          #ɾ��ԭ�ļ�
        if self.select == 4:
            arrw.insert(0, '������|���Ե�|���Ե���|���Ե�ִ��ʱ��|���Ե�ִ��ʱ��2|����ִ����Ա')
        self.spitetxt(arrw, outcsv)                                                 #�ָ�д��csv
        
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
            #----------------------------------�滻�ر��ַ�,��������
            #print line
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
    def  one_write(self,arrw,path):  #�ָ�д��csv
        fp = file(path)
        lines = []
        for line in fp: # ���õĵ�����, Ч�ʺܸ�
            lines.append(line)
        fp.close()
 
        lines.insert(1, 'a new line') # �ڵڶ��в���
        s = '\n'.join(lines)
        fp = file(path, 'w')
        fp.write(s)
        fp.close()     
        
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
        version = '1.8.6'
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
        print returnmsg
        if returnmsg == 'fail':
            pass
        else:
            msg1 = socket_data.stringtolist(returnmsg)#strתlist 
            for i in msg1:
                if i[-3:] =="_db":
                    self.listBox5.Append(i[:-3])  
                else:
                    self.listBox5.Append(i) 
    
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
        
class  TDthird(wx.Panel): #����3
    def __init__(self,parent):
        wx.Panel.__init__(self, parent)
        self.stat1=wx.StaticText(self,-1,"��Ŀ��",(50,15))#��Ŀ����ʾ��
        #self.stat2=wx.StaticText(self,-1,"��Ŀ",(50,200))#��Ŀ����ʾ7��     
        #self.stat3=wx.StaticText(self,-1,"������-������",(50,200))#��������ʾ��
        self.search=wx.StaticText(self,-1,"����",(420,15))#��Ŀ����ʾ��
        self.filtere = wx.TextCtrl(self, -1, "", pos=(450,10),size=(100, -1),style = wx.TE_PROCESS_ENTER) #�����ؼ�
        sampleList = []
        self.listBox1 = wx.ListBox (self, -1, (50, 40), (500, 140), sampleList,wx.LB_SINGLE)          #��Ŀ�ؼ�
        self.listBox2 = wx.ListBox (self, -1, (50, 190), (220, 140), sampleList,wx.LB_SINGLE)                #������
        self.tree = wx.TreeCtrl(self,pos=(290, 190),size=(260,140))                      #���Ե�
        self.button1 = wx.Button(self, -1, "�������в�������", pos=(130, 370))
        self.button2 = wx.Button(self, -1, "�������в��������ִ�ͳ��", pos=(330, 370))
        self.Bind(wx.EVT_PAINT,  self.autologin)  
        self.Bind(wx.EVT_LISTBOX,  self.timeget, self.listBox1)
        self.Bind(wx.EVT_LISTBOX,  self.sectimeget, self.listBox2)
        self.Bind(wx.EVT_BUTTON, self.out_feature3, self.button2)
        self.Bind(wx.EVT_BUTTON, self.out_feature3_alltest, self.button1)
        #--------------------���ؼ�     
        self.Bind(wx.EVT_TREE_SEL_CHANGED, self.thirdtimeget, self.tree)     
        self.doyouwant = 0 #�����жϷ�        
        #-----------------����
        self.Bind(wx.EVT_TEXT,self.filteres,self.filtere) 
        self.Bind(wx.EVT_TEXT_ENTER,self.filteres,self.filtere)         
        
    def  filteres(self,event):
        self.listBox1.Clear()
        self.text = self.filtere.GetValue()
        msgscr = socket_data.screening(self.msg1, self.text)
        print msgscr
        for i in msgscr:
            if i[-3:] =="_db":
                self.listBox1.Append(i[:-3])  
            else:
                self.listBox1.Append(i)  
    
    def  autologin(self,event):
        #print "����3======����autologin"
        global usrname
        global passwd
        global ip
        version = '1.8.6'
        #��ʼ���������ؼ�����
        #self.listBox1.Clear()
        #self.tree.DeleteAllItems()
        #-----------��ȡ����
        self.ips=ip
        self.port = 31500
        msg = ['login']
        #--------------------socketͨ��
        msg.append(usrname)
        msg.append(passwd)
        msg.append(version)
        strmsg = socket_data.listtostring(msg)
        returnmsg = socket_data.sendmsg(self.ips, self.port, strmsg)
        #print returnmsg
        if returnmsg == 'fail':
            pass
        else:
            self.msg1 = socket_data.stringtolist(returnmsg)#strתlist   
            for i in self.msg1:
                if i[-3:] =="_db":
                    self.listBox1.Append(i[:-3])  
                else:
                    self.listBox1.Append(i) 
        
    def timeget(self, event):#���listbox1�¼�---д��listbox2
        #try:
            #print "����3======����timeget"
            self.listBox2.Append("���в�����")
            arrw = ["pilotscaleexperiment_pilotscal"]
            self.listBox2.Clear()
            f =self.listBox1.GetSelection()#��ȡ��ǰѡ������ݿ��
            self.mssql = self.listBox1.GetString(f) #ͨ���Ż�ȡ���ݿ���
            if self.mssql in arrw:                           #�ж��Ƿ�Ϊ�������Ŀ����
                self.mssqls = self.mssql
            else:
                self.mssqls = self.mssql+ '_db'
            msg = ["feature4_first"] #���ͱ�ʾ
            msg.append(self.mssqls) #������ݿ���
            strmsg = socket_data.listtostring(msg) #listתstr
            time_td =  socket_data.sendmsg(self.ips, self.port, strmsg) #����&&����
            #print time_td
            if time_td =='timeout':
                wx.FutureCall(1000,self.showtimeout)                  #��ʱ����
            else:
                msg1 = socket_data.stringtolist(time_td) #strתlist
                for i in msg1:
                    self.listBox2.Append(i)
        #except:
            #print "error timeget"
            
    def  sectimeget(self, event):#���listbox2�¼�---д��listbox3
        #try: 
            #print "����3======����sectimeget"
            self.check_true = 1  #��ʶ�Ƿ�����listbox2��listbox3
            self.tree.DeleteAllItems()
            self.root = self.tree.AddRoot("���в��Ե�")         
            f =self.listBox2.GetSelection()#��ȡ��ǰѡ��Ķ���������
            self.secmssql = self.listBox2.GetString(f)#ͨ���Ż�ȡ��ǰ������Ŀ��
            #-----------------��Ϣ����-------------------------------
            msg = ["feature4_second"]
            msg.append(self.secmssql)
            strmsg = socket_data.listtostring(msg) #listתstr
            #print "����3======�ڶ��ε����Ŀ����������Ϊ��%s" % strmsg.encode("gb2312")
            #-------------------------------------------------------
            time_td =  socket_data.sendmsg(self.ips, self.port, strmsg) #����&&����
            if time_td =='timeout':
                wx.FutureCall(1000,self.showtimeout)           
            else:
                msg1 = socket_data.stringtolist(time_td) #strתlist
                msg_num = msg1.index("$")
                self.msg_arrw1 = msg1[0:msg_num]
                self.msg_arrw2 = msg1[msg_num+1:]
                print self.msg_arrw1
                print self.msg_arrw2
                self.treereset(self.msg_arrw2,self.msg_arrw1)
        #except:
            #print "error sectimeget"    
        
    def  thirdtimeget(self, event):#�μ��ִ�
        #try:
            #test = "���в��Ե�".encode("gb2312") 
            self.item = event.GetItem()
            self.thirdmssql = self.tree.GetItemText(self.item)
            self.thirdmssql_encode = self.thirdmssql.encode("gb2312")    
            if self.thirdmssql == "none_td":
                self.doyouwant = 1
            if self.thirdmssql_encode == "���в��Ե�":
                appendmsg = self.secmssql
            else:
                #===============��ȡpath==============
                valuemsg = self.msg_arrw1.index(str(self.thirdmssql_encode)) 
                appendmsg = self.msg_arrw2[valuemsg]
                self.doyouwant = 0
            #================����msg=======================
            msg = ["feature4_thrid"]
            msg.append(appendmsg)
            strmsg = socket_data.listtostring(msg) #listתstr
            print strmsg
            #================����=======================
            #print "����3====�����ε����Ŀ����������Ϊ��%s" % strmsg.encode("gb2312")
            time_td =  socket_data.sendmsg(self.ips, self.port, strmsg) #����&&����
            if time_td == "thok":
                pass
            elif time_td =='timeout':
                wx.FutureCall(1000,self.showtimeout)          
                
    #----------------------------------------------------------------------
    def  out_feature3(self,event):
        """����3======������"""    
        strmsg = "output_feature3"
        time_td =  socket_data.sendmsg(self.ips, self.port, strmsg) #����&&����
        #print time_td
        if time_td == "fail":
            wx.FutureCall(1000,self.showfailbox) 
        else:
            self.TD_one = TDapp(self)
            time_tds = time_td.replace(" ","_")                                 #�����ļ����пո�
            self.output_feature4(time_tds)   
            self.TD_one.savedialog(event,time_tds)
            wx.FutureCall(1000,self.showsusscebox)      
    #----------------------------------------------------------------------
    def  out_feature3_alltest(self,event):
        """����3======������====������"""    
        strmsg = "output_feature3_alltest"
        time_td =  socket_data.sendmsg(self.ips, self.port, strmsg) #����&&����
        #print time_td
        if time_td == "fail" or time_td == "timeout":
            wx.FutureCall(1000,self.showfailbox) 
        else:
            self.TD_one = TDapp(self)
            time_tds = time_td.replace(" ","_")                                 #�����ļ����пո�
            self.output_feature4_alltest(time_tds)   
            self.TD_one.savedialog(event,time_tds)
            wx.FutureCall(1000,self.showsusscebox)              
        
    def  output_feature4(self,time_tds): #txt����ת����д��csv�ļ�
        pathcsv = r'\\172.16.0.25\share\%s.txt' % time_tds          #������0.25�ϵ�txt�ļ�
        outcsv = r'\\172.16.0.25\share\%s.csv' % time_tds            #������0.25�ϵ�CSV�ļ�
        #print pathcsv
        #pathcsv = unicode(pathcsv , "utf8")
        arrw = self.TD_one.doublereplace(pathcsv)
        #========��ӡ=====
        title = '������|���Ե�|���Բ���|����ִ������|����ִ��ʱ��|����ִ�в���|����ִ�н��|pass����|failed����'
        return_arrw = socket_data.feature4_pass_and_fail(arrw,title)
        self.TD_one.spitetxt(return_arrw, outcsv) #�ָ��CSV���������0.25��
        os.remove(pathcsv)
        
    def  output_feature4_alltest(self,time_tds): #txt����ת����д��csv�ļ�
        pathcsv = r'\\172.16.0.25\share\%s.txt' % time_tds          #������0.25�ϵ�txt�ļ�
        outcsv = r'\\172.16.0.25\share\%s.csv' % time_tds            #������0.25�ϵ�CSV�ļ�
        print "pathcsv"
        arrw = self.TD_one.doublereplace(pathcsv)
        arrw.insert(0,"ID|���Ե�|���Բ���|��������|���Խ��")
       # for i in arrw:
            #print i
        #========��ӡ=====
        self.TD_one.spitetxt(arrw, outcsv) #�ָ��CSV���������0.25��
        os.remove(pathcsv)
        
    def  treereset(self,arrw,arrwvalue):  #��������͹�ϵ����������
        c = []
        d = []  
        lang = 6          #��߼�·�����ȣ���ѭ���������
        main_lang = 6 #��߼�·������
        #----------------ͳ��·�������Ԫ�س���maxlen--------------
        maxlen = 0
        for tl in arrw:
            if len(tl) > maxlen:
                maxlen = len(tl)   
        #-----------------д�볤��Ϊ6��Ԫ��-----------------
        for boss in arrw:
            if len(boss) == 6:
                c.append(boss)          #��ӽ�d
                i = arrw.index(boss)   #iΪ��Ԫ���������е�λ�ã��Դ����ڶ�λ����
                value_boss = arrwvalue[i]
                exec("self.child"+str(i) +"=" + "self.tree.AppendItem(self.root, value_boss)")
        #---------------------��λC����λD֮��Ľ���-------------------------------
        while maxlen > lang or maxlen == lang:    #����ǰ·������lang����·����󳤶�maxlenʱ��ѭ��ֹͣ
            #--------------------------д��D���з��ϳ��ȵ�ֵ-------------------------
            for lenlang in arrw:                                 #ѭ����ȡ�����е�ֵ
                if len(lenlang) == lang:                        #����ֵ�ĳ����Ƿ����Ҫ��
                    d.append(lenlang)                            #����Ҫ���д��D������
            #-----------------------------------------------------------------------
            for boss_s in c:                                        #��C��ѭ����ȡ��λ��ֵ
                for child_num in d:                              #��D��ѭ����ȡ��λ��ֵ                 
                    if self.matchlen(boss_s, child_num, len(boss_s)) == "pass": #�������λ�а�������λ��ֵ������Ϊ������
                        i_boss = arrw.index(boss_s)          #������ϼ����������е�λ��
                        i_child = arrw.index(child_num)          #������¼����������е�λ��
                        value_child = arrwvalue[i_child]           #��ȡ�������ֵ
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
        
    def showtimeout(self):  
        wx.MessageBox('���糬ʱ��','Info',wx.OK|wx.ICON_INFORMATION)     
    def showsusscebox(self):  
        wx.MessageBox('�����ѵ�����','Info',wx.OK|wx.ICON_INFORMATION)
    def showfailbox(self):  
        wx.MessageBox('��������ʧ�ܣ�','Info',wx.OK|wx.ICON_INFORMATION)      
class aboutUI(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, '����',pos=(700, 250),size=(300, 300),style=wx.DEFAULT_FRAME_STYLE ^(wx.RESIZE_BORDER | wx.MINIMIZE_BOX|wx.MAXIMIZE_BOX))
        self.panel = wx.ScrolledWindow(self, -1)
        self.stat7=wx.StaticText(self.panel,-1,"  �汾: 1.8.6.20170614",(80,80))
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
        
        tabthrid = TDthird(self)
        tabthrid.SetBackgroundColour("#B0E0E6")
        self.AddPage(tabthrid, "����3")
        
        self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.OnPageChanged)
        self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGING, self.OnPageChanging)
        self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGING, self.OnPageChangied)
        
    def OnPageChanged(self, event):
        pass
    def OnPageChanging(self, event):
        pass
    def OnPageChangied(self, event):
        pass    
 
class DemoFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, 'TDϵͳ����ͳ�Ʒ�������1.8.6',pos=(500, 50),size=(600, 500),style=wx.DEFAULT_FRAME_STYLE ^(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))
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