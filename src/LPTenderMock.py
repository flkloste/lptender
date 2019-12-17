from time import sleep

class LpTenderMock(object):
    def pressPlay(self):
        print '**Play button pressed**'
        self.waitForPlaying()
    def waitForPlaying(self):
        sleep(1)
        print '**Playing Sgt. Pepper**'
    def stop(self):
        print '**the music is stopped!**'
    def waitForStopDone(self):
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
        