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

class _StateBase(object):
    
    def __init__(self, stateMachine):
        self._stateMachine = stateMachine
        self._stateMachine._transitionCount += 1
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

class _StatePlaying(_StateBase):
    
    def __init__(self, stateMachine):
        super(_StatePlaying, self).__init__(stateMachine)
        threading.Thread(target=self._stateMachine._execFctAndDoTransitionAfterwards, args=(self._stateMachine._lptender.waitForEndOfRecord, None, Transitions.EndOfRecord, self._stateMachine._transitionCount)).start()
        
    def doTransition(self, transition):
        if transition == Transitions.Stop:
            return _StateStopping(self._stateMachine)
        elif transition == Transitions.EndOfRecord:
            return _StateStopped(self._stateMachine)
        else:
            return self.ignoreTransition(transition)
    
class _StateStopping(_StateBase):
    
    def __init__(self, stateMachine):
        super(_StateStopping, self).__init__(stateMachine)
        threading.Thread(target=self._stateMachine._execFctAndDoTransitionAfterwards, args=(self._stateMachine._lptender.waitForStopDone, None, Transitions.StopDone, self._stateMachine._transitionCount)).start()
        
    def doTransition(self, transition):
        if transition == Transitions.StopDone:
            return _StateStopped(self._stateMachine)
        else:
            return self.ignoreTransition(transition)
    
class _StateStopped(_StateBase):
    
    def __init__(self, stateMachine):
        super(_StateStopped, self).__init__(stateMachine)
        
    def doTransition(self, transition):
        if transition == Transitions.PressPlay:
            return _StatePlayPressed(self._stateMachine)
        elif transition == Transitions.FlipOnly:
            return _StateFlippingOnly(self._stateMachine)
        elif transition == Transitions.FlipWithAutoplay:
            return _StateFlippingWithAutoplay(self._stateMachine)
        else:
            return self.ignoreTransition(transition)
        
class _StatePlayPressed(_StateBase):
    
    def __init__(self, stateMachine):
        super(_StatePlayPressed, self).__init__(stateMachine)
        threading.Thread(target=self._stateMachine._execFctAndDoTransitionAfterwards, args=(self._stateMachine._lptender.pressPlay, None, Transitions.PlayingReady, self._stateMachine._transitionCount)).start()
        
    def doTransition(self, transition):
        if transition == Transitions.PlayingReady:
            return _StatePlaying(self._stateMachine)
        else:
            return self.ignoreTransition(transition)
        
class _StateFlippingWithAutoplay(_StateBase):
    
    def __init__(self, stateMachine):
        super(_StateFlippingWithAutoplay, self).__init__(stateMachine)
        threading.Thread(target=self._stateMachine._execFctAndDoTransitionAfterwards, args=(self._stateMachine._lptender.flip, None, Transitions.PlayAfterFlip, self._stateMachine._transitionCount)).start()
        
    def doTransition(self, transition):
        if transition == Transitions.PlayAfterFlip:
            return _StatePlayPressed(self._stateMachine)
        else:
            return self.ignoreTransition(transition)
    
class _StateFlippingOnly(_StateBase):
    
    def __init__(self, stateMachine):
        super(_StateFlippingOnly, self).__init__(stateMachine)
        threading.Thread(target=self._stateMachine._execFctAndDoTransitionAfterwards, args=(self._stateMachine._lptender.flip, None, Transitions.FlipDone, self._stateMachine._transitionCount)).start()
        
    def doTransition(self, transition):
        if transition == Transitions.FlipDone:
            return _StateStopped(self._stateMachine)
        else:
            return self.ignoreTransition(transition)
        
class LpTenderStateMachine(object):
    
    def __init__(self, lpTender):
        self._lock = threading.Lock()
        self._lptender = lpTender
        self._transitionCount = 0
        self._state = _StateStopped(self)
        self._autoFlip = False
        
    def doTransition(self, transition, numberOfTransititionsForCompare=None):
        with self._lock:
            if numberOfTransititionsForCompare == None or numberOfTransititionsForCompare == self._transitionCount:
                self._state = self._state.doTransition(transition)
            else:
                print "Transition outdated: " + transition
            
    def getCurrentState(self):
        with self._lock:
            return self._state

    @property
    def autoFlip(self):
        with self._lock:
            return self._autoFlip

    @autoFlip.setter
    def autoFlip(self, value):
        with self._lock:
            self._autoFlip = bool(value)

    def _execFctAndDoTransitionAfterwards(self, fct, args=None, transition=None, transitionCountBeforeFunc=0):        
        if args == None:
            fct()
        else:
            fct(args)

        if transition != None:
            self.doTransition(transition, transitionCountBeforeFunc)

