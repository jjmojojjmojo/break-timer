import rumps
import datetime
from AppKit import NSApplication, NSBundle

# TODO: do this in the plist file in the App bundle
#       This is also probably a bad idea if I can't get
#       the app to stay in the foreground all the time, since it makes
#       it hard to find the popup, and close the app if you can't
# info = NSBundle.mainBundle().infoDictionary()
# info["LSBackgroundOnly"] = "1"

rumps.debug_mode(True)

class BreakTimer:
    def __init__(self, work_interval=3600, nag_interval=60):
        self.work_interval = work_interval
        self.nag_interval = nag_interval
        
        self.work_delta = datetime.timedelta(seconds=work_interval)
        self.nag_delta = datetime.timedelta(seconds=nag_interval)
        self.delta = self.work_delta
        
        self.checkin = datetime.datetime.now()
        
        self.app = rumps.App(
            "Break Timer", 
            icon="wind.png")
        
        self.app.menu = [
            rumps.MenuItem('Stop', self.stop),
            rumps.MenuItem('Take Break', self.break_popup)
        ]
        
        self.work_timer = rumps.Timer(self.take_break, 10)
        self.front_timer = rumps.Timer(self.bring_to_front, 10)
        
        self.nag = False
        self.paused = False
        
    def __call__(self):
        self.work_timer.start()
        # self.front_timer.start()
        self.app.run()
        
    def stop(self, _):
        """
        Stop the timers
        """
        self.paused = True
        self.app.icon = "test.png"
        self.work_timer.stop()
        self.app.menu['Stop'].title = "Restart"
        self.app.menu['Stop'].set_callback(self.restart)
        
    def restart(self, _):
        self.paused = False
        self.app.icon = "wind.png"
        self.work_timer.start()
        self.app.menu['Stop'].title = "Stop"
        self.app.menu['Stop'].set_callback(self.stop)
        
    def bring_to_front(self, timer=None):
        """
        Bring the application to the front.
        """
        nsapplication = NSApplication.sharedApplication()
        nsapplication.activateIgnoringOtherApps_(True)
        
    def break_popup(self, _=None):
        """
        Popup prompting the user to let the app know when they have returned.
        """
        self.bring_to_front()
        rumps.alert(title="Go On Break", message="Get away from the computer!", ok="Back!")
        self.app.icon = "wind.png"
        self.checkin = datetime.datetime.now()
        self.delta = self.work_delta

    def take_break(self, timer):
        now = datetime.datetime.now()
        if now - self.checkin >= self.delta:
            self.checkin = now
            
            rumps.notification("Break Timer", "Time for a break!", "Click to take your break.")
            self.app.icon = "alert-circle.png"
            self.delta = self.nag_delta
            

class NotificationCenter:
    """
    Wrapper for a BreakTimer object that will handle user
    interaction - when the user clicks a notification, it will
    trigger the "click when you get back" alert
    
    This was necessary because rumps.notifications decorator doesn't support
    instance methods.
    """
    def __init__(self, breaktimer):
        self.bt = breaktimer
        
    def __call__(self, info):
        self.bt.break_popup()

if __name__ == "__main__":
    bt = BreakTimer()
    nc = rumps.notifications(NotificationCenter(bt))
    
    bt()
