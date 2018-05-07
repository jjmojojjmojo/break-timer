import rumps
import os
import datetime
from AppKit import NSApplication
import argparse

ICON_DIR = "icons"
NORMAL_ICON = os.path.join(ICON_DIR, "wind.png")
ALERT_ICON = os.path.join(ICON_DIR, "alert-circle.png")
DISABLED_ICON = os.path.join(ICON_DIR, "wind-off.png")

class BreakTimer:
    """
    Class that wraps some interaction around a usual rumps App
    """
    def __init__(self, work_interval=3600, nag_interval=60, debug=False):
        """
        Constructor.
        
        work_interval - integer, seconds. Time that will elapse before telling 
                        the user to take a break.
                        
        nag_interval - integer, seconds. After an initial notification, notifications
                       will increase in frequency - this setting controls how long
                       to wait between each subsequent notice.
        
        debug - boolean. Proxy for the rumps.debug function, turns on detailed 
                logging within rumps (log entries end up in the MacOS Console)
        """
        
        self.work_interval = work_interval
        self.nag_interval = nag_interval
        
        self.work_delta = datetime.timedelta(seconds=work_interval)
        self.nag_delta = datetime.timedelta(seconds=nag_interval)
        self.delta = self.work_delta
        
        self.checkin = datetime.datetime.now()
        
        self.app = rumps.App(
            "Break Timer", 
            icon=NORMAL_ICON)
        
        self.app.menu = [
            rumps.MenuItem('Stop', self.stop),
            rumps.MenuItem('Take Break', self.break_popup),
            rumps.MenuItem("Time Left", None)
        ]
        
        self.work_timer = rumps.Timer(self.take_break, 10)
        self.front_timer = rumps.Timer(self.bring_to_front, 10)
        self.time_left_timer = rumps.Timer(self.update_time_left, 45)
        
        self.nag = False
        self.paused = False       
        
        rumps.debug_mode(debug)
        
    def update_time_left(self, timer):
        end_date = self.checkin + self.work_delta
        time_left = end_date - datetime.datetime.now()
        
        self.app.menu['Time Left'].title = "Left: {}".format(":".join(str(time_left).split(":")[0:2])) 
        
    def __call__(self):
        self.work_timer.start()
        self.time_left_timer.start()
        self.app.run()
        
    def stop(self, _):
        """
        Stop the timers
        """
        self.paused = True
        self.app.icon = DISABLED_ICON
        self.work_timer.stop()
        self.time_left_timer.stop()
        self.app.menu['Stop'].title = "Restart"
        self.app.menu['Stop'].set_callback(self.restart)
        
    def restart(self, _):
        """
        Start the timers after a call to stop()
        """
        self.paused = False
        self.app.icon = NORMAL_ICON
        self.work_timer.start()
        self.time_left_timer.start()
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
        self.app.icon = NORMAL_ICON
        self.checkin = datetime.datetime.now()
        self.delta = self.work_delta

    def take_break(self, timer):
        """
        Notify the user that it's time to take a break.
        
        Only executes the notification if enough time has elapsed.
        
        If the user doesn't click on the notification, or click the "Take a Break"
        menu item, a new notification is resent every self.nag_interval seconds.
        """
        now = datetime.datetime.now()
        if now - self.checkin >= self.delta:
            self.checkin = now
            
            rumps.notification("Break Timer", "Time for a break!", "Click to take your break.")
            self.app.icon = ALERT_ICON
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

def factory(work_interval=3600, nag_interval=60, debug=False):
    """
    Simple factory function to create a BreakTimer and wire up a 
    NotificationCenter object
    """
    bt = BreakTimer(work_interval=work_interval, nag_interval=nag_interval, debug=debug)
    nc = rumps.notifications(NotificationCenter(bt))
    
    return bt

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-d", "--debug", 
        action="store_true",
        default=False, 
        help="Set the debug flag. Will turn on detailed logging.")
    parser.add_argument(
        "-t", "--work-interval", 
        type=lambda x: int(x)*60, 
        default="60", 
        help="Set the number of minutes before getting told it's time to take a break.")
    parser.add_argument(
        "-n", "--nag-interval", 
        type=lambda x: int(x)*60, 
        default="1", 
        help="Set the number of minutes between re-notifications when you don't take a break.")
    
    options = parser.parse_args()
    
    bt = factory(debug=options.debug, work_interval=options.work_interval, nag_interval=options.nag_interval)
    bt()
