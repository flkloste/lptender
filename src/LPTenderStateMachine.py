import threading

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
    
    def __init__(self, lptender):
        self._lptender = lptender
        print 'Processing current state:', str(self)
        
    def doTransition(self, transition):
        raise NotImplementedError()
    
    def ignoreTransition(self, transition):
        print 'Ignoring transition "%s" (state=%s)' % (transition, self)
        return self
    
    def __repr__(self):
        return self.__str__()
    
    def __str__(self):
        return self.__class__.__name__

class Playing(State):
    
    def __init__(self, lptender):
        super(Playing, self).__init__(lptender)
        threading.Thread(target=self._lptender.waitForEndOfRecord).start()
        
    def doTransition(self, transition):
        if transition == Transitions.Stop:
            return Stopping(self._lptender)
        elif transition == Transitions.EndOfRecord:
            return Stopped(self._lptender)
        else:
            return self.ignoreTransition(transition)
    
class Stopping(State):
    
    def __init__(self, lptender):
        super(Stopping, self).__init__(lptender)
        threading.Thread(target=self._lptender.waitForStopDone).start()
        
    def doTransition(self, transition):
        if transition == Transitions.StopDone:
            return Stopped(self._lptender)
        else:
            return self.ignoreTransition(transition)
    
class Stopped(State):
    
    def __init__(self, lptender):
        super(Stopped, self).__init__(lptender)
        
    def doTransition(self, transition):
        if transition == Transitions.PressPlay:
            return PlayPressed(self._lptender)
        elif transition == Transitions.FlipOnly:
            return FlippingOnly(self._lptender)
        elif transition == Transitions.FlipWithAutoplay:
            return FlippingWithAutoplay(self._lptender)
        else:
            return self.ignoreTransition(transition)
        
class PlayPressed(State):
    
    def __init__(self, lptender):
        super(PlayPressed, self).__init__(lptender)
        threading.Thread(target=self._lptender.pressPlay).start()
        
    def doTransition(self, transition):
        if transition == Transitions.PlayingReady:
            return Playing(self._lptender)
        else:
            return self.ignoreTransition(transition)
        
class FlippingWithAutoplay(State):
    
    def __init__(self, lptender):
        super(FlippingWithAutoplay, self).__init__(lptender)
        threading.Thread(target=self._lptender.flip, args = ([True])).start()
        
    def doTransition(self, transition):
        if transition == Transitions.PlayAfterFlip:
            return PlayPressed(self._lptender)
        else:
            return self.ignoreTransition(transition)
    
class FlippingOnly(State):
    
    def __init__(self, lptender):
        super(FlippingOnly, self).__init__(lptender)
        threading.Thread(target=self._lptender.flip, args = ([False])).start()
        
    def doTransition(self, transition):
        if transition == Transitions.FlippingDone:
            return Stopped(self._lptender)
        else:
            return self
        
class LpTenderStateMachine(object):
    
    def __init__(self):
        self._lock = threading.Lock()
        self._lptender = LpTenderDummy.LpTenderDummy(self)
        # set start state
        self._state = Stopped(self._lptender)
        
    def doTransition(self, transition):
        with self._lock:
            self._state = self._state.doTransition(transition)
            
    def getCurrentState(self):
        with self._lock:
            return self._state
