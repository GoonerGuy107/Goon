#Kyle Peppe
#CIS 655 Final OnlinePortion
#Due Date: 12/11/19

def pipelineHazardDectector():
    #Get the instructions from the user
    instructionCount = int(input('How many instructions? '))
    instructionList = []
    #For loop where you pull in all the MIPs style instructions
    for i in range(instructionCount):
        instructionList.append(list(map(str, input('Enter Instructions ' + str(i+1) +': ').split())))
    print('\n')

    #Data Hazard Section
    Baseline_DataHazardArray = ['ADD','SUB','ADDI','ADDU','SUBU','AND','OR','SLT','LW']   
    print("DATA HAZARDS\n")
    #Clearing Variables
    DataHazardArray = []
    DataHazardArrayCounter = 0
    spaces = -1
    stallArray = [[]] * instructionCount
    for i in range(len(instructionList)):
        #These are the instruction set steps
        DataHazardArray.append(['IF','ID','EX','MEM','WB'])
    
    for i in range(len(instructionList)):
        #If the insturction element is not the last one
        if (i<(len(instructionList)-1)):
            #If we find the instruction in the main array
            if (instructionList[i][0] in Baseline_DataHazardArray):
                #If we are not on the 2nd to list instruction
                if (i<(len(instructionList)-2)):
                    #Checking both the passed Instruction position + 2 to make sure there are no dependecies
                    if (instructionList[i][1] == instructionList[i+2][2]) or (instructionList[i][1] == instructionList[i+2][3]):
                        DataHazardArrayCounter += 1
                        DataHazardArray[i][4] = 'HZ'      #Found a hazard so set the Array Value to HZ
                        DataHazardArray[i+2][1] = 'HZ'    #Found a hazard so set the Array Value to HZ
                        stallArray[i+2] = stallArray[i+2] + [i]    #Storing the instruction that is causing the Hazard
                #Checking if the instruction i+1 trying to read from register that instruction i needs to write to
                if (instructionList[i][1] == instructionList[i+1][2]) or (instructionList[i][1] == instructionList[i+1][3]):
                    DataHazardArrayCounter += 1
                    DataHazardArray[i][4] = 'HZ'  
                    DataHazardArray[i+1][1] = 'HZ'    
                    stallArray[i+1] = stallArray[i+1] + [i] 
                #The SW instruction needs data for its first register by MEM stage
                if instructionList[i+1][0] == 'SW':
                    #Is the SW instruction trying to read from register that previous instruction needs to write to first
                    if (instructionList[i][1] == instructionList[i+1][1]):
                        DataHazardArrayCounter += 1                  
                        DataHazardArray[i][4] = 'HZ'  
                        DataHazardArray[i+1][1] = 'HZ'
                        stallArray[i+1] = stallArray[i+1] + [i]
    print('\n')
    #Just trying to make the output look a little cleaner
    for i in range(len(instructionList)):
        spaces += 1
        DataHazardArray[i] = [' ']*spaces + DataHazardArray[i]    
    print(str(DataHazardArrayCounter) + ' data hazard(s) found!')
    print("HZ represents a hazard in the pipeline stage where it appears:\n")
    #Print out the pipeline
    makeInstructionsString(instructionList, DataHazardArray)
    print('\n')
    print("Solution with adding stalls:")

    #For each element in the stallArray contains a list of the instruction indexes that cause a data hazard for instruction i
    for i in range(len(stallArray)):
        #For loop to iterate throug all instructions that cause a hazard for the instruction
        for j in range(len(stallArray[i])):
            if 'HZ' in DataHazardArray[stallArray[i][j]]:
                #Saving the index value of 'HZ' in row that caused hazard in WB stage
                hazardIndex = DataHazardArray[stallArray[i][j]].index('HZ')
                #Saving the index of 'HZ' in row that caused hazard in ID stage
                hazardIndex2 = DataHazardArray[i].index('HZ')
                #Value of how many columns apart are WB and ID hazards
                diff = hazardIndex - hazardIndex2
                #For loop to iterate over the amount of columns separating the hazards
                for k in range(diff):
                    #Setting stalls for the instruction i
                    addStall = i 
                    #Adding stalls to every row from instruction i to the last instruction
                    while addStall<len(instructionList): 
                        temp = 0
                        #Adding whitespace to row to help with printing
                        DataHazardArray[addStall] = [' '] + DataHazardArray[addStall]
                        while DataHazardArray[addStall][temp] == ' ':
                            temp += 1
                        #Adding Stall 'ST' to string
                        DataHazardArray[addStall][temp-1] = 'ST'
                        addStall += 1
                hazardIndex = DataHazardArray[stallArray[i][j]].index('HZ')  
                hazardIndex2 = DataHazardArray[i].index('HZ')
                #Changing HZ to WB in row that caused hazard in WB stage
                DataHazardArray[stallArray[i][j]][hazardIndex] = 'WB'
                #Changing HZ to ID in row that caused hazard in ID stage
                DataHazardArray[i][hazardIndex2] = 'ID'
    for i in range(len(DataHazardArray)):
    #Stall have been added now change any remaining hazards to ID 
        if 'HZ' in DataHazardArray[i]:
            DataHazardArray[i][DataHazardArray[i].index('HZ')] = 'ID'
    #Finally print out pipeline timing sequence
    makeInstructionsString(instructionList, DataHazardArray)

    #Corrected array of timing sequence showing data hazards fixed by forwarding
    NewDataArray = []
    spaces = -1
    #Array that holds how many data hazards per instruction which can't be fixed by forwarding - needs to stall
    StillDataHazardStalls = [0]*instructionCount
    for i in range(len(instructionList)):
        NewDataArray.append(['IF','ID','EX','MEM','WB'])
    
    for i in range(len(instructionList)):
        #As long as instruction is not the last one
        if i<(len(instructionList)-1):
            if instructionList[i][0] in Baseline_DataHazardArray:
                #IF data hazard is found between instruction i and i+1
                if (instructionList[i][1] == instructionList[i+1][2]) or (instructionList[i][1] == instructionList[i+1][3]):
                    #IF LW doesn't have its data until Memory stage, but instruction i+1 needs it by Excute stage we need to stall
                    if (instructionList[i][0] == 'LW') and (instructionList[i+1][0] in Baseline_DataHazardArray):
                        #Adding stall for row starting from instruction i+1
                        addStall = i+1
                        while addStall<len(instructionList):
                            StillDataHazardStalls[addStall] += 1
                            temp = 0
                            NewDataArray[addStall] = [' '] + NewDataArray[addStall]
                            while NewDataArray[addStall][temp] == ' ':
                                temp += 1
                            NewDataArray[addStall][temp-1] = 'ST'
                            addStall += 1
    print('\n')
    for i in range(len(instructionList)):
        #Adding spaces in NewDataArray rows to show timing sequence, just to help with readability
        spaces += 1
        NewDataArray[i] = [' ']*spaces + NewDataArray[i]
    print("The new pipeline timing sequence after forwarding was applied:\n")
    #Now printing out the pipeline timing sequence
    makeInstructionsString(instructionList, NewDataArray)
    print('\n')

    #CONTROL HAZARDS Section
    print("\nCONTROL HAZARDS\n")
    #Array to store the timing sequence for control hazards
    ControlHazardArray = []
    #Counter for control hazards found
    ControlHazardCount = 0
    #Counter used to add spaces in ControlHazardArray rows to show timing sequence per instruction
    spaces = -1
    for i in range(len(instructionList)):
        #Adding a list of correct timing sequence for each instruction into control hazard array
        ControlHazardArray.append(['IF','ID','EX','MEM','WB'])
        #If instruction is a branch checks for a Branch
        if instructionList[i][0]=='BEQ':
            ControlHazardCount += 1
            #Setting hazard in instruction i IF stage - we will need to add stall
            ControlHazardArray[i][0] = 'HZ'
            print("Branch detected: instruction "+str(i+1))
    for i in range(len(instructionList)):
        #Adding spaces in array to help with printing readability
        spaces += 1
        ControlHazardArray[i] = [' ']*spaces + ControlHazardArray[i]
    print('\n')
    print(str(ControlHazardCount) + ' control hazard found!')
    print("HZ represents a hazard in the pipeline stage where it appears:\n")
    #Print out pipeline timing sequence
    makeInstructionsString(instructionList, ControlHazardArray)
    print('\n')

    #Array of corrected timing sequence (Hazards replaced with Stalls)
    ControlHazardArray2 = []
    spaces = -1
    for i in range(len(instructionList)):
        ControlHazardArray2.append(['IF','ID','EX','MEM','WB'])
        if instructionList[i][0]=='BEQ':
            #Adding a stall to each row, starting at i
            addStall = i
            while addStall<len(instructionList):
                temp = 0
                ControlHazardArray2[addStall] = [' '] + ControlHazardArray2[addStall]
                while ControlHazardArray2[addStall][temp] == ' ':
                    temp += 1
                ControlHazardArray2[addStall][temp-1] = 'ST'
                addStall += 1
    for i in range(len(instructionList)):
        #Adding spaces in array to show timing sequence
        spaces += 1
        ControlHazardArray2[i] = [' ']*spaces + ControlHazardArray2[i]

    #Printing out the pipeline timing sequence
    makeInstructionsString(instructionList, ControlHazardArray2)
    print('\n')

    #STRUCTURAL HAZARDS Section
    print("\nSTRUCTURAL HAZARDS\n")
    #Array of timing sequence of structural hazards
    StructureHazardArray = []
    #Counter for structural hazards
    StructureHazardCount = 0
    #Counter to add spaces in StructureHazardArray rows to help with readability
    spaces = -1
    for i in range(len(instructionList)):
        #Appending instruction set into structural hazard array
        StructureHazardArray.append(['IF','ID','EX','MEM','WB'])
        #If we are at least at the 3rd Insturction and the Instruction List is LW or SW 
        if (i>=3 and (instructionList[i-3][0]=='LW' or instructionList[i-3][0]=='SW')):
            StructureHazardCount += 1
            StructureHazardArray[i][0] = 'HZ'   #Found hazard in Instruction Fetch stage
            StructureHazardArray[i-3][3] = 'HZ' #Found hazard in Memory Access stage 
    for i in range(len(instructionList)):
        #Add spacing to improve readability
        spaces += 1
        StructureHazardArray[i] = [' ']*spaces + StructureHazardArray[i]
        
    print('\n')
    print(str(StructureHazardCount) + ' structural hazard found!')
    print("HZ represents a hazard in the pipeline stage where it appears:\n")
    #Printing out pipeline timing sequence
    makeInstructionsString(instructionList, StructureHazardArray)
    print('\n')
    
    print('Solution with adding stalls:\n')
    #Array with corrected timing sequence
    StructureHazardArray2 = []
    stalls = 0
    for i in range(len(instructionList)):
        #Adding a space to stalls variable to improve readability
        StructureHazardArray2.append([' ']*stalls + ['IF','ID','EX','MEM','WB'])
        stalls += 1
    #Setting the Structure Hazard Stalls to pass to subroutine    
    StructuceHazardStalls = [0]*instructionCount
    #Subroutine adds stalls to each row to fix structural hazards and returns the new array
    finalArray = StructureHazardFix(instructionList,StructureHazardArray2,StructuceHazardStalls)

    print("Here is the combined timing sequence combining the 3 hazard solutions:\n")
    #This subroutine adds a stall if needed
    StructureHazardWithBranch(instructionList,finalArray,StillDataHazardStalls)

