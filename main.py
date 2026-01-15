import gi
import os
import threading
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib
def testcallback(parent,response):
    parent.devices=response
    print(response)
def runCmd(command,callback,WinObj):
    os.system(command)
    callback(WinObj,os.popen(command).read())
class ThreadMg:
    def __init__(self,manager):
        self.manager=manager
        self.cmdsList={
            "list":"xinput list",
            "props":lambda dev: f"xinput list-props {dev}",
            "set-prop":lambda dev,prop,val: f"xinput set-prop {dev} \"{prop}\" {val}",
            "enable":lambda dev,val: f"xinput set-prop {dev} \"Device Enabled\" {val}",
        }
        self.ThreadPool=[]
    def appendThread(self,thread):
        self.ThreadPool.append(thread)
    def ThreadGen(self,threadCmdKey,callback,manObj,*args):
        if threadCmdKey in self.cmdsList:
            cmd=self.cmdsList[threadCmdKey]
            if callable(cmd):
                command=cmd(*args)
            else:
                command=cmd
            myth=threading.Thread(target=runCmd, args=(command,callback,manObj))
            self.appendThread(myth)
    def ExecThs(self):
        for oneTh in self.ThreadPool :
            oneTh.start()
class TouchPadManager:
    def __init__(self,owner=None):
        self.devices=""
        self.speed=0.6
        self.device_id=self.find_device_id()
        self.owner=owner
        ThreadManager = ThreadMg(self)
        ThreadManager.ThreadGen("list",testcallback,self)
        ThreadManager.ExecThs()
    def find_device_id(self):
        out=os.popen("xinput list").read()
        for line in out.splitlines():
            if "touchpad" in line.lower():
                parts=line.split()
                for p in parts:
                    if p.startswith("id="):
                        try:
                            return int(p.split("=")[1])
                        except:
                            pass
        return None
    def refresh(self):
        if self.device_id is None:
            self.device_id=self.find_device_id()
        if self.device_id:
            ThreadManager = ThreadMg(self)
            ThreadManager.ThreadGen("props",testcallback,self,self.device_id)
            ThreadManager.ExecThs()
    def set_property(self,prop,value):
        if self.device_id is None:
            self.device_id=self.find_device_id()
        if self.device_id is None:
            return
        ThreadManager = ThreadMg(self)
        ThreadManager.ThreadGen("set-prop",testcallback,self,self.device_id,prop,value)
        ThreadManager.ExecThs()
    def enable_device(self,enable=True):
        if self.device_id is None:
            self.device_id=self.find_device_id()
        if self.device_id is None:
            return
        val=1 if enable else 0
        ThreadManager = ThreadMg(self)
        ThreadManager.ThreadGen("enable",testcallback,self,self.device_id,val)
        ThreadManager.ExecThs()
    def increase_speed(self):
        if self.speed >= 1.0:
            self.speed=1.0
        else:
            self.speed=round(min(1.0,self.speed+0.05),2)
        self.apply_speed()
    def decrease_speed(self):
        if self.speed <= -1.0:
            self.speed=-1.0
        else:
            self.speed=round(max(-1.0,self.speed-0.05),2)
        self.apply_speed()
    def apply_speed(self):
        self.set_property("libinput Accel Speed", self.speed)
    def toggle_tapping(self):
        if self.device_id is None:
            self.device_id=self.find_device_id()
        if self.device_id is None:
            return
        out=os.popen(f"xinput list-props {self.device_id}").read()
        cur=0
        for line in out.splitlines():
            if "libinput Tapping Enabled" in line:
                parts=line.split()
                for p in parts[::-1]:
                    if p.isdigit():
                        cur=int(p)
                        break
                break
        new=0 if cur==1 else 1
        self.set_property("libinput Tapping Enabled", new)
    def toggle_natural_scroll(self):
        if self.device_id is None:
            self.device_id=self.find_device_id()
        if self.device_id is None:
            return
        out=os.popen(f"xinput list-props {self.device_id}").read()
        cur=0
        for line in out.splitlines():
            if "libinput Natural Scrolling Enabled" in line:
                parts=line.split()
                for p in parts[::-1]:
                    if p.isdigit():
                        cur=int(p)
                        break
                break
        new=0 if cur==1 else 1
        self.set_property("libinput Natural Scrolling Enabled", new)
class MyWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="Touchpad Settings")
        self.Touchpad=TouchPadManager(owner=self)
        vbox=Gtk.Box(orientation=Gtk.Orientation.VERTICAL,spacing=6)
        self.add(vbox)
        self.status_label=Gtk.Label(label="Status:")
        vbox.pack_start(self.status_label,False,False,0)
        hbox=Gtk.Box(spacing=6)
        vbox.pack_start(hbox,False,False,0)
        self.button_increase = Gtk.Button(label="+5%")
        self.button_increase.connect("clicked", self.on_increase)
        hbox.pack_start(self.button_increase,True,True,0)
        self.button_decrease = Gtk.Button(label="-5%")
        self.button_decrease.connect("clicked", self.on_decrease)
        hbox.pack_start(self.button_decrease,True,True,0)
        self.button_toggle_enable = Gtk.Button(label="Enable/Disable")
        self.button_toggle_enable.connect("clicked", self.on_toggle_enable)
        vbox.pack_start(self.button_toggle_enable,False,False,0)
        self.button_tapping = Gtk.Button(label="Toggle Tapping")
        self.button_tapping.connect("clicked", self.on_toggle_tapping)
        vbox.pack_start(self.button_tapping,False,False,0)
        self.button_natural = Gtk.Button(label="Toggle Natural Scroll")
        self.button_natural.connect("clicked", self.on_toggle_natural)
        vbox.pack_start(self.button_natural,False,False,0)
        self.button_refresh = Gtk.Button(label="Refresh")
        self.button_refresh.connect("clicked", self.on_refresh)
        vbox.pack_start(self.button_refresh,False,False,0)
        self.show_all()
    def on_increase(self, widget):
        self.Touchpad.increase_speed()
        GLib.timeout_add(200,self.update_status_once)
    def on_decrease(self, widget):
        self.Touchpad.decrease_speed()
        GLib.timeout_add(200,self.update_status_once)
    def on_toggle_enable(self, widget):
        out=os.popen(f"xinput list-props {self.Touchpad.device_id}").read() if self.Touchpad.device_id else ""
        cur=1
        for line in out.splitlines():
            if "Device Enabled" in line:
                parts=line.split()
                for p in parts[::-1]:
                    if p.isdigit():
                        cur=int(p)
                        break
                break
        self.Touchpad.enable_device(enable=(cur==0))
        GLib.timeout_add(200,self.update_status_once)
    def on_toggle_tapping(self, widget):
        self.Touchpad.toggle_tapping()
        GLib.timeout_add(200,self.update_status_once)
    def on_toggle_natural(self, widget):
        self.Touchpad.toggle_natural_scroll()
        GLib.timeout_add(200,self.update_status_once)
    def on_refresh(self, widget):
        self.Touchpad.refresh()
        GLib.timeout_add(200,self.update_status_once)
    def update_status_once(self):
        text=self.Touchpad.devices if self.Touchpad.devices else "No data"
        self.status_label.set_text(text)
        return False
win = MyWindow()
win.connect("destroy", Gtk.main_quit)
Gtk.main()
