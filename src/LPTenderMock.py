from time import sleep

class LpTenderMock(object):
    def __init__(self):
        self.currentSide = 'A'
    def initialize(self):
        print "**Initializing...**"
        sleep(2)
    def pressPlay(self):
        print '**Play button pressed**'
        self.waitForPlaying()
    def waitForPlaying(self):
        sleep(1)
        print '**Playing Sgt. Pepper side %s**' % self.currentSide
    def stop(self):
        print '**Stop pressed!**'
        sleep(2)
        print '**stop done**'        
    def waitForEndOfRecord(self):
        sleep(5)
        print '**the end of the record is reached**'
    def flip(self):
        print '**flipping the lp...**'
        for i in range(10):
            print '.'
            sleep(i*0.1)
        if self.currentSide == 'A':
            self.currentSide = 'B'
        else:
            self.currentSide = 'A'
        