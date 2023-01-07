#!/usr/bin/env python

from collections import namedtuple, defaultdict
import struct

# Author: Daniel Ozminkowski

# PROGRAM_STATE_MESSAGE = 25

programStateMessageHeaderFmt = '!Qb'

ProgramStateMessageHeader = namedtuple("ProgramStateMessageHeader", "timestamp robotMessageType")

class ProgramState():
    '''
    Object decoding Program State messages from Primary Interface.
    '''

    variableNames = []
    variableValues = []
    

    def __init__(self, content):
        self.content = content
        self.type_ = None
        self.programRestarted = False
        self.updatedVariables = {}
        self.missedVariableSetup = False
        self.process()

    def process_setup(self):
        '''
        Decode variable names.
        '''
        self.type = 'setup'
        (startIndex, listOfVariables) = \
                         struct.unpack(
                             '!H'+ str(len(self.content)-9-2) + 's',
                             self.content[9:]
                             )
        listOfVariables = listOfVariables.split('\n')[:-1]
        
        # Assuming messages will just come in order
        # Not checking startIndex
        if startIndex == 0:
            self.programRestarted = True
            ProgramState.variableNames = []
            ProgramState.variableValues = []
        if startIndex >= len(ProgramState.variableNames):
            ProgramState.variableNames.extend(listOfVariables)
            ProgramState.variableValues.extend([None] * len(listOfVariables))

    def process_update(self):
        '''
        Decode new variable values.
        '''
        self.type_ = 'update'
        i = 9
        startIndex, = struct.unpack('!H', self.content[i:i+2])
        i += 2

        varNr = startIndex
        while i+1 < len(self.content):
            type_, value, size = self.__decodeTypeValue(self.content, i)
            i += size 
            if varNr >= len(ProgramState.variableValues):
                # Program was already started, but we didn't get the memo
                self.missedVariableSetup = True
                return
            if ProgramState.variableValues[varNr] != value:
                ProgramState.variableValues[varNr] = value
                self.updatedVariables[ProgramState.variableNames[varNr]] = value
            varNr +=1
            assert self.content[i] == '\n'
            i += 1
        
    def process(self):
        '''
        Check message type and call process_setup() or process_update().
        '''
        (timestamp, type_) = ProgramStateMessageHeader._make(
        struct.unpack(programStateMessageHeaderFmt, self.content[:9])
        )

        # Global variable setup
        if type_ == 0:
            self.process_setup()
            
        # Global variable update
        elif type_ == 1:
            self.process_update()
            
        else:
            print 'Unknown package. Package type/length:',  packtype, '/', packlen, \
              'msgType:', programStateMessageHeader.robotMessageType

    def __decodeTypeValue(self, data, i):
        '''
        Input parameters:
        data:  raw data received from UR
        i:     position where to start reading data
        Output parameters:
        type:  type of variable
        value: value
        size:  size of decoded data
        '''
        start_i = i
        variableType, = struct.unpack('!B', data[i])
        
        i+=1
        
        # None
        if variableType == 0:
            value = None
        # Constant string
        elif variableType == 3:
            length, = struct.unpack('!H', data[i:i+2])
            i+=2
            value, = struct.unpack('!'+str(length)+'s', data[i:i+length])
            i += length
        # Variable string
        elif variableType == 4:
            length, = struct.unpack('!H', data[i:i+2])
            i+=2
            value, = struct.unpack('!'+str(length)+'s', data[i:i+length])
            i += length
        # List
        elif variableType == 5:
            listLength, = struct.unpack('!H', data[i:i+2])
            i += 2
            list_ = [0] * listLength
            j = 0
            while j < listLength:
                itemType, itemValue, itemSize = self.__decodeTypeValue(data, i)
                i += itemSize
                list_[j] = itemValue
                j += 1
            value = list_
        # Pose
        elif variableType == 10:
            value = struct.unpack('!ffffff', data[i:i+24])
            i += 6*4
        # Bool
        elif variableType == 12:
            value, = struct.unpack('!?', data[i:i+1])
            i += 1
        # Num
        elif variableType == 13:
            #print len(data[i:])
            #print [ str(ord(ch)) for ch in globalVariableUpdatePayload ]
            exit()
        # Integer
        elif variableType == 14:
            value, = struct.unpack('!i', data[i:i+4])
            i += 4
        # Float
        elif variableType == 15:
            value,  = struct.unpack('!f', data[i:i+4])
            i += 4
        else:
            print 'Unknown data type in GlobalVariableUpdateMessage'
        
        return variableType, value, i-start_i
