


def calcRamp(steps):
    
    frequencyRampUp = [320, 400, 500, 800, 1000, 1600, 2000, 4000, 8000]
    rampLevels = 8
    rampLevelFactor = 1.5
    firstRampLevelSteps = 50
    
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
 
#start
    
    stepsToDistribute = steps/2
    
    for i in range(rampLevels):
        if stepsToDistribute <= 0:
            break        
        stepsInCurrentLevel = rampStepsPerLevel[i]
        if stepsInCurrentLevel <= stepsToDistribute:
            resultRamp[i] = stepsInCurrentLevel
            stepsToDistribute -= stepsInCurrentLevel;
        else:
            diffSteps = stepsInCurrentLevel - stepsToDistribute
            resultRamp[i] = diffSteps
            stepsToDistribute -= diffSteps
    
    # full speed steps
    if stepsToDistribute > 0:
        fullspeedSteps = stepsToDistribute * 2
        if steps % 2 == 1:
            fullspeedSteps += 1
        resultRamp[rampLevels] = fullspeedSteps
    
    result = list()
    for i in range(len(resultRamp)):        
        result.append([frequencyRampUp[i], resultRamp[i]])
    
    for i in range(1, len(resultRamp)):
        reverseIndex = len(resultRamp) - i - 1
        result.append([frequencyRampUp[reverseIndex], resultRamp[reverseIndex]])
    
    
    #verification
    count = 0
    for i in range(len(result)):
        count += result[i][1]
        
    if count == steps:
        print "SUCCESS"
    else:
        print "FAILURE, count==%d" % count
    
    return result




    
        
ramp = calcRamp(30001)


print "=== RESULT ==="
for i in ramp:
    print i