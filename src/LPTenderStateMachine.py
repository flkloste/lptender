import threading
from time import sleep

class Transitions(object):
    PressPlay = 'PressPlay'
    PlayingReady = 'PlayingReady'
    EndOfRecord = 'EndOfRecord'
    Stop = 'Stop'
    StopDone = 'StopDone'
    FlipOnly = 'FlipOnly'
    FlipDone = 'FlipDone'
    FlipWithAutoplay = 'FlipWithAutoplay'
    PlayAfterFlip = 'PlayAfterFlip'

class State(object):
    
    numberOfTransitionsDone = 0
    
    def __init__(self, stateMachine):
        self._stateMachine = stateMachine
        print 'Processing current state:', str(self)
        State.numberOfTransitionsDone += 1
        
    def doTransition(self, transition):
        raise NotImplementedError()
    
    def ignoreTransition(self, transition):
        print 'Ignoring transition "%s" (state=%s)' % (transition, self)
        return self
    
    def execFctAndDoTransitionAfterwards(self, fct, args=None, transition=None):
        # store number of transitions so that passed transition will be ignored if another transition was invoked before
        currentNumberOfTransitions = State.numberOfTransitionsDone
        
        if args == None:
            fct()
        else:
            fct(args)
        if transition != None and currentNumberOfTransitions == State.numberOfTransitionsDone:
            self._stateMachine.doTransition(transition)
    
    def __repr__(self):
        return self.__str__()
    
    def __str__(self):
        return self.__class__.__name__

class Playing(State):
    
    def __init__(self, stateMachine):
        super(Playing, self).__init__(stateMachine)
        threading.Thread(target=self.execFctAndDoTransitionAfterwards, args=(self._stateMachine._lptender.waitForEndOfRecord, None, Transitions.EndOfRecord)).start()
        
    def doTransition(self, transition):
        if transition == Transitions.Stop:
            return Stopping(self._stateMachine)
        elif transition == Transitions.EndOfRecord:
            return Stopped(self._stateMachine)
        else:
            return self.ignoreTransition(transition)
    
class Stopping(State):
    
    def __init__(self, stateMachine):
        super(Stopping, self).__init__(stateMachine)
        threading.Thread(target=self.execFctAndDoTransitionAfterwards, args=(self._stateMachine._lptender.waitForStopDone, None, Transitions.StopDone)).start()
        
    def doTransition(self, transition):
        if transition == Transitions.StopDone:
            return Stopped(self._stateMachine)
        else:
            return self.ignoreTransition(transition)
    
class Stopped(State):
    
    def __init__(self, stateMachine):
        super(Stopped, self).__init__(stateMachine)
        
    def doTransition(self, transition):
        if transition == Transitions.PressPlay:
            return PlayPressed(self._stateMachine)
        elif transition == Transitions.FlipOnly:
            return FlippingOnly(self._stateMachine)
        elif transition == Transitions.FlipWithAutoplay:
            return FlippingWithAutoplay(self._stateMachine)
        else:
            return self.ignoreTransition(transition)
        
class PlayPressed(State):
    
    def __init__(self, stateMachine):
        super(PlayPressed, self).__init__(stateMachine)
        threading.Thread(target=self.execFctAndDoTransitionAfterwards, args=(self._stateMachine._lptender.pressPlay, None, Transitions.PlayingReady)).start()
        
    def doTransition(self, transition):
        if transition == Transitions.PlayingReady:
            return Playing(self._stateMachine)
        else:
            return self.ignoreTransition(transition)
        
class FlippingWithAutoplay(State):
    
    def __init__(self, stateMachine):
        super(FlippingWithAutoplay, self).__init__(stateMachine)
        threading.Thread(target=self.execFctAndDoTransitionAfterwards, args=(self._stateMachine._lptender.flip, None, Transitions.PlayAfterFlip)).start()
        
    def doTransition(self, transition):
        if transition == Transitions.PlayAfterFlip:
            return PlayPressed(self._stateMachine)
        else:
            return self.ignoreTransition(transition)
    
class FlippingOnly(State):
    
    def __init__(self, stateMachine):
        super(FlippingOnly, self).__init__(stateMachine)
        threading.Thread(target=self.execFctAndDoTransitionAfterwards, args=(self._stateMachine._lptender.flip, None, Transitions.FlipDone)).start()
        
    def doTransition(self, transition):
        if transition == Transitions.FlipDone:
            return Stopped(self._stateMachine)
        else:
            return self.ignoreTransition(transition)
        
class LpTenderStateMachine(object):
    
    def __init__(self):
        self._lock = threading.Lock()
        self._lptender = LpTenderDummy.LpTenderDummy()
        # set start state
        self._state = Stopped(self)
        
    def doTransition(self, transition):
        with self._lock:
            self._state = self._state.doTransition(transition)
            
    def getCurrentState(self):
        with self._lock:
            return self._state

