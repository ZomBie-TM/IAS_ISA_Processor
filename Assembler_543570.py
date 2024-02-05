#opcode is 6 digits
#address is 4 digits

#function to convert decimal -> binary (4-bit) string for address
def d2b(n): 
    res = bin(n).replace("0b", "")
    if len(res) != 4:
        num_of_zero = 4 - len(res)
        res = ("0" * num_of_zero) + res
    return res
    
#function to convert assembly inputs to opcodes
def convert(i):
    if(i == 'DEC'): #Gets value at M(X) to AC and decrements by 1, stores back to M(X)
        ele = '011111'
    elif(i == 'ISODD'): #Checks if value in MQ is odd, if yes, then adds 1 to AC
        ele = "110000"
    elif(i == 'LOAD1'): #Loads M(X) to MQ
        ele = "001001"
    elif(i == 'LOAD2'): #Loads MQ to AC
        ele = "001010"
    elif(i == 'LOAD3'): #Loads M(X) to AC
        ele = "000001"
    elif(i == 'LOAD4'): #Loads -M(X) to AC
        ele = "000010"
    elif(i == 'LOAD5'): #Loads |M(X)| to AC
        ele = "000011"
    elif(i == 'LOAD6'): #Loads -|M(X)| to AC
        ele = "000100"
    elif(i == 'STOR1'): #Stores value in AC to M(X)
        ele = "100001"
    elif(i == 'ADD1'): #Adds M(X) to AC and stores in AC
        ele = "000101"
    elif(i == 'ADD2'): #Adds |M(X)| to AC and stores in AC
        ele = "000111"
    elif(i == 'SUB1'): #Subtracts M(X) from AC and stores in AC
        ele = "000110"
    elif(i == 'SUB2'): #Subtracts |M(X)| from AC and stores in AC
        ele = "001000"
    elif(i == 'MUL'): #Multipies M(X) with MQ, stores MSBs in AC and LSBs in MQ
        ele = "001011"
    elif(i == 'DIV'): #Divides AC with M(X), stores quotient in MQ and remainder in AC
        ele = "001100"
    elif(i == 'JUMP+1'): #Checks if AC is positive, if true, then jumps to LI of M(X)
        ele = "001111"
    elif(i == 'JUMP+2'): #Checks if AC is positive, if true, then jumps to RI of M(X)
        ele = "010000"
    elif(i == 'JUMP1'): #Take LI of M(X) next
        ele = "001101"
    elif(i == 'JUMP2'): #Take RI of M(X) next
        ele = "001110"
    elif(i == 'LSH'): #Left shift AC by one bit (multiply by 2)
        ele = "010100"
    elif(i == 'RSH'): #Right shift AC by one bit (divide by 2)
        ele = "010101"
    elif(i == 'STOR2'): #Replace left address field of M(X) with 12 LSBs of AC
        ele = "010010"
    elif(i == 'STOR3'): #Replace right address field of M(X) with 12 LSBs of AC
        ele = "010011"
    else: #Halts the program if incorrect instruction
        ele = "000000"
    return ele

#open instruction file
f = open(r"C:\Users\dveer\OneDrive - iiit-b\Sem 2\EG212 - Computer Architecture\Project 1\543,570_Instructions.txt", "r")

#initialize memory array
mem=[]
ins = (
    'DEC', 'ISODD',
    'LOAD1', 'LOAD2', 'LOAD3', 'LOAD4', 'LOAD5', 'LOAD6',
    'STOR1', 'STOR2', 'STOR3',
    'JUMP1', 'JUMP2',
    'JUMP+1', 'JUMP+2',
    'ADD1', 'ADD2',
    'DIV', 'MUL',
    'SUB1', 'SUB2',
    'LSH', 'RSH')

#read each line in file
line_num = 1
for x in f:
    #split RI and LI
    i = x.split(" | ")
    #array to join RI and LI later in binary
    temp = []
    for ele in i:
        #stop memory appending if HALT given
        if ele == "HALT":
            temp.append("0000000000")
            break
        else:
            #split instruction from address
            s = ele.split(" ")
            instruc = s[0]
            #check if given instruction exists
            if instruc not in ins:
                print(f"ERROR in line {line_num}: Command {instruc} does not exist!")
                quit()
            #convert instruction to opcode
            op = convert(instruc)
            #checks if it's JUMP+ or JUMP
            if s[1][0:3] == "MQ,":
                l = s[1][5]
            #Checks if operation is with MQ, if yes, then use last memory location temporarily
            elif s[1][0:2] == "MQ":
                l = 15
            #Else opration is with M(X)
            else:
                l =s[1][2]
            #Get location in binary
            loc = d2b(int(l))
            
            #Get final one side instruction with opcode and address
            final_instruction = op + loc
            
            #append to temp array
            temp.append(final_instruction)
    line_num += 1
    
    #if temp has two instruction, join them to make one 20-bit instruction with LI and RI
    if len(temp) == 2:
        mem.append(temp[0] + temp[1])
    #otherwise just make one instruction and append to memory
    else:
        mem.append("".join(temp))