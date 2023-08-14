#!/usr/bin/env python
""" pygame.examples.music_drop_fade
Fade in and play music from a list while observing several events

Adds music files to a playlist whenever played by one of the following methods
Music files passed from the commandline are played
Music files and filenames are played when drag and dropped onto the pygame window
Polls the clipboard and plays music files if it finds one there

Keyboard Controls:
* Press space or enter to pause music playback
* Press up or down to change the music volume
* Press left or right to seek 5 seconds into the track
* Press escape to quit
* Press any other button to skip to the next music file in the list
"""

import pygame
import os, sys

VOLUME_CHANGE_AMOUNT = 0.02  # how fast should up and down arrows change the volume?
SCREEN_SIZE = (640, 480)

MUSIC_DONE = pygame.event.custom_type()  # event to be set as mixer.music.set_endevent()
main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, "data")

starting_pos = 0  # needed to fast forward and rewind
volume = 0.75
music_file_list = []
music_file_types = ("mp3", "ogg", "mid", "mod", "it", "xm", "wav")
music_can_seek = ("mp3", "ogg", "mod", "it", "xm")
screen = None


def add_file(filename):
    """
    This function will check if filename exists and is a music file
    If it is the file will be added to a list of music files(even if already there)
    Type checking is by the extension of the file, not by its contents
    We can only discover if the file is valid when we mixer.music.load() it later

    It looks in the file directory and its data subdirectory
    """
    if filename.rpartition(".")[2].lower() not in music_file_types:
        print(f"{filename} not added to file list")
        print("only these files types are allowed: ", music_file_types)
        return False
    elif os.path.exists(filename):
        music_file_list.append(filename)
    elif os.path.exists(os.path.join(main_dir, filename)):
        music_file_list.append(os.path.join(main_dir, filename))
    elif os.path.exists(os.path.join(data_dir, filename)):
        music_file_list.append(os.path.join(data_dir, filename))
    else:
        print("file not found")
        return False
    print(f"{filename} added to file list")
    return True


def play_file(filename):
    """
    This function will call add_file and play it if successful
    The music will fade in during the first 4 seconds
    set_endevent is used to post a MUSIC_DONE event when the song finishes
    The main loop will call play_next() when the MUSIC_DONE event is received
    """
    global starting_pos

    if add_file(filename):
        try:  # we must do this in case the file is not a valid audio file
            pygame.mixer.music.load(music_file_list[-1])
        except pygame.error as e:
            print(e)  # print description such as 'Not an Ogg Vorbis audio stream'
            if filename in music_file_list:
                music_file_list.remove(filename)
                print(f"{filename} removed from file list")
            return
        pygame.mixer.music.play(fade_ms=4000)
        pygame.mixer.music.set_volume(volume)

        if filename.rpartition(".")[2].lower() in music_can_seek:
            print("file supports seeking")
            starting_pos = 0
        else:
            print("file does not support seeking")
            starting_pos = -1
        pygame.mixer.music.set_endevent(MUSIC_DONE)


def play_next():
    """
    This function will play the next song in music_file_list
    It uses pop(0) to get the next song and then appends it to the end of the list
    The song will fade in during the first 4 seconds
    """

    global starting_pos
    if len(music_file_list) > 1:
        nxt = music_file_list.pop(0)

        try:
            pygame.mixer.music.load(nxt)
        except pygame.error as e:
            print(e)
            print(f"{nxt} removed from file list")

        music_file_list.append(nxt)
        print("starting next song: ", nxt)
    else:
        nxt = music_file_list[0]
    pygame.mixer.music.play(fade_ms=4000)
    pygame.mixer.music.set_volume(volume)
    pygame.mixer.music.set_endevent(MUSIC_DONE)

    if nxt.rpartition(".")[2].lower() in music_can_seek:
        starting_pos = 0
    else:
        starting_pos = -1


def change_music_position(amount):
    """
    Changes current playback position by amount seconds.
    This only works with OGG and MP3 files.
    music.get_pos() returns how many milliseconds the song has played, not
    the current position in the file. We must track the starting position
    ourselves. music.set_pos() will set the position in seconds.
    """
    global starting_pos

    if starting_pos >= 0:  # will be -1 unless play_file() was OGG or MP3
        played_for = pygame.mixer.music.get_pos() / 1000.0
        old_pos = starting_pos + played_for
        starting_pos = old_pos + amount
        pygame.mixer.music.play(start=starting_pos)
        print(f"jumped from {old_pos} to {starting_pos}")


def main():
    global font  # this will be used by the draw_text_line function
    global volume, starting_pos
    global screen
    running = True
    paused = False

    # we will be polling for key up and key down events
    # users should be able to change the volume by holding the up and down arrows
    # the change_volume variable will be set by key down events and cleared by key up events
    change_volume = 0

    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE)
    font = pygame.font.SysFont("Arial", 24)
    font.align = pygame.FONT_CENTER
    clock = pygame.Clock()

    clipped = ""
    if pygame.scrap.has_text():
        clipped = pygame.scrap.get_text()

    # add the command line arguments to the  music_file_list
    for arg in sys.argv[1:]:
        add_file(arg)
    play_file("house_lo.ogg")  # play default music included with pygame

    # draw instructions on screen
    text = """
Drop music files or path names onto this window
Copy file names into the clipboard
Or feed them from the command line
If it's music it will play!

LEFT and RIGHT will skip around the track
UP and DOWN will change volume
ENTER or SPACE will pause/unpause the track
Other keys will start the next track"""
    screen.blit(font.render(text, True, "white", "black", SCREEN_SIZE[0] - 20), (10, 5))
    """
    This is the main loop
    It will respond to drag and drop, clipboard changes, and key presses
    """
    while running:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                running = False
            elif ev.type == pygame.DROPTEXT:
                play_file(ev.text)
            elif ev.type == pygame.DROPFILE:
                play_file(ev.file)
            elif ev.type == MUSIC_DONE:
                play_next()
            elif ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_ESCAPE:
                    running = False  # exit loop
                elif ev.key in (pygame.K_SPACE, pygame.K_RETURN):
                    if paused:
                        pygame.mixer.music.unpause()
                        paused = False
                    else:
                        pygame.mixer.music.pause()
                        paused = True
                elif ev.key == pygame.K_UP:
                    change_volume = VOLUME_CHANGE_AMOUNT
                elif ev.key == pygame.K_DOWN:
                    change_volume = -VOLUME_CHANGE_AMOUNT
                elif ev.key == pygame.K_RIGHT:
                    change_music_position(+5)
                elif ev.key == pygame.K_LEFT:
                    change_music_position(-5)

                else:
                    play_next()

            elif ev.type == pygame.KEYUP:
                if ev.key in (pygame.K_UP, pygame.K_DOWN):
                    change_volume = 0

        # is the user holding up or down?
        if change_volume:
            volume += change_volume
            volume = min(max(0, volume), 1)  # volume should be between 0 and 1
            pygame.mixer.music.set_volume(volume)
            print("volume:", volume)

        if pygame.scrap.has_text():
            new_text = pygame.scrap.get_text()
            if new_text != clipped:
                clipped = new_text
                play_file(clipped)

        pygame.display.flip()
        clock.tick(9)  # keep CPU use down by updating screen less often

    pygame.quit()


if __name__ == "__main__":
    main()
