import random


class Chip8:
    def __init__(self):
        self.opcode = 0b0000000000000000
        self.reg = [0b00000000]*16
        self.regI = 0b0000000000000000
        self.pc = 0
        self.delayTimer = 0
        self.soundTimer = 0
    def cycle(self):
        self.opcode = memory[self.pc]<<8 | memory[self.pc+1]
        opFirstByte = (self.opcode & 0xf000)>>12
        opSecondByte = (self.opcode & 0x0f00)>>8
        opThirdByte = (self.opcode & 0x00f0)>>4
        opFourthByte = (self.opcode & 0x000f)  
        if opFirstByte == 0:
            if (self.opcode&0x0f00==0):
                if (self.opcode&0x000f==0):
                    for i in range(32):
                        graphic[i]=[0]*32
                elif(self.opcode&0x000f==E):
                    self.pc=stack[sp-1]
                    sp-=1
            else:
                print("noop") #no need to implementation?
        elif opFirstByte == 1:
            self.pc = self.opcode&0x0fff
        elif opFirstByte == 2:#call subroutine at NNN
            stack[sp] = pc+2
            sp+=2
            self.pc = self.opcode&0x0fff
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
            self.reg[(self.opcode&0x0f00)>>8]=self.opcode&0x00ff
            print(self.reg[(self.opcode&0x0f00)>>8])
            print((self.opcode&0x0f00)>>8)
        elif opFirstByte == 7:
            self.reg[(self.opcode&0x0f00)>>8]+=self.opcode&0x00ff
        elif opFirstByte == 8:
            if opFourthByte == 0x0:
                self.reg[opSecondByte]=self.reg[opThirdByte]
            elif opFourthByte ==0x1:
                self.reg[opSecondByte]=sel.reg[opSecondByte] | self.reg[opThirdByte]
            elif opFourthByte ==0x2:
                self.reg[opSecondByte]=sel.reg[opSecondByte] & self.reg[opThirdByte]
            elif opFourthByte ==0x3:
                self.reg[opSecondByte]=sel.reg[opSecondByte] ^ self.reg[opThirdByte]
            elif opFourthByte ==0x4:
                self.reg[opSecondByte]=sel.reg[opSecondByte] + self.reg[opThirdByte]
                if(self.reg[opSecondByte]>255):
                    self.reg[15]=1
                    self.reg[opSecondByte]-=255
                else:
                    self.reg[15]=0
            elif opFourthByte ==0x5:
                self.reg[opSecondByte]=sel.reg[opSecondByte] - self.reg[opThirdByte]
                if(self.reg[opSecondByte]<0):
                    self.reg[15]=0
                    self.reg[opSecondByte]+=255
                else:
                    self.reg[15]=1
            elif opFourthByte ==0x6:
                self.reg[15]=sel.reg[opSecondByte]%2
                self.reg[opSecondByte] = self.reg[opSecondByte]>>1
            elif opFourthByte == 0x7:
                self.reg[opSecondByte]=sel.reg[opThirdByte] - self.reg[opSecondByte]
                if(self.reg[opSecondByte]<0):
                    self.reg[15]=0
                    self.reg[opSecondByte]+=255
                else:
                    self.reg[15]=1
                
            elif opFourthByte == 0xE:
                self.reg[15]=self.reg[opSecondByte]>>7
                self.reg[opSecondByte]=self.reg[opSecondByte]<<1

        elif opFirstByte == 9:
            if self.reg[opSecondByte]!=self.reg[opThirdByte]:
                self.pc+=2
        elif opFirstByte == 10:#A
            self.regI = self.opcode&0x0fff
        elif opFirstByte == 11:
            self.pc = self.reg[0]+(self.opcode&0x0fff)
        elif opFirstByte == 12:
            self.reg[opSecondByte] = (self.opcode&0x00ff) & random.randint(0,255)
        elif opFirstByte == 13:
            for i in range(opFourthByte):
                for j in range(8):
                    if(graphic[opSecondByte+j][opThirdByte+i]+((memory[self.regI+i]>>(7-j))%2)==2):
                        self.reg[15]=1
                    else:
                        self.reg[15]=0
                    graphic[opSecondByte+j][opThirdByte+i]=graphic[opSecondByte+j][opThirdByte+i]^((memory[self.regI+i]>>(7-j))%2)
                    
        elif opFirstByte == 14:
            if(opThirdByte==0x9):
                if key[opSecondByte]==1:
                    self.pc+=2
            elif(opThirdByte == 0xA):
                if key[opSecondByte]==0:
                    self.pc+=2
        elif opFirstByte == 15:
            if(self.opcode&0x00ff==0x0007):
                self.reg[opSecondByte]=self.delayTimer
            elif(self.opcode&0x00ff==0x000A):
                print("not implement now")
                #wait a key store in reg X
            elif(self.opcode&0x00ff==0x0015):
                self.delayTimer=self.reg[opSecondByte]
            elif(self.opcode&0x00ff==0x0018):
                self.soundTimer=self.reg[opSecondByte]
            elif(self.opcode&0x00ff==0x001E):
                self.regI+=self.reg[opSecondByte]
            elif(self.opcode&0x00ff==0x0029):
                print("noop")#set the regI to the location of font reg[opSecondByte]
            elif(self.opcode&0x00ff==0x0033):
                memory[self.regI] = (self.reg[opSecondByte]/100)%10
                memory[self.regI+1] = (self.reg[opSecondByte]/10)%10
                memory[self.regI+2] = (self.reg[opSecondByte])%10
            elif(self.opcode&0x00ff==0x0055):
                for i in range(opSecondByte+1):
                    memory[self.regI+i]=self.reg[i]
            elif(self.opcode&0x00ff==0x0065):
                for i in range(opSecondByte+1):
                    self.reg[i]=memory[self.regI+i]
        self.pc+=2


memory = [0b00000000]*4096
interpreter = [0b00000000]*512
graphic = [0]*64
for i in range(32):
    graphic[i]=[0]*32
stack = [0]*24
sp = 0
key = [0b0]*16
chip8 = Chip8()
memory[4]=0x63
memory[5]=0x55
for i in range(60):
    chip8.cycle()
    print(graphic)