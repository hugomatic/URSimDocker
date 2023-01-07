#!/usr/bin/env python
# encoding: utf-8

import socket
import struct
from collections import namedtuple
from pprint import pprint
import datetime
from sqlitedict import SqliteDict
import json
from time import sleep

from PrimaryInterface.RobotStatePackage import RobotStatePackage
from PrimaryInterface.RobotMessage import RobotMessage
from PrimaryInterface.ProgramState import ProgramState

""" 
#UR Controller Client Interface Datastream Reader
# For software version 3.x
#
# Datastream info found here: https://s3-eu-west-1.amazonaws.com/ur-support-site/16496/Client_Interface.xlsx
# Struct library used to extract data, info found here: https://docs.python.org/2/library/struct.html

# Based on code sample found at https://forum.universal-robots.com/t/how-to-process-package-from-robot-controller/390/4
"""

packageHeaderFmt = '!iB'

def packageFactory(type_, content):
    if type_ == 16:
        return RobotStatePackage(content)
    elif type_ == 20:
        return RobotMessage(content)
    elif type_ == 25:
        return ProgramState(content)
    else:
        return None

def main():

    #Establish connection to controller
    HOST = '127.0.0.1'
    PORT = 30001

    s = None

    while True:
        while s is None:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((HOST, PORT))
                print s.fileno(), s.getpeername(), s.getsockname()
                print 'Connection established.'
            except socket.error:
                print 'Can not open connection...',
                sleep(2)
                s = None
                print 'retrying'

        data = 'data'

        while data:
            try:
                data = s.recv(4096*4)

                if data:
                    #initialise i to keep track of position in packet
                    i = 0
                    while i+5 < len(data):
                        #extract packet length, timestamp and packet type from start of packet and print to screen
                        (length, type_) =  struct.unpack(packageHeaderFmt, data[i:i+5])
                        assert i + length <= len(data), '{}+{}<={}'.format(i, length, len(data))

                        package = packageFactory(type_, data[i+5:i+length])

                        #if isinstance(package, RobotStatePackage):
                        #    for subpackage in package.subpackages():
                        #        if subpackage:
                        #            robotstateDB.update(subpackage._asdict())
                        #
                        #if isinstance(package, RobotMessage):
                        #    print package.message()

                        if isinstance(package, ProgramState):
                            if package.programRestarted:
                                for key in variablesDB:
                                    del variablesDB[key]
                            if package.updatedVariables:
                                variablesDB.update(package.updatedVariables)
                                #pprint(package.updatedVariables)

                        i+=length

                    # Save values to database
                    variablesDB.commit()
                    robotstateDB.commit()
                else:
                    print 'No data!'
                    s.close()
                    s = None
            except socket.error:
                print 'Exception while receiving data'
                s.close()
                s = None
                data = None

if __name__ == '__main__':
    with SqliteDict('/tmp/ur_variables.db', autocommit=False, encode=json.dumps, decode=json.loads) as variablesDB:
        with SqliteDict('/tmp/ur_robotstate.db', autocommit=False) as robotstateDB:
            print "Starting main"
            main()
