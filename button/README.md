# MOFO 
This is a Python/Qt based app for playing Fortress Party media (either audio or video) based off some sort of a trigger.

The application pairs a [Trigger](trigger.md) object with a [Player](player.md) object to provide a highly configurable way to play Fortress Party off from some sort of action taken by a guest. The general concept is that a Trigger is watching for something to happen, either a button to be pressed, a web response to change, etc. When it detects the event has happened, it emits a string using a Qt Signal which the application then routes to the Player's *triggered* slot. At this point the Player does whatever it's supposed to do when it gets triggered.  

A collection of Triggers and Players have already been created, but if you don't see the one you need, it's pretty easy to develop a new one. Read either the [Trigger](trigger.md) or [Player](player.md) documentation accordingly.

## **Most years, editing the [config.ini](config_ini.md) file should be all you need to do!**

