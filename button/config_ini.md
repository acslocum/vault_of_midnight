# config.ini
Unless you need to write a new trigger or player class, the **config.ini** file should be the only file you need to edit to get MOFO up and running for a given Fort.

The **config.ini** is parsed by Python's configparser module. It's a standard .ini file structure - sections can be created via placing the section name in square brackets like so:  
```
[general]
```  
and then the parameters are stored as key/value pairs:  
```
debug = True
```
Comments can be added by starting the line with the '#' key:
```
# This is a comment
```

## Example config.ini
Here's an example of the **config.ini** file:

```
[general]
    debug = True
    
    type = video
    
    trigger_type = button

    # random file string
    random = *

    #full or relative path to the media folder
    media_folder = media/video

[audio]
    idle_audio = idle.wav

[video]
    #filename of the idle loop video within the video_folder
    idle_video = idle.mp4

[button_params]
    # raspberry pi GPIO mode (BCM or BOARD)
    gpio_mode = BCM
    pin = 18
    interval = 100
    # debounce time (ms)
    debounce = 300

[url_params]
    #server_url = https://dqzpkqyqqu.us-east-2.awsapprunner.com
    server_url = http://localhost:8080/watch
    # request interval and request timeout in ms
    interval = 5000
    timeout = 2500

[timer_params]
    # timer interval in ms
    interval = 5000

[mqtt_params]
    # hostname, port, topic
    host = 127.0.0.1
    port = 1883
    topic = test
```
## Sections Explained
### General Section
At the top is the **\[general]** section. This controls the core of the application. At the moment it has the following keys and their uses:
1. debug - (True/False) sets/clears a debug flag in the application that can be used to control printing of debug messages
2. type - specifies what type of player (audio, video, etc.) to instantiate and use
3. trigger_type - specifies what type of trigger (button, url, mqtt, etc.) to instantiate and use
4. random - specifies the string sent by the trigger for the player to consider to be a request to randomly select a media file instead of playing a specific one
5. media_folder - the folder path (relative or absolute) in which the media is located

### Player/Trigger Sections
Following the **\[general]** section are sections dedicated for each player/trigger. When developing a new player or trigger class, create a new group section for all of that class' parameters and then ensure your class is looking in that group for its configuration needs. We won't go into all the different sections here, but we'll take a look at one player (video) and one trigger (url) type.
#### Video Player
```
[video]
    idle_video = idle.mp4
```
The video player has one parameter currently, *idle_video*. This is filename within the specified media folder for the video player to consider to be the background video to loop forever until a trigger is received. 
#### URL Trigger
```
[url_params]
    server_url = http://localhost:8080/watch
    # request interval and request timeout in ms
    interval = 5000
    timeout = 2500
```
The URL trigger has three parameters:
1. *server_url* - the URL to make requests from
2. *interval* - the time in milliseconds between request attempts
3. *timeout* - the time in milliseconds between when a request is made and when the response needs to be received before considering that the server is not responding