#import memory from assembler
from Assembler_543570 import mem, d2b

#change recursion limit to allow for bigger numbers
import sys
sys.setrecursionlimit(10**9)

#function to convert binary string to decimal
def b2d(s):
    l = len(s)
    sr = s[::-1]
    num = 0
    for x in range(l):
        num += int(sr[x]) * (pow(2, x))
    return num

#initialize address array
ad = []

#~~~~~~ONLY CHANGE THIS VALUE FOR DIFFERENT SEQUENCES~~~~~
val = 1738
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#append various location required, refer C code of fibonacci
ad.append(0) #memory location of a => [0]
ad.append(1) #memory location of b => [1]
ad.append(0) #memory location of temp (extra location) => [2]
ad.append(val) #memory location of n (inputed by user) => [3]
ad.append(val) #memory location of n (copy for odd use) => [4]
ad.append(0) #memory location of o => [5]
ad.append(10) #memory location used for modulus with 10 to get last digit=> [6]
ad.append(0) #memory location to store even number => [7]
ad.append([]) #list for fib sequence => [8]

#intiaize all registers to 0
pc = 0   #program count
mar = 0  #memory address register
mbr = 0  #memory buffer register
ir = 0   #instruction register
mq = 0   #multiplication/quotient
ac = 0   #accumalator
ibr = 0  #instruction buffer register
x = 0    #this is used to acces certain parts of memory (acts as mar <- mem), 
         #and fetch cycle executes when x is incremented

#function to print values of addresses and registers
def p():
    print(ad)
    print("ac: ", ac)
    print("ibr: ", ibr)
    print("ir: ", ir)
    print("mar: ", mar)
    print("mq: ", mq)

#ALWAYS GLOBALISE ALL REGISTERS TO MAKE CHANGES

#execute cycle
def execute():
    global pc, mar, mbr, ir, mq, ac, ibr, x
    
    #convert address in mar to decimal
    loc_dec = b2d(str(mar))
    
    #check opcodes and perform instructions
    if ir == '011111':      #DEC
        ac = ad[loc_dec]
        ac -= 1
        ad[loc_dec] = ac
    elif ir == '110000':    #ISODD
        if mq % 2 == 1:
            ac += 1
        else:
            pass
    elif ir == '001001':    #LOAD1
        mq = ad[loc_dec]
    elif ir == '001010':    #LOAD2
        ac = mq
    elif ir == '000001':    #LOAD3
        ac = ad[loc_dec]
    elif ir == '000010':    #LOAD4
        ac = -ad[loc_dec]
    elif ir == '000011':    #LOAD5
        ac = abs(ad[loc_dec])
    elif ir == '000100':    #LOAD6
        ac = -abs(ad[loc_dec])
    elif ir == '100001':    #STOR1
        ad[loc_dec] = ac
    elif ir == '010010':    #STOR2
        ad[loc_dec] = ad[loc_dec][0:6] + d2b(ac)[len(d2b(ac) - 4):]
    elif ir == '010011':    #STOR3
        ad[loc_dec] = ad[loc_dec][0:6] + d2b(ac)[:4]
    elif ir == '000101':    #ADD1
        #we append value of a here as this gives us each increment of fibonacci
        #this is just for verification purposes
        ad[8].append(ad[0])
        ac += ad[loc_dec]
    elif ir == '000111':    #ADD2
        ac += abs(ad[loc_dec])
    elif ir == '001100':    #DIV
        ac = ac % ad[loc_dec]
        mq = ac // ad[loc_dec]
    elif ir == '001111':    #JUMP+1
        if ac > 0:
            ir = mem[loc_dec]
            mar = mem[loc_dec]
            #set x as (memory loc - 2) as x starts from 0 (first -1) and we increment by 1 
            #when RI has been executed (second -1)
            x = loc_dec - 2
        else:
            pass
    elif ir == '010000': #JUMP+2
        if ac > 0:
            ir = mem[loc_dec][10:16]
            mar = mem[loc_dec][16:]
            ibr = 0 #RI is already being executed
            #set x as (memory loc - 2) as x starts from 0 (first -1) and we increment by 1 
            #when RI has been executed (second -1)
            x = loc_dec - 2
        else:
            pass
    elif ir == '001101': #JUMP1
        ir = mem[loc_dec]
        mar = mem[loc_dec]
        #set x as (memory loc - 2) as x starts from 0 (first -1) and we increment by 1 
        #when RI has been executed (second -1)
        x = loc_dec - 2
    elif ir == '001101': #JUMP2
        ir = mem[loc_dec][10:16]
        mar = mem[loc_dec][16:]
        ibr = 0 #RI is already being executed
        #set x as (memory loc - 2) as x starts from 0 (first -1) and we increment by 1 
        #when RI has been executed (second -1)
        x = loc_dec - 2
    elif ir == '000110':    #SUB1
        ac -= ad[loc_dec]
    elif ir == '001000':    #SUB2
        ac -= abs(ad[loc_dec])
    elif ir == '001011':    #MUL
        prod = mq * ad[loc_dec]
        prod_bi = d2b(prod)
        ac = prod_bi[0:len(prod_bi//2)]
        mq = prod_bi[len(prod_bi//2):]
    elif ir == '010100':    #LSH
        ac << 1
    elif ir == '010101':    #RSH
        ac >> 1
    elif ir == '000000':    #HALT
        #print entire fib sequence stored in address array
        print("Given value: ", ad[4])
        print("Fib: ", end ='')
        for x in ad[8]:
            print(x, end = ' ')
        print()
        #print number of odd and even numbers in the sequence
        print("Odd:", ad[5])
        print("Even:", ad[7])
        exit()
    
    #checks of RI has been executed or not
    if ibr != 0: 
        #if RI is not executed, execute that next
        #p()
        ir = ibr[:6]
        mar = ibr[6:]
        ibr = 0
        execute()
    else:
        #otherwise go to next fetch cycle
        #p()
        #increment x to go to next memory loc
        x += 1
        fetch()
    
def decode():
    global pc, mar, mbr, ir, mq, ac, ibr, x
    
    #ir is first 6 digits of mbr
    ir = mbr[:6]
    #mar is next 4 digits of mbr
    mar = mbr[6:10]
    #set pc to next instruction
    pc = mem[x]
    
    #if RI and LI both exist, ibr becomes last 10 digits of mbr
    if len(mbr) == 20:
        ibr = mbr[10:]
    #otherwise, ibr is 0, i.e., nothing to execute from RI
    else:
        ibr = 0
        
    #call execute after decode
    execute() 

def fetch():
    global pc, mar, mbr, ir, mq, ac, ibr, x
    
    #print("--------\nx: ", x, "\n--------")
        
    #mar gets what is in pc
    mar = pc
    #mbr gets xth instruction set from memory
    mbr = mem[x]
    decode()

#initialize pc to first instruction of memory
pc = mem[0]
fetch()