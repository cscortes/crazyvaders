from datetime import datetime, timedelta
from lib import invaderutils

#from dataclasses import dataclass
from datetime import datetime

class Transition:
    state : int
    next_state : int
    delay : int
    wave_setup = None
    start_time : datetime

    def __init__(self, state, next_state, delay, wave_setup, start_time):
        self.state = state
        self.next_state = next_state
        self.delay = delay
        self.wave_setup = wave_setup
        self.start_time = start_time


class Transitions(object):
    transitions   : list = []
    current_state : int  = invaderutils.GAME_STARTED_EVENT

    def add( self, state, next_state, delay=0, wave_setup=None):
        item = Transition(state, next_state, delay, wave_setup, None)
        self.transitions.append(item)

    def _check(self, state, next_state, time_tics):

        for t in self.transitions:
            if ( t.state == state ) and ( t.next_state == next_state ):
                if (t.delay == 0):
                    self.current_state = next_state
                    return wave_setup 
                
                elif (t.start_time == None):
                    t.start_time = datetime.now()
                
                elif (t.start_time + timedelta(seconds = t.delay) < datetime.now()):
                    self.current_state = next_state
                    return t.wave_setup
        return None
    
    def get_wave(self, next_state):
        return self._check( self.current_state, next_state, datetime.now())

