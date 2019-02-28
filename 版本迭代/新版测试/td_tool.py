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
class  login_frame(wx.Frame):#登陆界面类
    def __init__(self):
        wx.Frame.__init__(self, None, -1, '登陆界面',pos=(500, 100),size=(400, 280)) 
        panel = wx.Panel(self)
        #==============记住用户名===============
        self.save = wx.CheckBox(panel,-1,'记住用户名密码',(30,120),(100,-1))
        self.button_login = wx.Button(panel, -1, "登陆", pos=(30,160))
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
        #wx.StaticText(panel,-1,"TD工具服务器IP地址",(30,10))
        #self.ip = wx.TextCtrl(panel, -1, "172.16.121.34", pos=(30,40),size=(120, -1))
        wx.StaticText(panel,-1,"用户名",(30,10))
        self.usrname = wx.TextCtrl(panel, -1, str_name, pos=(30,30),size=(100, -1))
        wx.StaticText(panel,-1,"密码",(30,70))
        self.passwd = wx.TextCtrl(panel, -1, str_passwd, pos=(30,90),size=(100, -1),style=wx.TE_PASSWORD)        
        #-------------------------图片----------------------------------
        bm = wx.Bitmap('image\drag1.png', wx.BITMAP_TYPE_ANY)
        wx.StaticBitmap(panel, -1, bm,pos=(180, 0),size=(200,220))
        #----------------------------------------------------------------
        self.Bind(wx.EVT_BUTTON,  self.login, self.button_login)
    def login(self,event):
        #-----------------------获取变量--------------------
        version = '1.2.1'
        self.ips = "172.16.121.34"
        name = self.usrname.GetValue()
        passwd = self.passwd.GetValue()  
        box_value = self.save.GetValue()          #获取复选框状态
        self.port = 31500        
        #-----------------------------------------------------
        msg = ['login']
        msg.append(name)
        msg.append(passwd)
        msg.append(version)
        strmsg = socket_data.listtostring(msg)
        returnmsg = socket_data.sendmsg(self.ips, self.port, strmsg)        
        if returnmsg == 'fail': #登陆失败
            wx.FutureCall(1000,self.showfaillogin)
        elif returnmsg =='version':#版本过低
            wx.FutureCall(1000,self.showfailversion) 
        elif returnmsg =='timeout':#超时
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
        wx.MessageBox('网络超时！','Info',wx.OK|wx.ICON_INFORMATION)     
    def showfailversion(self):  
        wx.MessageBox('当前版本过旧，请更新至最新版本！','Info',wx.OK|wx.ICON_INFORMATION)   
    def showfaillogin(self):  
        wx.MessageBox('登陆失败! 用户名密码错误!','Info',wx.OK|wx.ICON_INFORMATION)          
class logo(wx.Frame):   #logo图片类(未被使用)
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
        frame = login_frame()
        frame.Center()
        frame.Show()        
    def OnExit(self):
        self.Close()    

class NotebookDemo(wx.Notebook): #菜单页面
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
        self.AddPage(tabOne, "功能1")
 
        tabTwo = function_2(self)
        tabTwo.SetBackgroundColour("#3299CC")
        self.AddPage(tabTwo, "功能2")
        
        self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.OnPageChanged)
        self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGING, self.OnPageChanging)
 
    def OnPageChanged(self, event):
        pass
    def OnPageChanging(self, event):
        pass
    
class Frame(wx.Frame):#总体框架
    def __init__(self):
        wx.Frame.__init__(self, None, -1, 'TD系统数据统计分析工具1.2.1',pos=(-1, -1),size=(1000, 500),style=wx.DEFAULT_FRAME_STYLE ^(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))
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
        frameabout.Center()
        frameabout.Show()      

class aboutUI(wx.Frame):#关于框架
    def __init__(self):
        wx.Frame.__init__(self, None, -1, '关于',pos=(700, 250),size=(300, 300),style=wx.DEFAULT_FRAME_STYLE ^(wx.RESIZE_BORDER | wx.MINIMIZE_BOX|wx.MAXIMIZE_BOX))
        self.panel = wx.ScrolledWindow(self, -1)
        self.stat7=wx.StaticText(self.panel,-1,"  版本: 1.0.0.20150629",(80,80))
        self.stat8=wx.StaticText(self.panel,-1,"  作者: 中试部 陈琪",(80,110))
        self.stat8=wx.StaticText(self.panel,-1,"  邮箱: chen_qi@kedacom.com",(80,140))
        self.stat8=wx.StaticText(self.panel,-1,"  分机: 7776",(80,170))
        
class function_1(wx.Panel): #功能1
    def __init__(self,parent):
        wx.Panel.__init__(self, parent)
        #-------------------------------项目list----------------------------------
        sampleList = []
        self.listBox1 = wx.ListBox(self, -1, (10, -1), (1000, 200), sampleList,wx.LB_SINGLE)        
        #-------------------------------主轮次list--------------------------------
        sampleList2 = []
        self.listBox2 = wx.ListBox(self, -1, (10, 200), (500, 170), sampleList2,wx.LB_SINGLE)        
        #-------------------------------下级轮次list------------------------------
        self.tree = wx.TreeCtrl(self,pos=(500, 200),size=(500,170))   
        #self.Bind(wx.EVT_TREE_SEL_CHANGED, self.thirdtimeget, self.tree)             
class  function_2(wx.Panel): #功能2
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