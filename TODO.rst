=====
TODOs
=====

This file contains outstanding rough edges, enhancements, and new features that are planned for future versions of the application.

On-Break Icon
=============
When on break, change the icon to something that indicates you are on break.

.. admonition:: Done
   
   Completed in 0.2.

Logarithmic back-off For Nagging
================================
If the user doesn't respond initially to the notification to take a break,
the app notifies much more frequently. There should be a gradual back-off.

One use case for this is if you step away from the computer without indicating you are taking a break, and don't get back before time is up.

Loss Of Focus
=============
It's possible, especially when using the "Take a break" menu item, for the alert 
popup to end up behind the current window. There has to be an elegant way to
make it come to the very forefront ("always on top") before showing the modal. 

.. admonition:: Initial Research
   
   It appears what I want to do is not possible. This s/o post sums up what I've tried and I think my only recourse is to do as one of answerers did, and make my own fake modal window. There must be something buried in NSAlert that is preventing my code from keeping the window on top.
   
   https://stackoverflow.com/questions/765416/can-nsalert-be-used-to-create-a-floating-window
   
   I believe that if I really want to address this (and `Change Settings`_) in a comprehensive way, It will be easier to just build a native app using Xcode and swift).

Change Settings
===============
There should be a way for users to change the settings without having to rebuild
the application.

.. admonition:: Done (Initial Pass)
   
   Added in first release. Compromise between a proper settings control panel item or window by adding comand-line arguments.
   
   I'm not sure this is worth digging too deeply into beyond this. It's probably best to abandon pyobjc and build a native app using the moden swift-based toolchain, but the CLI option approach works for now.
   


Hide The Dock Icon
==================
It might be a good idea to hide the Dock icon to keep things tidy. This hinges on being able to always keep the "On Break" modal in the foreground.

.. note::
    
    It seems this is possible via a plist option: LSBackgroundOnly
    


Show Time Left
==============
Sometimes I'm curious how much time is left - it would be great to have a disabled menu item or a tool tip that would show that (possibly next to the icon in the menu bar but I don't want to obesess about it)

.. admonition:: Done
   
   Part of the initial release.

Icons Should Be Global Constants
================================
The icon paths are hard-coded all over the place. Better to put them into one place.

.. admonition:: Done
   
   Part of initial release.