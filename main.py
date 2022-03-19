import random
import pygame, sys
from pygame.locals import *
import time
import struct
memory = [0b00000000]*4096
graphic = [0]*32
for i in range(32):
    graphic[i]=[0]*100
stack = [0]*24
romStart=0x0200
key = [0b0]*16
#font set
memory[0]=0xf0
memory[1]=0x90
memory[2]=0x90
memory[3]=0x90
memory[4]=0xf0
memory[5]=0x20
memory[6]=0x60
memory[7]=0x20
memory[8]=0x20
memory[9]=0x70
memory[10]=0xf0
memory[11]=0x10
memory[12]=0xf0
memory[13]=0x80
memory[14]=0xf0
memory[15]=0xf0
memory[16]=0x10
memory[17]=0xf0
memory[18]=0x10
memory[19]=0xf0#3
memory[20]=0x90
memory[21]=0x90
memory[22]=0xf0
memory[23]=0x10
memory[24]=0x10
memory[25]=0xf0
memory[26]=0x80
memory[27]=0xf0
memory[28]=0x10
memory[29]=0xf0
memory[30]=0xf0
memory[31]=0x80
memory[32]=0xf0
memory[33]=0x90
memory[34]=0xf0
memory[35]=0xf0
memory[36]=0x10
memory[37]=0x20
memory[38]=0x40
memory[39]=0x40
memory[40]=0xf0
memory[41]=0x90
memory[42]=0xf0
memory[43]=0x90
memory[44]=0xf0
memory[45]=0xf0
memory[46]=0x90
memory[47]=0xf0
memory[48]=0x10
memory[49]=0xf0
memory[50]=0xe0
memory[51]=0x90
memory[52]=0xe0
memory[53]=0x90
memory[54]=0xe0
memory[55]=0xf0
memory[56]=0x80
memory[57]=0x80
memory[58]=0x80
memory[59]=0xf0
memory[60]=0xe0
memory[61]=0x90
memory[62]=0x90
memory[63]=0x90
memory[64]=0xe0
memory[65]=0xf0
memory[66]=0x80
memory[67]=0xf0
memory[68]=0x80
memory[69]=0xf0
memory[70]=0xf0
memory[71]=0x80
memory[72]=0xf0
memory[73]=0x80
memory[74]=0x80
memory[75]=0x0
memory[76]=0x0
memory[77]=0x0
memory[78]=0x0
memory[79]=0x0

#and f opcode not finish 