#Make the Instruction List into a String
def makeInstructionsString(instructionList, array):
    #Looping through the input array (instruction list)
    for i in range(len(instructionList)):
        instr = ''
        for j in range(len(array[i])):
            instr += array[i][j] + ' '
        if len(instructionList[i][0]) == 3:
            print(str(i+1)+ '. '+' ' + str(instructionList[i][0]) + ': ' + str(instr))
        elif len(instructionList[i][0]) == 2:
            print(str(i+1)+ '. '+'  ' + str(instructionList[i][0]) + ': ' + str(instr))
        else:
            print(str(i+1)+ '. '+str(instructionList[i][0]) + ': ' + str(instr))    

#This subroutine adds stalls to the row to fix the structural hazards
def StructureHazardFix(instructionList,StructureHazardArray2,stallArray2):
    for i in range(len(instructionList)):
        MEMInstructIndex = 0
        IFInstructIndex = -1
        #If the instruction is a load or store
        if instructionList[i][0] == 'LW' or instructionList[i][0] == 'SW':
            for j in range(len(StructureHazardArray2[i])):
                #We have found a Memory Access structural hazard
                if StructureHazardArray2[i][j] == 'MEM':
                    MEMInstructIndex = j     #Save the Position
            k = i+1
            #Loop until we either find a Instruction Fetch Hazard or there isn't one
            while k<len(instructionList) and IFInstructIndex == -1:
                #Found an Instruction Fetch Hazard
                if StructureHazardArray2[k][MEMInstructIndex] == 'IF':
                    IFInstructIndex = k
                k += 1
            #Break loop since we did not find a Instruction Fetch Hazard
            if IFInstructIndex == -1:
                break
            #Set value to the array index of the hazard (if there is one)
            addStall = IFInstructIndex
            while addStall<len(instructionList):
                temp = 0
                #Adding space to row that has stall added to help with readability
                StructureHazardArray2[addStall] = [' '] + StructureHazardArray2[addStall]
                #Get past the new spaces added
                while StructureHazardArray2[addStall][temp] == ' ':
                    temp += 1
                if stallArray2[addStall] == 0:
                    #Replace the space with ST for stall
                    StructureHazardArray2[addStall][temp-1] = 'ST'
                else:
                    #Stall was added so nothing needs to be added - decrementing stallArray2
                    stallArray2[addStall] = (stallArray2[addStall] - 1)
                addStall += 1

    makeInstructionsString(instructionList, StructureHazardArray2)
    print('\n')
    #Return the new Instruction Pipeline
    return StructureHazardArray2

#Takes the original instructions array and adds stalls as needed with a branch instruction
def StructureHazardWithBranch(instructionList,StructureHazardArray2,stallArray3):
    for i in range(len(instructionList)):
        #If the instruction is a Branch - add a stall
        if instructionList[i][0]=='BEQ':
            addStall = i
            while addStall<len(instructionList):
                temp = 0
                StructureHazardArray2[addStall] = [' '] + StructureHazardArray2[addStall] 
                while StructureHazardArray2[addStall][temp] == ' ':
                    temp += 1
                StructureHazardArray2[addStall][temp-1] = 'ST'
                addStall += 1
    #Prints out Pipeline
    makeInstructionsString(instructionList, StructureHazardArray2)
    print('\n')
            

pipelineHazardDectector()