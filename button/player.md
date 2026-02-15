# The Player Class
In general, a Player object is the class that receives a signal from a Trigger class and then plays whatever is requested.  Typically it also plays a background media file in between requested media

## Player Code Structure
Writing a new Player class is pretty straightforward! Start by making a copy of the *template_player.py* file, implement whatever code is necessary for the class to react to the received *triggered* signal. We'll go through the template code:

### Python Imports
```
import configparser
from PyQt6.QtCore import (
    QObject, pyqtSlot
)
```
At minimum, you'll need to import these. *configparser* is neeeded for parsing the **config.ini** file. Two Qt classes are also needed:  
 - QObject - your Player class **MUST** inherit from QObject
 - pyqtSlot - your class needs to define a Qt slot that takes a string parameter to execute whatever is supposed to happen when it is triggered by the paired Trigger


### Class Definition and \_\_init__()
```
class template_player(QObject):
    def __init__(self, config : configparser.ConfigParser, parent : QObject = None):
        super().__init__(parent)
        self.config = config
        self.config_section = 'section' # change to whatever section you want to use for this trigger

        # repeat a modified version of this call to pull out whatever parameters you need
        self.value = int(self.config.get(self.config_section, 'key'))

```
The first line defines the Player class name, and has it inherit from *QObject*. Next, we define the *\_\_init__()* function that takes in a *configparser* object, and an optional QObject *parent*. We then call QObject's \_\_init__() function to ensure all the Qt QObject stuff is initialized correct. After that, we just parse whatever information we'll need to get out of the *config.ini* file to finish configuring this Player.

### Doing the work
```
@pyqtSlot(str)
    def triggered(self, filename : str):
        # do whatever you're supposed to do with 'filename'
```
Finally we have the Player's function that plays the requested media.  

 **NOTE: you need to properly handle an empty string ```(filename == '')```, as that is commonly used to indicate that the player should randomly select a media file from the media directory.**

### Integrating into MOFO
The last step is to let the main application know that it needs to instantiate an instance of this new Player class whenever the *config.ini* parameter 'general/type' is set to request this class. Let's assume we just created a class named 'Foo'. Integrating 'Foo' requires three simple steps:
1. Import your new class via ```import Foo``` near the top of the main application file
2. In the main application, you'll see a section of code that looks like the following:
```
        media_type = config.get('general', 'type')
        if media_type == 'audio':
            print('Creating audio player')
            player = AudioPlayer.AudioPlayer(config)
        elif media_type == 'console':
            print('Creating console player')            
            player = ConsolePlayer.ConsolePlayer(config)
```
Add an ```elif``` block to instatiate an instance of your 'Foo' class, and assign it to the 'player' variable
```
        elif media_type == 'foo':
            print('Creating Foo player')            
            player = Foo.Foo(config)
```
3. Assign the type in the *config.ini* to be your Foo type. Under the \[general] section, set the *type* variable to the same string you used in the ```elif```
   ```
   type = foo
   ```

That's it! Launch the main application and you should be able to use your newly created Player