class Chip8:
    def __init__(self):
        self.opcode = 0b0000000000000000
        self.reg = [0b00000000]*16
        self.regI = 0
        self.pc = 0x0200
        self.sp = 0
        self.delayTimer = 60
        self.soundTimer = 60
    def cycle(self):
        self.opcode = (memory[self.pc]<<8) | (memory[self.pc+1])
        opFirstByte = (self.opcode & 0xf000)>>12
        opSecondByte = (self.opcode & 0x0f00)>>8
        opThirdByte = (self.opcode & 0x00f0)>>4
        opFourthByte = (self.opcode & 0x000f)  
        if opFirstByte == 0:
            if (self.opcode&0x0f00==0):
                if (self.opcode&0x000f==0): #clear screen
                    for i in range(32):
                        graphic[i]=[0]*64
                elif(self.opcode&0x000f==0xe):#return from a subroutine
                    self.pc=stack[self.sp-1]
                    self.sp-=1
            else:
                print("noop") #no need to implementation?
        elif opFirstByte == 1:#jump to address NNN
            self.pc = (self.opcode&0x0fff)-2
        elif opFirstByte == 2:#call subroutine at NNN
            stack[self.sp] = self.pc
            self.sp+=1
            self.pc = (self.opcode&0x0fff)-2

        elif opFirstByte == 3:
            if self.reg[opSecondByte]==(self.opcode&0x00ff):
                self.pc+=2
        elif opFirstByte == 4:
            if self.reg[opSecondByte]!=(self.opcode&0x00ff):
                self.pc+=2
        elif opFirstByte == 5:  
            if self.reg[opSecondByte]==self.reg[opThirdByte]:
                self.pc+=2
        elif opFirstByte == 6:
            self.reg[opSecondByte]=self.opcode&0x00ff
        elif opFirstByte == 7:
            self.reg[opSecondByte]+=self.opcode&0x00ff
        elif opFirstByte == 8:
            if opFourthByte == 0x0:
                self.reg[opSecondByte]=self.reg[opThirdByte]
            elif opFourthByte ==0x1:
                self.reg[opSecondByte]=self.reg[opSecondByte] | self.reg[opThirdByte]
            elif opFourthByte ==0x2:
                self.reg[opSecondByte]=self.reg[opSecondByte] & self.reg[opThirdByte]
            elif opFourthByte ==0x3:
                self.reg[opSecondByte]=self.reg[opSecondByte] ^ self.reg[opThirdByte]
            elif opFourthByte ==0x4:
                self.reg[opSecondByte]=self.reg[opSecondByte] + self.reg[opThirdByte]
                if(self.reg[opSecondByte]>255):
                    self.reg[15]=1
                    self.reg[opSecondByte]-=256
                else:
                    self.reg[15]=0
            elif opFourthByte ==0x5:
                self.reg[opSecondByte]=self.reg[opSecondByte] - self.reg[opThirdByte]
                if(self.reg[opSecondByte]<0):
                    self.reg[15]=0
                    self.reg[opSecondByte]+=256
                else:
                    self.reg[15]=1
            elif opFourthByte ==0x6:
                self.reg[15]=sel.reg[opSecondByte]%2
                self.reg[opSecondByte] = self.reg[opSecondByte]>>1
            elif opFourthByte == 0x7:
                self.reg[opSecondByte]=sel.reg[opThirdByte] - self.reg[opSecondByte]
                if(self.reg[opSecondByte]<0):
                    self.reg[15]=0
                    self.reg[opSecondByte]+=256
                else:
                    self.reg[15]=1
                
            elif opFourthByte == 0xE:
                self.reg[15]=(self.reg[opSecondByte]>>7)%2
                self.reg[opSecondByte]=(self.reg[opSecondByte]<<1)%256

        elif opFirstByte == 9: #skip next ins if vx=vy
            if self.reg[opSecondByte]!=self.reg[opThirdByte]:
                self.pc+=2
        elif opFirstByte == 10:#A
            self.regI = self.opcode&0x0fff
        elif opFirstByte == 11:
            self.pc = self.reg[0]+(self.opcode&0x0fff)-2
        elif opFirstByte == 12:
            self.reg[opSecondByte] = (self.opcode&0x00ff) & random.randint(0,255)
        elif opFirstByte == 13:
            for i in range(0,opFourthByte):
                for j in range(8):
                    #print(self.reg[opThirdByte]+i)
                    #print(self.reg[opSecondByte]+j)
                    #print(self.regI+i)
                    if(opThirdByte<len(self.reg) and self.regI+i< len(memory)):
                        if(self.reg[opThirdByte]+i<32 and self.reg[opSecondByte]+j < 100):
                            if(graphic[self.reg[opThirdByte]+i][self.reg[opSecondByte]+j]+((memory[self.regI+i]>>(7-j))%2)>=2):
                                self.reg[15]=1
                            else:
                                self.reg[15]=0
                            graphic[self.reg[opThirdByte]+i][self.reg[opSecondByte]+j]^=((memory[self.regI+i]>>(7-j))%2)
                    
        elif opFirstByte == 14:
            if(opThirdByte==0x9):
                if key[self.reg[opSecondByte]]==1:
                    self.pc+=2
            elif(opThirdByte == 0xA):
                if key[self.reg[opSecondByte]]==0:
                    self.pc+=2
        elif opFirstByte == 15:
            if(self.opcode&0x00ff==0x0007):
                self.reg[opSecondByte]=self.delayTimer
            elif(self.opcode&0x00ff==0x000A):
                reg[opSecondByte]=int(input('wait for input'))
                #wait a key store in reg X
            elif(self.opcode&0x00ff==0x0015):
                self.delayTimer=self.reg[opSecondByte]
            elif(self.opcode&0x00ff==0x0018):
                self.soundTimer=self.reg[opSecondByte]
            elif(self.opcode&0x00ff==0x001E):
                self.regI+=self.reg[opSecondByte]
            elif(self.opcode&0x00ff==0x0029):
                self.regI=self.reg[opSecondByte]*5#set the regI to the location of font reg[opSecondByte]
            elif(self.opcode&0x00ff==0x0033):
                memory[self.regI] = (int(self.reg[opSecondByte]/100))%10
                memory[self.regI+1] = (int(self.reg[opSecondByte]/10))%10
                memory[self.regI+2] = int(self.reg[opSecondByte])%10
            elif(self.opcode&0x00ff==0x0055):
                for i in range(opSecondByte+1):
                    memory[self.regI+i]=self.reg[i]
            elif(self.opcode&0x00ff==0x0065):
                for i in range(opSecondByte+1):
                    self.reg[i]=memory[self.regI+i]
        #print(self.pc)
        print(hex(self.opcode))
        self.pc+=2
        self.soundTimer-=1
        self.delayTimer-=1
        if(self.soundTimer<0):
            self.soundTimer=60
        if(self.delayTimer<0):
            self.delayTimer=60

