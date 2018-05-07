===========
Break Timer
===========

What Is?
========
A simple MacOS application that reminds you to take a break.

Background
==========
This application is built using `rumps <https://github.com/jaredks/rumps>`_ (*Ridiculously Uncomplicated Mac os x Python Statusbar*).

Rumps is a lightweight wrapper around pyobjc, allowing for easy creation of simple MacOS applications that exist in the status bar in python.

The application was developed on MacOS 10.11.6. It should run on other versions of MacOS (OS X) 10.7 and higher. 

The underlying bits and pieces were installed using MacPorts.

Overview
========
When launched, the application shows the "wind" icon in the status bar. 

The work timer starts immeadiately. After 60 minutes, a notification pops up, telling you to take a break. You can click on the notification, or the "Take a Break" menu item to tell the app you are taking its advice.

The application will "nag" you more frequently after the initial 60 minutes - if you do not go on break within 60 seconds, you will be notified again every 60 seconds.

This way, if you are particularly busy, you can ignore the notification, but you won't be able to completely forget.

When you click the menu item or the notification, a modal dialog pops up. Time to get away from your computer. When you return, click "I'm Back" to start the work timer over again.

You can stop the timer at any time, and subsequently retsart it using the menu that comes up when you click on the status bar icon.

The current time remaining is displayed in the menu as well, in case you are curious - but don't peek too often.

Installation
============
Download the latest release from [TODO: link to the release]. Unzip, and copy to your Applications folder.

Changing The Parameters
=======================
This application has support for command-line arguments. You can run the app with arguments from your Applications folder in the terminal like this::
    
    $ /Applications/break-timer.app/Contents/MacOS/break-timer -d -t 120 -n 5
    
This will run the application with a two-hour "work time" and a five minute "nag time". Work time is the time that has to pass before you are prompted to take a break, and nag time is the time between each subsequent notification - so if you ignore the initial notification after two hours, you will be notified again every 5 minutes.  

The currently supported options are (for the most up-to-date information, run break-timer with the -h switch)::
    
    usage: break-timer.py [-h] [-d] [-t WORK_INTERVAL] [-n NAG_INTERVAL]
    
    optional arguments:
      -h, --help            show this help message and exit
      -d, --debug           Set the debug flag. Will turn on detailed logging.
      -t WORK_INTERVAL, --work-interval WORK_INTERVAL
                            Set the number of minutes before getting told it's
                            time to take a break.
      -n NAG_INTERVAL, --nag-interval NAG_INTERVAL
                            Set the number of minutes between re-notifications
                            when you don't take a break.
                            
    


Development
===========
To develop this application, you will first need to install python 3.5 or higher.

Then you will need a few extra packages, installable via pip::
    
    $ pip install rumps py2app
    
Then you can just edit break-timer.py as needed.

To run the app whilst developing, you can simply run::
    
    $ python break-timer.py
    

Building
========
To build the application bundle for basic tests use the following command::
    
    $ python setup.py py2app -A
    
The app bundle will be located in the dist folder. You must run it from this location, however you can edit the files and relaunch the app without having to rebuild it.

For final deployment, use the following commands to clean up any old builds, and build a proper, portable app bundle::
    
    $ rm -rf build dist
    $ python setup.py py2app
    
Then zip up the bundle (you can use the Finder's "compress" command-click menu option as well)::
    
    $ zip -r break-timer.zip break-timer.app
    
Credits
=======
Source code is copyright Josh Johnson, 2018, All Rights Reserved. 

Icons are taken from https://feathericons.com/. Icons were released under an MIT license and reworked for this project.