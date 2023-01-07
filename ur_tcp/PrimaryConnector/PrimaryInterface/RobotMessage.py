#!/usr/bin/env python

from collections import namedtuple
import struct

# Author: Daniel Ozminkowski

# ROBOT_MESSAGE = 20

robotMessageHeaderFmt = '!Qbb'

RobotMessageHeader = namedtuple("RobotMessageHeader", "timestamp source robotMessageType")

class RobotMessage:

    def __init__(self, content):
        self.content = content

    def messageFactory(self, type_, content):
        # Text
        if type_ == 0:
            text, = struct.unpack('!'+str(messageLength)+'s', content)
            return text
        # Label
        elif type_ == 1:
            (id, text) = struct.unpack('!i'+str(len(content)-4)+'s', content)
            return str(id)+':',text
        # Version
        elif type_ == 3:
            projectNameSize, = struct.unpack('!b', content[0])
            projectName, = struct.unpack('!'+ str(projectNameSize) + 's', content[1:1+projectNameSize])
            buildDateArraySize = len(content)-1-projectNameSize-1-1-4-4
            
            (majorVersion, minorVersion, bugFix, build, buildDate) = \
                           struct.unpack(
                               '!BBii'+ str(buildDateArraySize) + 's',
                               content[1+projectNameSize:]
                               )
            return projectName, '.'.join(
                (str(majorVersion),
                 str(minorVersion),
                 str(bugFix),
                 str(build))
                ), 'Build Date', \
                buildDate
        # SafetyMode
        elif type_ == 5:
            (robotMessageCode, robotMessageArgument, safetyModeType, textMessage) = \
                               struct.unpack('!iib'+str(len(content)-9)+'s', content)
            return 'SafetyMode code {0}, arg {1}, type {2}, message{3}'.format(
                  robotMessageCode, robotMessageArgument, 
                  safetyModeType, textMessage)
        # RobotComm
        elif type_ == 6:
            (robotMessageCode, robotMessageArgument, warningLevel, textMessage) = \
                               struct.unpack('!iii'+str(len(content)-3*4)+'s', content)
            return 'Robot Comm code {0}, arg {1}, warnLvl {2}, message {3}'.format(
                  robotMessageCode, robotMessageArgument, 
                  warningLevel, textMessage)
        # Key
        elif type_ == 7:
            (robotMessageCode, robotMessageArgument, titleSize) = \
                               struct.unpack('!iiB', content[:9])
            (messageTitle, textMessage) = \
                           struct.unpack('!'+str(titleSize)+'s'+str(len(content)-9-titleSize)+'s',
                                         content[9:])
            return 'Key code {0}, arg {1}, title {2}, message {3}'.format(
                robotMessageCode, robotMessageArgument, messageTitle, textMessage)
        # Request value
        elif type_ == 9:
            i = 0
            (requestID, requestedType) = struct.unpack('!II', content[:8])
            i += 8
            result = 'Request value ID {0}, type {1},'.format(requestID, requestedType)
            if requestedType == 8:
                (warning, error, blocking, titleLength) = \
                          struct.unpack('!???B', content[i:i+4])
                i += 4
                messageTitle, = struct.unpack('!'+str(titleLength)+'s', content[i:i+titleLength])
                i += titleLength
                result += 'warn {0}/err {1}/block {2}, title {3}, '.format(warning, error, blocking, messageTitle)
            (textMessage, ) = struct.unpack('!'+str(len(content)-i)+'s', content[i:])
            result += textMessage
            return result
        else:
            print str(content)


    def message(self):
        (timestamp, source, type_) = RobotMessageHeader._make(struct.unpack(robotMessageHeaderFmt, self.content[:10]))
        i = 10
        messageLength = len(self.content)-10

        return self.messageFactory(type_, self.content[10:])
        