chip8 = Chip8()

with open("./roms/PONG", "rb") as rom:
    byte = rom.read(1)
    while byte:
        memory[romStart]=struct.unpack('B',byte)[0]
        #print(struct.unpack('B',byte))
        romStart+=1
        byte = rom.read(1)

    pygame.init()
    DISPLAY=pygame.display.set_mode((66*5,32*5),0,32)

    WHITE=(255,255,255)
    BLACK=(0,0,0)

    DISPLAY.fill(WHITE)

while(1):
    chip8.cycle()
    #print(graphic)
    for event in pygame.event.get():
        if event.type==QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key==pygame.K_1:
                key[1]=1
            if event.key==pygame.K_2:
                key[2]=1
            if event.key==pygame.K_3:
                key[3]=1
            if event.key==pygame.K_4:
                key[12]=1
            if event.key==pygame.K_q:
                key[4]=1
            if event.key==pygame.K_w:
                key[5]=1
            if event.key==pygame.K_e:
                key[6]=1
            if event.key==pygame.K_r:
                key[13]=1
            if event.key==pygame.K_a:
                key[7]=1
            if event.key==pygame.K_s:
                key[8]=1
            if event.key==pygame.K_d:
                key[9]=1
            if event.key==pygame.K_f:
                key[14]=1
            if event.key==pygame.K_z:
                key[10]=1
            if event.key==pygame.K_x:
                key[0]=1
            if event.key==pygame.K_c:
                key[11]=1
            if event.key==pygame.K_v:
                key[15]=1
        if event.type == pygame.KEYUP:
            if event.key==pygame.K_1:
                key[1]=0
            if event.key==pygame.K_2:
                key[2]=0
            if event.key==pygame.K_3:
                key[3]=0
            if event.key==pygame.K_4:
                key[12]=0
            if event.key==pygame.K_q:
                key[4]=0
            if event.key==pygame.K_w:
                key[5]=0
            if event.key==pygame.K_e:
                key[6]=0
            if event.key==pygame.K_r:
                key[13]=0
            if event.key==pygame.K_a:
                key[7]=0
            if event.key==pygame.K_s:
                key[8]=0
            if event.key==pygame.K_d:
                key[9]=0
            if event.key==pygame.K_f:
                key[14]=0
            if event.key==pygame.K_z:
                key[10]=0
            if event.key==pygame.K_x:
                key[0]=0
            if event.key==pygame.K_c:
                key[11]=0
            if event.key==pygame.K_v:
                key[15]=0
    DISPLAY.fill(WHITE)
    for i in range(32):
        for j in range(64):
            if(graphic[i][j]!=0):
                pygame.draw.rect(DISPLAY,BLACK,(j*5,i*5,5,5))


    pygame.display.update()
    time.sleep(0.001)
