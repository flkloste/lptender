def verifyRamp(func):
    def decorator(steps):
        result = func(steps)
        count = 0
        for i in range(len(result)):
            count += result[i][1]
            
        if count == steps:
            #print "SUCCESS"
            pass
        else:        
            print "FAILURE, count==%d, expected=%d" % (count, steps)
            raise RuntimeError("Failed to calculate ramp!")
        return result
    return decorator
    
@verifyRamp
def calcRamp(steps):

    if steps < 1:
        raise RuntimeError("Number of steps must be greater than 0")

    frequencyRampUp = [320, 400, 500, 800, 1000, 1600, 2000, 4000, 8000]
    rampLevels = 8
    rampLevelFactor = 1.5
    firstRampLevelSteps = 50
    
    if steps <= firstRampLevelSteps:
        return [[frequencyRampUp[0], steps]]

    rampStepsPerLevel = dict()
    
    # do while number of ramp levels is calculated
    while True:
        rampUpSteps = firstRampLevelSteps
        cumulativeRampUpSteps = firstRampLevelSteps
        rampStepsPerLevel[0] = rampUpSteps
        for i in range(1, rampLevels):
            rampUpSteps = int (rampUpSteps * rampLevelFactor)
            cumulativeRampUpSteps += rampUpSteps
            rampStepsPerLevel[i] = rampUpSteps
            
        if cumulativeRampUpSteps < steps/2 or rampLevels == 1:
            break        
        else:
            rampLevels -= 1

    resultRamp = dict()
 
    # distribute steps to first half of ramp (ramp up)    
    stepsToDistribute = steps/2
    
    for i in range(rampLevels):
        if stepsToDistribute <= 0:
            break        
        stepsInCurrentLevel = rampStepsPerLevel[i]
        if stepsInCurrentLevel <= stepsToDistribute:
            resultRamp[i] = stepsInCurrentLevel
            stepsToDistribute -= stepsInCurrentLevel
        else:
            diffSteps = stepsInCurrentLevel - stepsToDistribute
            resultRamp[i] = diffSteps
            stepsToDistribute -= diffSteps
        
    # full speed steps
    fullspeedSteps = 0
    if steps % 2 == 1:
        fullspeedSteps += 1

    if stepsToDistribute > 0:
        fullspeedSteps += stepsToDistribute * 2
        
    resultRamp[rampLevels] = fullspeedSteps
    
    # create result list
    result = list()
    for i in range(len(resultRamp)):        
        result.append([frequencyRampUp[i], resultRamp[i]])
    
    # mirror the first half of the ramp (ramp down)
    for i in range(1, len(resultRamp)):
        reverseIndex = len(resultRamp) - i - 1
        result.append([frequencyRampUp[reverseIndex], resultRamp[reverseIndex]])
    
    return result


for i in range (1, 102000):
    calcRamp(i)
        
#ramp = calcRamp(101)
#print ramp

#print "=== RESULT ==="
#for i in ramp:
#    print i