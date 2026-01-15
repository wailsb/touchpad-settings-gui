import gi
import os
import threading
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib
def testcallback(parent,response):
    parent.devices=response
    print(response)
def runCmd(command,callback,WinObj):
    try:
        os.system(command)
        out=os.popen(command).read()
    except Exception as e:
        out=str(e)
    try:
        callback(WinObj,out)
    except Exception:
        pass
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
        self.available_devices=[]
        ThreadManager = ThreadMg(self)
        ThreadManager.ThreadGen("list",testcallback,self)
        ThreadManager.ExecThs()
        try:
            self.update_device_list()
        except Exception:
            pass
    def find_device_id(self):
        try:
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
        except Exception:
            pass
        return None
    def update_device_list(self):
        self.available_devices=[]
        try:
            out=os.popen("xinput list").read()
            for line in out.splitlines():
                if "id=" in line:
                    try:
                        left=line.split("id=")[0].strip()
                        name=left.replace('\ufffd','').replace('\u2192','').replace('\xe2\x86\xb3','')
                        name=name.replace('\u251c','').replace('\u2502','').replace('\u2514','').strip()
                        name=name.replace('\u25b8','').replace('↳','').strip()
                        id_part=line.split("id=")[1].split()[0]
                        did=int(id_part)
                        self.available_devices.append((name,did))
                    except Exception:
                        pass
        except Exception:
            pass
        return self.available_devices
    def refresh(self):
        if self.device_id is None:
            self.device_id=self.find_device_id()
        if self.device_id:
            ThreadManager = ThreadMg(self)
            ThreadManager.ThreadGen("props",testcallback,self,self.device_id)
            ThreadManager.ExecThs()
        try:
            self.update_device_list()
        except Exception:
            pass
    def set_property(self,prop,value):
        try:
            if self.device_id is None:
                self.device_id=self.find_device_id()
            if self.device_id is None:
                return
            ThreadManager = ThreadMg(self)
            ThreadManager.ThreadGen("set-prop",testcallback,self,self.device_id,prop,value)
            ThreadManager.ExecThs()
        except Exception:
            pass
    def enable_device(self,enable=True):
        try:
            if self.device_id is None:
                self.device_id=self.find_device_id()
            if self.device_id is None:
                return
            val=1 if enable else 0
            ThreadManager = ThreadMg(self)
            ThreadManager.ThreadGen("enable",testcallback,self,self.device_id,val)
            ThreadManager.ExecThs()
        except Exception:
            pass
    def increase_speed(self):
        try:
            if self.speed >= 1.0:
                self.speed=1.0
            else:
                self.speed=round(min(1.0,self.speed+0.05),2)
            self.apply_speed()
        except Exception:
            pass
    def decrease_speed(self):
        try:
            if self.speed <= -1.0:
                self.speed=-1.0
            else:
                self.speed=round(max(-1.0,self.speed-0.05),2)
            self.apply_speed()
        except Exception:
            pass
    def apply_speed(self):
        try:
            self.set_property("libinput Accel Speed", self.speed)
        except Exception:
            pass
    def toggle_tapping(self):
        try:
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
        except Exception:
            pass
    def toggle_natural_scroll(self):
        try:
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
        except Exception:
            pass
    def toggle_palm_detection(self):
        try:
            if self.device_id is None:
                self.device_id=self.find_device_id()
            if self.device_id is None:
                return
            out=os.popen(f"xinput list-props {self.device_id}").read()
            cur=0
            for line in out.splitlines():
                if "libinput Palm Detection Enabled" in line:
                    parts=line.split()
                    for p in parts[::-1]:
                        if p.isdigit():
                            cur=int(p)
                            break
                    break
            new=0 if cur==1 else 1
            self.set_property("libinput Palm Detection Enabled", new)
        except Exception:
            pass
    def toggle_middle_emulation(self):
        try:
            if self.device_id is None:
                self.device_id=self.find_device_id()
            if self.device_id is None:
                return
            out=os.popen(f"xinput list-props {self.device_id}").read()
            cur=0
            for line in out.splitlines():
                if "libinput Middle Emulation Enabled" in line:
                    parts=line.split()
                    for p in parts[::-1]:
                        if p.isdigit():
                            cur=int(p)
                            break
                    break
            new=0 if cur==1 else 1
            self.set_property("libinput Middle Emulation Enabled", new)
        except Exception:
            pass
    def toggle_disable_while_typing(self):
        try:
            if self.device_id is None:
                self.device_id=self.find_device_id()
            if self.device_id is None:
                return
            out=os.popen(f"xinput list-props {self.device_id}").read()
            cur=0
            for line in out.splitlines():
                if "libinput Disable While Typing Enabled" in line:
                    parts=line.split()
                    for p in parts[::-1]:
                        if p.isdigit():
                            cur=int(p)
                            break
                    break
            new=0 if cur==1 else 1
            self.set_property("libinput Disable While Typing Enabled", new)
        except Exception:
            pass
class MyWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="Touchpad Settings")
        self.Touchpad=TouchPadManager(owner=self)
        vbox=Gtk.Box(orientation=Gtk.Orientation.VERTICAL,spacing=6)
        self.add(vbox)
        self.device_combo=Gtk.ComboBoxText()
        self.device_combo.connect("changed", self.on_device_changed)
        vbox.pack_start(self.device_combo,False,False,0)
        self.scrolled=Gtk.ScrolledWindow()
        self.scrolled.set_min_content_height(120)
        vbox.pack_start(self.scrolled,True,True,0)
        self.status_view=Gtk.TextView()
        self.status_view.set_editable(False)
        self.status_view.set_cursor_visible(False)
        self.scrolled.add(self.status_view)
        self.status_label=Gtk.Label(label="Status:")
        vbox.pack_start(self.status_label,False,False,0)
        self.populate_devices()
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
        self.button_palm = Gtk.Button(label="Toggle Palm Detection")
        self.button_palm.connect("clicked", self.on_toggle_palm)
        vbox.pack_start(self.button_palm,False,False,0)
        self.button_middle = Gtk.Button(label="Toggle Middle Emulation")
        self.button_middle.connect("clicked", self.on_toggle_middle)
        vbox.pack_start(self.button_middle,False,False,0)
        self.button_disable_typing = Gtk.Button(label="Toggle Disable While Typing")
        self.button_disable_typing.connect("clicked", self.on_toggle_disable_typing)
        vbox.pack_start(self.button_disable_typing,False,False,0)
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
    def on_toggle_palm(self, widget):
        self.Touchpad.toggle_palm_detection()
        GLib.timeout_add(200,self.update_status_once)
    def on_toggle_middle(self, widget):
        self.Touchpad.toggle_middle_emulation()
        GLib.timeout_add(200,self.update_status_once)
    def on_toggle_disable_typing(self, widget):
        self.Touchpad.toggle_disable_while_typing()
        GLib.timeout_add(200,self.update_status_once)
    def on_refresh(self, widget):
        self.Touchpad.refresh()
        GLib.timeout_add(200,self.update_status_once)
    def populate_devices(self):
        try:
            self.device_combo.remove_all()
            devices=self.Touchpad.update_device_list()
            for name,did in devices:
                self.device_combo.append_text(f"{did}: {name}")
            if devices:
                self.device_combo.set_active(0)
        except Exception:
            pass
    def on_device_changed(self, combo):
        try:
            text=combo.get_active_text()
            if not text:
                return
            did=int(text.split(':')[0])
            self.Touchpad.device_id=did
            self.Touchpad.refresh()
            GLib.timeout_add(200,self.update_status_once)
        except Exception:
            pass
    def update_status_once(self):
        try:
            text=self.Touchpad.devices if self.Touchpad.devices else "No data"
            buf=self.status_view.get_buffer()
            buf.set_text(text)
            self.status_label.set_text(text.splitlines()[0] if text else "Status:")
        except Exception:
            pass
        return False
win = MyWindow()
win.connect("destroy", Gtk.main_quit)
Gtk.main()
