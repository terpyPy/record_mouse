#!/usr/bin/python3
# mouseposi.py - Displays the mouse cursor's current position.
# record and playback mouse movements, and left clicks.
# assign custom hotkeys to play back recordings, save recordings, ect.
import time
from hotkeys import hkManager
from ListenSettings import State_Resource, move_event, draging_event

keybinds = hkManager()
state = State_Resource()
state.run = True
line_pos = state.line_pos


def curserListener():
    print('ctrl+shift+q to quit.')
    while state.run:
        # Get and print the mouse coordinates.
        if not state.playingBack:
            x, y = state.getPos()
            # check is left click is still held down
            if keybinds.is_pressed('left'):
                state.record_list.append((draging_event, (x, y)))
            else:
                state.record_list.append((move_event, (x, y)))

            state.positionStr = f'X: {x} Y: {y}'
            print(state.positionStr)
            time.sleep(0.1)
            print(line_pos('up'), end=line_pos('clear'))

        else:

            print('playing back...')
            time.sleep(0.01)
            print(line_pos('up'), end=line_pos('clear'))
    else:
        print(line_pos('down'), end=line_pos('clear'))
        print(f'\nquitting...\nlast position: {state.positionStr}')
        keybinds.kill_all()
        quit()


def playing():
    """plays back the recording asynchronously"""
    state.playingBack = True
    print('starting playback...')
    # Prevent hook for click from recording itself in playback
    keybinds.remove_hotkeys(['ctrl+shift+p',
                             'ctrl+shift+s',
                             'leftClick'])
    # if a recording json exists, play it
    try:
        record_list = state.loadEvents('recordings.json')
    except FileNotFoundError:
        print('no recording file found')
        record_list = None

    # play the recording
    state.playRecording(record_list)
    state.record_list.clear()

    # restart the hooks for click and playback
    keybinds.add_hotkeys(['ctrl+shift+p',
                          'ctrl+shift+s',
                          'leftClick'])
    state.playingBack = False


def saveRecording():
    """save the recording asynchronously"""
    print('saving recording...')
    state.saveEvents()

if __name__ == '__main__':
    keybinds.init_funcs_to_dict([state.stop,
                                 playing,
                                 saveRecording,
                                 state.onLeftClick])

    keybinds.add_hotkeys(['ctrl+shift+q',
                          'ctrl+shift+p',
                          'ctrl+shift+s',
                          'leftClick'])
    curserListener()
