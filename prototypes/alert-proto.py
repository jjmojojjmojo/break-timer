"""
Attempts at creating a modal that will always stay in the foreground.
"""

import AppKit
from AppKit import NSApplication, NSBundle, NSAlert, NSRunningApplication
from AppKit import NSStatusWindowLevel, NSScreenSaverWindowLevel, NSWindowCollectionBehaviorCanJoinAllSpaces, NSWindowCollectionBehaviorFullScreenAuxiliary, NSFloatingWindowLevel

from Cocoa import NSApplicationActivateIgnoringOtherApps

import rumps
from rumps.compat import text_type, string_types, iteritems

def handler(info):
    print(info)

def alert(title=None, message='', ok=None, cancel=None):
    """
    Repackaged from rumps, so we can try to make the window float above 
    the others.
    
    Generate a simple alert window.
    .. versionchanged:: 0.2.0
        Providing a `cancel` string will set the button text rather than only using text "Cancel". `title` is no longer
        a required parameter.
    :param title: the text positioned at the top of the window in larger font. If ``None``, a default localized title
                  is used. If not ``None`` or a string, will use the string representation of the object.
    :param message: the text positioned below the `title` in smaller font. If not a string, will use the string
                    representation of the object.
    :param ok: the text for the "ok" button. Must be either a string or ``None``. If ``None``, a default
               localized button title will be used.
    :param cancel: the text for the "cancel" button. If a string, the button will have that text. If `cancel`
                   evaluates to ``True``, will create a button with text "Cancel". Otherwise, this button will not be
                   created.
    :return: a number representing the button pressed. The "ok" button is ``1`` and "cancel" is ``0``.
    """
    message = text_type(message)
    if title is not None:
        title = text_type(title)
    rumps.rumps._require_string_or_none(ok)
    if not isinstance(cancel, string_types):
        cancel = 'Cancel' if cancel else None
    alert = NSAlert.alertWithMessageText_defaultButton_alternateButton_otherButton_informativeTextWithFormat_(
        title, ok, cancel, None, message)
    alert.setAlertStyle_(0)  # informational style
    
    #panel = alert.window()
    #panel.setLevel_(NSStatusWindowLevel)
    # alert.window().setFloatingPanel_(True)
    # import ipdb; ipdb.set_trace();
    rumps.rumps._log('alert opened with message: {0}, title: {1}'.format(repr(message), repr(title)))
    
    #app = NSRunningApplication.currentApplication()
    #app.activateWithOptions_(NSApplicationActivateIgnoringOtherApps)
    nsapplication = NSApplication.sharedApplication()
    nsapplication.activateIgnoringOtherApps_(True)
    
    result = alert.runModal()
    return result

def alert2(message, title="Test", ok="OK", cancel="Cancel"):
    """
    Use the native pyobjc NSAlert
    """
    title = "Test"
    ok = "OK"
    cancel = "Cancel"
    message = "Hello"
    nsapplication = AppKit.NSApplication.sharedApplication()
    alert = AppKit.NSAlert.alertWithMessageText_defaultButton_alternateButton_otherButton_informativeTextWithFormat_(title, ok, None, None, message)
    alert.beginSheetModalForWindow_completionHandler_(nsapplication.mainWindow, handler)


alert("Test", "This is only a test")
alert2("This is only a test")