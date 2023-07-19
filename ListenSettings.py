#!/usr/bin/python3
import numpy as np
import json
import time
import pyautogui
import PySimpleGUI as sg

# global variables, not in class to be used in other modules as needed
LINE_UP = '\033[1A'
LINE_DOWN = '\033[1B'
LINE_CLEAR = '\x1b[2K'
HOME_CURSOR = '\033[0;0H'

move_event = 0
left_click_event = 1
draging_event = 2

class State_Resource:
    def __init__(self):
        self.run = False
        self.positionStr = 'default'
        self.line_dict = {'up': LINE_UP,
                          'down': LINE_DOWN,
                          'clear': LINE_CLEAR,
                          'home': HOME_CURSOR}
        self.playingBack = False
        self.record_list = []
        

    def __repr__(self):
        return f'State_Resource(run={self.run}, positionStr={self.positionStr})'

    def __str__(self):
        return f'record_list: {self.record_list}'

    def line_pos(self, line):
        return self.line_dict.get(line, 'home')

    @property
    def line_dict(self):
        return self._line_dict

    @line_dict.setter
    def line_dict(self, value:dict):
        self._line_dict = value

    @property
    def run(self):
        return self._run

    @run.setter
    def run(self, value:bool):
        self._run = value

    @property
    def positionStr(self):
        return self._positionStr

    @positionStr.setter
    def positionStr(self, value):
        # set if the value is a string
        if isinstance(value, str):
            self._positionStr = value
        else:
            raise TypeError('value must be a string')

    def stop(self):
        self.run = False
        
    def onLeftClick(self):
        x, y = pyautogui.position()
        print(self.line_pos('down'), end=self.line_pos('clear'))
        print(f'left click at: {x}, {y}', end=self.line_pos('down'))
        self.record_list.append((left_click_event, (x, y)))
        time.sleep(0.1)

    def playRecording(self, recording=None):
        if recording is None:
            recording = self.record_list.copy()
        # clear the recording list
        for event in recording:
            eventType, eventPos = event
            
            if eventType == move_event:
                pyautogui.moveTo(eventPos)
                
            elif eventType == left_click_event:
                pyautogui.click(eventPos)
                
            elif eventType == draging_event:
                pyautogui.dragTo(eventPos)

    def getPos(self):
        return pyautogui.position()
    
    def saveEvents(self, toSave=None):
        if toSave is None:
            toSave = self.record_list.copy()
        else:
            toSave = toSave.copy()
            
        name = sg.popup_get_text('enter a name for the recording: ')
        with open(f'{name}.json', 'w') as f:
            json.dump(toSave, f)
        f.close()
        
    def loadEvents(self):
        fileName = sg.popup_get_file('enter the name of the recording: ')
        record_list = json.load(open(fileName, 'r'))
        return record_list
    
    def modify_recording(self, newOrigin=None):
        """modify the recording by setting start x,y coords to (0,0),
        and translating the rest of the coords accordingly"""
        # load the recording, shows popup to browse for file
        record_list = self.loadEvents()
        result = []
        startPos = record_list[0][1]
        # separate events and coords into separate lists
        events = [event[0] for event in record_list]
        coords = np.array([event[1] for event in record_list]) 
        modified_coords = coords - startPos
        newOrigin = sg.popup_get_text('enter a new origin for the recording: (x,y)')
        if newOrigin is None:
            # find min x and y values if negative
            min_x = min(modified_coords[:,0])
            min_y = min(modified_coords[:,1])
            # translate the coords to be positive
            modified_coords += abs(min_x), abs(min_y)
        else:
            newOrigin = tuple(map(int, newOrigin.split(',')))
            modified_coords += newOrigin
        # combine the modified coords and events into a list of tuples
        result = list(zip(events, modified_coords.tolist()))
        # save the modified recording
        self.saveEvents(toSave=result)
        time.sleep(0.1)
        
if __name__ == "__main__":
    t = State_Resource()
    t.modify_recording((60, 60))
    