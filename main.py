import gi
import os
import threading
gi.require_version("Gtk", "3.0")

from gi.repository import Gtk
def testcallback(parent,response):
    parent.devices=response
    print(response)
def runCmd(command,callback,WinObj):
    os.system(command)
    # Capture the output of the command using subprocess

    callback(WinObj,os.popen(command).read())
class ThreadMg:
    def __init__(self,globale):
        self.cmdsList={"list":"xinput list","increase":f"xinput set-prop 11 \"libinput Accel Speed\" {globale}","decrease":f"xinput set-prop 11 \"libinput Accel Speed\" {globale}"}
        self.ThreadPool=[]
    def appendThread(self,thread):
        self.ThreadPool.append(thread)
    def ThreadGen(self,threadCmdKey,callback,manObj):
        if(threadCmdKey in self.cmdsList):
            myth=threading.Thread(target=runCmd, args=(self.cmdsList[threadCmdKey],callback,manObj))
            self.appendThread(myth)
    def ExecThs(self):
        for oneTh in self.ThreadPool :
            oneTh.start()
    
class TouchPadManager:
    def __init__(self):
        self.devices=""
        self.speed=0.6
        ThreadManager = ThreadMg(self.speed)
        ThreadManager.ThreadGen("list",testcallback,self)
        ThreadManager.ExecThs()
    def applyNewVal(self):
        ThreadManager = ThreadMg(self.speed)
        ThreadManager.ThreadGen("increase",testcallback,self)
        ThreadManager.ExecThs()
class MyWindow(Gtk.Window):
    def __init__(self):

        super().__init__(title="Hello World")
        self.Touchpad=TouchPadManager()

        self.buttonMin = Gtk.Button(label="-5%")

        self.buttonMin.connect("clicked",self.on_button_clicked)


        self.buttonAdd = Gtk.Button(label="+5%")

        self.buttonMin.connect("clicked",self.on_button_clicked2)
        self.add(self.buttonMin)
        self.add(self.buttonAdd)

    def on_button_clicked(self, widget):
        if (self.Touchpad.speed==1):
            self.Touchpad.speed=0
            return
        self.Touchpad.speed+=0.05
    def on_button_clicked2(self, widget):
        if (self.Touchpad.speed==0):
            self.Touchpad.speed=1
            return
        self.Touchpad.speed-=0.05




win = MyWindow()

win.connect("destroy", Gtk.main_quit)

win.show_all()
Gtk.main()
