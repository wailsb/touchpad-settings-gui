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
    def __init__(self):
        self.cmdsList={"list":"xinput list"}
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
        ThreadManager = ThreadMg()
        ThreadManager.ThreadGen("list",testcallback,self)
        ThreadManager.ExecThs()
        print("init done")
        print(self.devices)
class MyWindow(Gtk.Window):
    def __init__(self):

        super().__init__(title="Hello World")
        Touchpad=TouchPadManager()

        self.button = Gtk.Button(label="Click Here")

        self.button.connect("clicked", self.on_button_clicked)

        self.add(self.button)


    def on_button_clicked(self, widget):

        print("Hello World")



win = MyWindow()

win.connect("destroy", Gtk.main_quit)

win.show_all()
Gtk.main()
