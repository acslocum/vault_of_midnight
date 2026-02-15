# The Trigger Class
In general, a Trigger object is the class that watches for a guest to do "something" (pressing a button, scanning a QR code, etc.) and then emits a signal notifying the paired Player object to do its thing and play whatever is requested. 

## Trigger Code Structure
Writing a new Trigger class is pretty straightforward! Start by making a copy of the *template_trigger.py* file, implement whatever code is necessary for the class to watch for the desired user event, and then make sure when it detects that event, that it emits the **triggered(str)** signal to notify the MOFO application that it needs to play some media. We'll go through the template code:

### Python Imports
```
import configparser
from PyQt6.QtCore import (
    QObject,
    pyqtSignal,
    pyqtSlot
)
```
At minimum, you'll need to import these. *configparser* is neeeded for parsing the **config.ini** file. Two Qt classes are also needed:  
 - QObject - your Trigger class **MUST** inherit from QObject
 - pyqtSignal - your class needs to emit a signal with a string parameter to let the application notify the paired Player

The third import, *pyqtSlot*, isn't required but is stronly encouraged. You need to have some sort of function that is called periodically that checks to see if whatever your trigger is looking for has occurred, at which point you emit the *triggered* signal.

### Class Definition and \_\_init__()
```
class template_trigger(QObject):
    triggered = pyqtSignal(str)
    
    def __init__(self, config : configparser.ConfigParser, parent : QObject = None):
        super().__init__(parent)
        self.config = config
        self.config_section = 'section' # change to whatever section you want to use for this trigger

        # repeat a modified version of this call to pull out whatever parameters you need
        self.value = int(self.config.get(self.config_section, 'key'))
```
The first line defines the Trigger class name, and has it inherit from *QObject*. Right below that, the *triggered* signal is defined as a Qt signal that will contain a string parameter. Next, we define the *\_\_init__()* function that takes in a *configparser* object, and an optional QObject *parent*. We then call QObject's \_\_init__() function to ensure all the Qt QObject stuff is initialized correct. After that, we just parse whatever information we'll need to get out of the *config.ini* file to finish configuring this Trigger.

### Doing the work
```
@pyqtSlot()
    def checkForAction(self):
        actionOccurred = False

        # do whatever is needed to check if the action occurred

        # emit the signal if so
        if actionOccurred == True:
            self.triggered.emit('')
```
Finally we have the Trigger's function that checks to see if the user has initiated whatever action we're looking for to trigger the main application to play some media. This function should be called periodically to check, and it's important this is **NOT** called from within a blocking loop - Qt's event loop needs to spin to allow signals and slots to work properly. It is recommend that you set up a QTimer to periodically call this function only when the timer goes off.  

Once you've determined that a party guest did the thing that is supposed to trigger media play, you emit the *triggered* signal via:
```self.triggered.emit('')```. Note that emitting an empty string is shorthand to tell the player to randomly select a media file, while emitting a non-empty string would tell the player to play a specific file. For example, ```self.triggered.emit('hello.mp4')``` would tell the player to play a file called 'hello.mp4'

### Integrating into MOFO
The last step is to let the main application know that it needs to instantiate an instance of this new Trigger class whenever the *config.ini* parameter 'general/trigger_type' is set to request this class. Let's assume we just created a Trigger class named 'Foo'. Integrating 'Foo' requires three simple steps:
1. Import your new class via ```import Foo``` near the top of the main application file
2. In the main application, you'll see a section of code that looks like the following:
```
        trigger_type = config.get('general', 'trigger_type')
        if trigger_type == 'timer':
            trigger = TimerTrigger.TimerTrigger(config)
        elif trigger_type == 'url':
            trigger = URLTrigger.URLTrigger(config)
        ...
```
Add an ```elif``` block to instatiate an instance of your 'Foo' class, and assign it to the 'trigger' variable
```
        elif trigger_type == 'foo':
            print('Creating Foo trigger')            
            trigger = Foo.Foo(config)
```
3. Assign the type in the *config.ini* to be your Foo type. Under the \[general] section, set the *trigger_type* variable to the same string you used in the ```elif```
   ```
   trigger_type = foo
   ```

That's it! Launch the main application and you should be able to use your newly created Trigger