import threading

class Transitions(object):
    PressPlay = 'PressPlay'
    PlayingReady = 'PlayingReady'
    EndOfRecordTransition = 'EndOfRecordTransition'
    EndOfRecordToStop = 'EndOfRecordToStop'
    PressStop = 'PressStop'
    StopDone = 'StopDone'
    Flip = 'Flip'
    FlipDone = 'FlipDone'
    Ready = 'Ready'    
    AutoFlip = 'AutoFlip'
    PressPlayAfterAutoFlip = 'PressPlayAfterAutoFlip'

class States(object):
    Initializing = 'Initializing'
    Playing = 'Playing'
    Stopping = 'Stopping'
    Stopped = 'Stopped'
    PlayPressed = 'PlayPressed'
    Flipping = 'Flipping'
    EndOfRecord = 'EndOfRecord'

class _StateBase(object):
    
    def __init__(self, name, stateMachine):
        self._name = name
        self._stateMachine = stateMachine
        self._stateMachine._transitionCount += 1
        print 'Processing current state:', str(self)
        
    def doTransition(self, transition):
        raise NotImplementedError()
    
    def ignoreTransition(self, transition):
        print 'Ignoring transition "%s" (state=%s)' % (transition, self)
        return self
    
    def __str__(self):
        return self._name

class _StateInitializing(_StateBase):
    
    def __init__(self, stateMachine):
        super(_StateInitializing, self).__init__(States.Initializing, stateMachine)
        threading.Thread(target=self._stateMachine._execFctAndDoTransitionAfterwards, args=(self._stateMachine._lptender.initialize, None, Transitions.Ready, self._stateMachine._transitionCount)).start()
        
    def doTransition(self, transition):
        if transition == Transitions.Ready:
            return _StateStopped(self._stateMachine)
        else:
            return self.ignoreTransition(transition)

class _StatePlaying(_StateBase):
    
    def __init__(self, stateMachine):
        super(_StatePlaying, self).__init__(States.Playing, stateMachine)
        threading.Thread(target=self._stateMachine._execFctAndDoTransitionAfterwards, args=(self._stateMachine._lptender.waitForEndOfRecord, None, Transitions.EndOfRecordTransition, self._stateMachine._transitionCount)).start()
        
    def doTransition(self, transition):
        if transition == Transitions.PressStop:
            return _StateStopping(self._stateMachine)
        elif transition == Transitions.EndOfRecordTransition:
            return _StateEndOfRecord(self._stateMachine)
        else:
            return self.ignoreTransition(transition)
    
class _StateStopping(_StateBase):
    
    def __init__(self, stateMachine):
        super(_StateStopping, self).__init__(States.Stopping, stateMachine)
        threading.Thread(target=self._stateMachine._execFctAndDoTransitionAfterwards, args=(self._stateMachine._lptender.stop, None, Transitions.StopDone, self._stateMachine._transitionCount)).start()
        
    def doTransition(self, transition):
        if transition == Transitions.StopDone:
            return _StateStopped(self._stateMachine)
        else:
            return self.ignoreTransition(transition)

class _StateEndOfRecord(_StateBase):
    
    def __init__(self, stateMachine):
        super(_StateEndOfRecord, self).__init__(States.EndOfRecord, stateMachine)
        if self._stateMachine.autoFlip == True:
            nextTransition = Transitions.AutoFlip
        else:
            nextTransition = Transitions.EndOfRecordToStop

        threading.Thread(target=self._stateMachine._execFctAndDoTransitionAfterwards, args=(None, None, nextTransition, self._stateMachine._transitionCount)).start()
        
    def doTransition(self, transition):
        if transition == Transitions.AutoFlip:
            return _StateFlipping(self._stateMachine, True)
        elif transition == Transitions.EndOfRecordToStop:
            return _StateStopped(self._stateMachine)
        else:
            return self.ignoreTransition(transition)        

class _StateStopped(_StateBase):
    
    def __init__(self, stateMachine):
        super(_StateStopped, self).__init__(States.Stopped, stateMachine)
        
    def doTransition(self, transition):
        if transition == Transitions.PressPlay:
            return _StatePlayPressed(self._stateMachine)
        elif transition == Transitions.Flip:
            return _StateFlipping(self._stateMachine)
        else:
            return self.ignoreTransition(transition)
        
class _StatePlayPressed(_StateBase):
    
    def __init__(self, stateMachine):
        super(_StatePlayPressed, self).__init__(States.PlayPressed, stateMachine)
        threading.Thread(target=self._stateMachine._execFctAndDoTransitionAfterwards, args=(self._stateMachine._lptender.pressPlay, None, Transitions.PlayingReady, self._stateMachine._transitionCount)).start()
        
    def doTransition(self, transition):
        if transition == Transitions.PlayingReady:
            return _StatePlaying(self._stateMachine)
        else:
            return self.ignoreTransition(transition)
    
class _StateFlipping(_StateBase):
    
    def __init__(self, stateMachine, autoflip=False):
        super(_StateFlipping, self).__init__(States.Flipping, stateMachine)
        
        if autoflip:
            nextTransition = Transitions.PressPlayAfterAutoFlip
        else:
            nextTransition = Transitions.FlipDone

        def FlipAndResetAutoFlip():
            self._stateMachine._lptender.flip()
            if autoflip:
                self._stateMachine.autoFlip = False
        
        threading.Thread(target=self._stateMachine._execFctAndDoTransitionAfterwards, args=(FlipAndResetAutoFlip, None, nextTransition, self._stateMachine._transitionCount)).start()
        
    def doTransition(self, transition):
        if transition == Transitions.FlipDone:
            return _StateStopped(self._stateMachine)
        elif transition == Transitions.PressPlayAfterAutoFlip:
            return _StatePlayPressed(self._stateMachine)
        else:
            return self.ignoreTransition(transition)

class LpTenderStateMachine(object):
    
    def __init__(self, lpTender):
        self._lock = threading.Lock()
        self._lptender = lpTender
        self._transitionCount = 0
        self._state = _StateInitializing(self)
        self._autoFlip = False
        
    def _doTransition(self, transition, numberOfTransititionsForCompare=None):
        with self._lock:
            if numberOfTransititionsForCompare == None or numberOfTransititionsForCompare == self._transitionCount:
                self._state = self._state.doTransition(transition)
            else:
                print "Transition outdated: " + transition
            
    def getCurrentState(self):
        with self._lock:
            return str(self._state)

    @property
    def autoFlip(self):
        return self._autoFlip

    @autoFlip.setter
    def autoFlip(self, value):
        with self._lock:
            self._autoFlip = bool(value)

    def _execFctAndDoTransitionAfterwards(self, fct=None, args=None, transition=None, transitionCountBeforeFunc=None):    
        if fct != None:
            if args == None:
                fct()
            else:
                fct(args)

        if transition != None:
            self._doTransition(transition, transitionCountBeforeFunc)

    def play(self):
        self._doTransition(Transitions.PressPlay)

    def stop(self):
        self._doTransition(Transitions.PressStop)

    def flip(self):
        self._doTransition(Transitions.Flip)

