import pygame
from pyvidplayer2 import Video
import glob
import random
import configparser

kill_process = False
button_pushed = False
idle_is_playing = True
video_queue = []
CONFIG_VIDEO_PATH = "video_folder"
CONFIG_IDLE_VIDEO_NAME = "idle_video"
config = None

def read_configuration():
    config_ini = configparser.ConfigParser(allow_unnamed_section=True)
    config_ini.read("config.ini")
    return config_ini

def debug(value):
    if config[configparser.UNNAMED_SECTION].getboolean("debug"):
        print(value)

def play_video(video):
    global kill_process
    global button_pushed
    global idle_is_playing
    debug(video)
    vid = Video(video)

    win = pygame.display.set_mode(vid.current_size, pygame.FULLSCREEN | pygame.SCALED)
    # pygame.display.set_caption(vid.name)
    while vid.active:
        key = None
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                vid.stop()
                kill_process = True
            elif (event.type == pygame.KEYDOWN) & (idle_is_playing == True):
                vid.stop()
                button_pushed = True
        if vid.draw(win, (0, 0), force_draw=False):
            pygame.display.update()
        pygame.time.wait(16) # around 60 fps
    # close video when done
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

def init_video_queue():
    all_videos = glob.glob(f"{video_directory()}/*.mp4")
    all_videos.remove(f"{idle_video()}")
    random.shuffle(all_videos)
    return all_videos

def choose_video():
    global video_queue
    if len(video_queue) == 0:
        video_queue = init_video_queue()
    debug(video_queue)
    return video_queue.pop(0)

def loop():
    global button_pushed
    global kill_process
    play_idle_video()
    if button_pushed == True:
        play_video(choose_video())
        button_pushed = False
    elif kill_process == True:
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


