import wx
import os
import sys
import socket_data 
import shutil
import ConfigParser 
import time
global usrname 
global passwd
global ip
class  login_frame(wx.Frame):#��½������
    def __init__(self):
        wx.Frame.__init__(self, None, -1, '��½����',pos=(500, 100),size=(400, 280)) 
        panel = wx.Panel(self)
        #==============��ס�û���===============
        self.save = wx.CheckBox(panel,-1,'��ס�û�������',(30,120),(100,-1))
        self.button_login = wx.Button(panel, -1, "��½", pos=(30,160))
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
        #wx.StaticText(panel,-1,"TD���߷�����IP��ַ",(30,10))
        #self.ip = wx.TextCtrl(panel, -1, "172.16.121.34", pos=(30,40),size=(120, -1))
        wx.StaticText(panel,-1,"�û���",(30,10))
        self.usrname = wx.TextCtrl(panel, -1, str_name, pos=(30,30),size=(100, -1))
        wx.StaticText(panel,-1,"����",(30,70))
        self.passwd = wx.TextCtrl(panel, -1, str_passwd, pos=(30,90),size=(100, -1),style=wx.TE_PASSWORD)        
        #-------------------------ͼƬ----------------------------------
        bm = wx.Bitmap('image\drag1.png', wx.BITMAP_TYPE_ANY)
        wx.StaticBitmap(panel, -1, bm,pos=(180, 0),size=(200,220))
        #----------------------------------------------------------------
        self.Bind(wx.EVT_BUTTON,  self.login, self.button_login)
    def login(self,event):
        #-----------------------��ȡ����--------------------
        version = '1.2.1'
        self.ips = "172.16.121.34"
        name = self.usrname.GetValue()
        passwd = self.passwd.GetValue()  
        box_value = self.save.GetValue()          #��ȡ��ѡ��״̬
        self.port = 31500        
        #-----------------------------------------------------
        msg = ['login']
        msg.append(name)
        msg.append(passwd)
        msg.append(version)
        strmsg = socket_data.listtostring(msg)
        returnmsg = socket_data.sendmsg(self.ips, self.port, strmsg)        
        if returnmsg == 'fail': #��½ʧ��
            wx.FutureCall(1000,self.showfaillogin)
        elif returnmsg =='version':#�汾����
            wx.FutureCall(1000,self.showfailversion) 
        elif returnmsg =='timeout':#��ʱ
            wx.FutureCall(1000,self.showtimeout)   
        else:
            if box_value == True:
                self.conf.set("Saveinfo", "value","1")
                self.conf.set("Saveinfo", "name",name)
                self.conf.set("Saveinfo", "passwd",passwd)
                self.conf.write(open('conf.ini', "r+"))
            else:
                self.conf.set("Saveinfo", "value","0")
                self.conf.write(open('conf.ini', "r+"))                      
            self.OnExit()
            frame = Frame()
            frame.Center()
            frame.Show()
    def OnExit(self):
        self.Close()        
    def showtimeout(self):  
        wx.MessageBox('���糬ʱ��','Info',wx.OK|wx.ICON_INFORMATION)     
    def showfailversion(self):  
        wx.MessageBox('��ǰ�汾���ɣ�����������°汾��','Info',wx.OK|wx.ICON_INFORMATION)   
    def showfaillogin(self):  
        wx.MessageBox('��½ʧ��! �û����������!','Info',wx.OK|wx.ICON_INFORMATION)          
class logo(wx.Frame):   #logoͼƬ��(δ��ʹ��)
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
        frame = login_frame()
        frame.Center()
        frame.Show()        
    def OnExit(self):
        self.Close()    

class NotebookDemo(wx.Notebook): #�˵�ҳ��
    def __init__(self, parent):
        wx.Notebook.__init__(self, parent, id=wx.ID_ANY, style=
                             wx.BK_DEFAULT
                             #wx.BK_TOP 
                             #wx.BK_BOTTOM
                             #wx.BK_LEFT
                             #wx.BK_RIGHT
                             )
 
        tabOne = function_1(self)
        tabOne.SetBackgroundColour("#ADEAEA")
        self.AddPage(tabOne, "����1")
 
        tabTwo = function_2(self)
        tabTwo.SetBackgroundColour("#3299CC")
        self.AddPage(tabTwo, "����2")
        
        self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.OnPageChanged)
        self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGING, self.OnPageChanging)
 
    def OnPageChanged(self, event):
        pass
    def OnPageChanging(self, event):
        pass
    
class Frame(wx.Frame):#������
    def __init__(self):
        wx.Frame.__init__(self, None, -1, 'TDϵͳ����ͳ�Ʒ�������1.2.1',pos=(-1, -1),size=(1000, 500),style=wx.DEFAULT_FRAME_STYLE ^(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))
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
        frameabout.Center()
        frameabout.Show()      

class aboutUI(wx.Frame):#���ڿ��
    def __init__(self):
        wx.Frame.__init__(self, None, -1, '����',pos=(700, 250),size=(300, 300),style=wx.DEFAULT_FRAME_STYLE ^(wx.RESIZE_BORDER | wx.MINIMIZE_BOX|wx.MAXIMIZE_BOX))
        self.panel = wx.ScrolledWindow(self, -1)
        self.stat7=wx.StaticText(self.panel,-1,"  �汾: 1.0.0.20150629",(80,80))
        self.stat8=wx.StaticText(self.panel,-1,"  ����: ���Բ� ����",(80,110))
        self.stat8=wx.StaticText(self.panel,-1,"  ����: chen_qi@kedacom.com",(80,140))
        self.stat8=wx.StaticText(self.panel,-1,"  �ֻ�: 7776",(80,170))
        
class function_1(wx.Panel): #����1
    def __init__(self,parent):
        wx.Panel.__init__(self, parent)
        #-------------------------------��Ŀlist----------------------------------
        sampleList = []
        self.listBox1 = wx.ListBox(self, -1, (10, -1), (1000, 200), sampleList,wx.LB_SINGLE)        
        #-------------------------------���ִ�list--------------------------------
        sampleList2 = []
        self.listBox2 = wx.ListBox(self, -1, (10, 200), (500, 170), sampleList2,wx.LB_SINGLE)        
        #-------------------------------�¼��ִ�list------------------------------
        self.tree = wx.TreeCtrl(self,pos=(500, 200),size=(500,170))   
        #self.Bind(wx.EVT_TREE_SEL_CHANGED, self.thirdtimeget, self.tree)             
class  function_2(wx.Panel): #����2
    def __init__(self,parent):
        wx.Panel.__init__(self, parent)
if __name__ == "__main__":
    app = wx.App()
    #---------------------------
    frame = login_frame()
    frame.Center()
    frame.Show()          
    #----------------------------
    app.MainLoop()        