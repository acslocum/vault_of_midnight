import pygame
from pyvidplayer2 import Video
import glob
import random
import configparser
import urllib.request

kill_process = False
requested_video_name = None
idle_is_playing = True
CONFIG_VIDEO_PATH = "video_folder"
CONFIG_IDLE_VIDEO_NAME = "idle_video"
CONFIG_SERVER_URL = "server_url"
FPS_MAX = "fps_max"
config = None

def read_configuration():
    config_ini = configparser.ConfigParser(allow_unnamed_section=True)
    config_ini.read("config.ini")
    return config_ini

def debug(value):
    if config[configparser.UNNAMED_SECTION].getboolean("debug"):
        print(value)

def check_video_request():
    global requested_video_name
    global CONFIG_SERVER_URL
    url = f"{config[configparser.UNNAMED_SECTION][CONFIG_SERVER_URL]}/watch"
    contents = urllib.request.urlopen(url).read()
    if contents:
        debug(f"scanned <{contents.decode('utf-8')}>")
        return contents.decode('utf-8')
    return None

def fps_sleep():
    global FPS_MAX
    fps = config[configparser.UNNAMED_SECTION].getint(FPS_MAX)
    if fps:
        return int(1000//fps)
    return 16

def play_video(video):
    global kill_process
    global requested_video_name
    global idle_is_playing
    debug(f"playing: <{video}>")
    vid = Video(video)

    win = pygame.display.set_mode(vid.current_size, pygame.FULLSCREEN | pygame.SCALED)
    while vid.active:
        key = None
        requested_video_name = check_video_request()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                vid.stop()
                kill_process = True
        if (requested_video_name is not None) & (idle_is_playing == True):
            vid.stop()
        if vid.draw(win, (0, 0), force_draw=False):
            pygame.display.update()
        pygame.time.wait(fps_sleep()) # around 60 fps
    vid.close()

def video_directory():
    global config
    global CONFIG_VIDEO_PATH
    return f"{config[configparser.UNNAMED_SECTION][CONFIG_VIDEO_PATH]}"

def idle_video():
    global config
    global CONFIG_IDLE_VIDEO_NAME
    return f"{video_directory()}/{config[configparser.UNNAMED_SECTION][CONFIG_IDLE_VIDEO_NAME]}"

def play_idle_video():
    global idle_is_playing
    idle_is_playing = True
    play_video(idle_video())
    idle_is_playing = False
    return

def loop():
    global requested_video_name
    global kill_process
    play_idle_video()
    if requested_video_name:
        play_video(f"{video_directory()}/{requested_video_name}")
        requested_video_name = None
        return

def run():
    global kill_process
    global idle_is_playing
    global config
    config = read_configuration()
    pygame.init()
    idle_is_playing = True
    while kill_process == False:
        loop()
    pygame.quit()

random.seed()
run()


