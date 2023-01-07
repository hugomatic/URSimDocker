#!/usr/bin/env python

from collections import namedtuple
import struct

# Author: Daniel Ozminkowski

# ROBOT_STATE = 16

robotModeFmt = '!Q???????BBdddB'
jointDataFmt = '!dddffffBdddffffBdddffffBdddffffBdddffffBdddffffB'
toolDataFmt = '!bbddfBffB'
masterboardDataFmt_len85 = '!iibbddbbddffffBBbiiffIBB'
masterboardDataFmt_len74 = '!iibbddbbddffffBBbIBB'
cartesianInfoFmt = '!dddddddddddd'
configurationDataFmt = '!'+ 'd'*53 + 'i'*4
forceModeDataFmt = '!'+'d'*7
additionalInfoFmt = '!???'

RobotMode = namedtuple("RobotMode",
                       "timestamp "
                       "physicalRobotConnected "
                       "realRobotEnabled "
                       "robotPowerOn "
                       "emergencyStopped "
                       "protectiveStopped "
                       "programRunning "
                       "programPaused "
                       "robotMode "
                       "controlMode "
                       "targetSpeedFraction "
                       "speedScaling "
                       "targetSpeedFractionLimit "
                       "reserve_robot_mode"
                       )

JointData = namedtuple("JointData",
                       "q1_actual q1_target q1d_actual i1 v1 t1 reserve1 jointMode1 "
                       "q2_actual q2_target q2d_actual i2 v2 t2 reserve2 jointMode2 "
                       "q3_actual q3_target q3d_actual i3 v3 t3 reserve3 jointMode3 "
                       "q4_actual q4_target q4d_actual i4 v4 t4 reserve4 jointMode4 "
                       "q5_actual q5_target q5d_actual i5 v5 t5 reserve5 jointMode5 "
                       "q6_actual q6_target q6d_actual i6 v6 t6 reserve6 jointMode6"
                       )

ToolData = namedtuple("ToolData",
                      "analogInputRange2 "
                      "analogInputRange3 "
                      "analogInput2 "
                      "analogInput3 "
                      "toolVoltage48V "
                      "toolOutputVoltage "
                      "toolCurrent "
                      "toolTemperature "
                      "toolMode"
                      )

MasterBoardData_withEuromap67 = namedtuple("MasterBoardData_withEuromap67",
                             "digitalInputBits "
                             "digitalOutputBits "
                             "analogInputRange0 "
                             "analogInputRange1 "
                             "analogInput0 "
                             "analogInput1 "
                             "analogOutputDomain0 "
                             "analogOutputDomain1 "
                             "analogOutput0 "
                             "analogOutput1 "
                             "masterboardTemperature "
                             "robotVoltage48V "
                             "robotCurrent "
                             "masterIOCurrent "
                             "safetyMode "
                             "inReducedMode "
                             "euromap67Installed "
                             "euromapInputBits "
                             "euromapOutputBits "
                             "euromapVoltage "
                             "euromapCurrent "
                             "reserve_masterboard_data "
                             "operationModeSelectorInput "
                             "threePositionEnablingDeviceInput"
                             )

MasterBoardData_withoutEuromap67 = namedtuple("MasterBoardData_withoutEuromap67",
                             "digitalInputBits "
                             "digitalOutputBits "
                             "analogInputRange0 "
                             "analogInputRange1 "
                             "analogInput0 "
                             "analogInput1 "
                             "analogOutputDomain0 "
                             "analogOutputDomain1 "
                             "analogOutput0 "
                             "analogOutput1 "
                             "masterboardTemperature "
                             "robotVoltage48V "
                             "robotCurrent "
                             "masterIOCurrent "
                             "safetyMode "
                             "inReducedMode "
                             "euromap67Installed "
                             "reserve_masterboard_data "
                             "operationModeSelectorInput "
                             "threePositionEnablingDeviceInput"
                             )


CartesianInfo = namedtuple("CartesianInfo",
                           "toolX "
                           "toolY "
                           "toolZ "
                           "toolRx "
                           "toolRy "
                           "toolRz "
                           "tcpOffsetX "
                           "tcpOffsetY "
                           "tcpOffsetZ "
                           "tcpOffsetRX "
                           "tcpOffsetRY "
                           "tcpOffsetRZ"
                           )

ConfigurationData = namedtuple("ConfigurationData",
                               "Joint1Min Joint1Max "
                               "Joint2Min Joint2Max "
                               "Joint3Min Joint3Max "
                               "Joint4Min Joint4Max "
                               "Joint5Min Joint5Max "
                               "Joint6Min Joint6Max "
                               "Joint1MaxVel Joint1MaxAcc "
                               "Joint2MaxVel Joint2MaxAcc "
                               "Joint3MaxVel Joint3MaxAcc "
                               "Joint4MaxVel Joint4MaxAcc "
                               "Joint5MaxVel Joint5MaxAcc "
                               "Joint6MaxVel Joint6MaxAcc "
                               "VJointDefault "
                               "AJointDefault "
                               "VToolDefault "
                               "AToolDefault "
                               "EqRadius "
                               "DHa1 DHa2 DHa3 DHa4 DHa5 DHa6 "
                               "DHd1 DHd2 DHd3 DHd4 DHd5 DHd6 "
                               "DHalpha1 DHalpha2 DHalpha3 DHalpha4 DHalpha5 DHalpha6 "
                               "DHtheta1 DHtheta2 DHtheta3 DHtheta4 DHtheta5 DHtheta6 "
                               "masterBoardVersion "
                               "controllerBoxType "
                               "robotType "
                               "robotSubType"
                               )

ForceModeData = namedtuple("ForceModeData",
                           "x y z rx ry rz robotDexterity"
                           )

AdditionalInfo = namedtuple("AdditionalInfo",
                            "FreedriveButtonPressed "
                            "FreedriveButtonEnabled "
                            "ioEnabledFreedrive"
                            )
class RobotStatePackage:

    def __init__(self, content):
        self.content = content

    def subpackages(self):
        i = 0

        while i+5 < len(self.content):
            #extract length and type of message
            (length, type_) = struct.unpack('!iB', self.content[i:i+5])
            content = self.content[i+5:i+length]
            yield self.subpackageFactory(type_, content)
            i += length


    def subpackageFactory(self, type_, content):
        i = 0

        if type_ == 0:
            return RobotMode._make(struct.unpack(robotModeFmt, content))
            pass
            
        elif type_ == 1:
            return JointData._make(struct.unpack(jointDataFmt, content))
            pass
            
        elif type_ == 2:
            return ToolData._make(struct.unpack(toolDataFmt, content))
            pass
            
        elif type_ == 3:
            if len(content) == 74-5:
                return MasterBoardData_withoutEuromap67._make(struct.unpack(masterboardDataFmt_len74, content))
                pass
            else:
                return MasterBoardData_withEuromap67._make(struct.unpack(masterboardDataFmt_len85, content))
                pass
            
        elif type_ == 4:
            return CartesianInfo._make(struct.unpack(cartesianInfoFmt, content))
            pass
            
        elif type_ == 5:
            # Kinematics info specific to robot
            return None
            pass
        elif type_ == 6:
            return ConfigurationData._make(struct.unpack(configurationDataFmt, content))
            pass
        elif type_ == 7:
            return ForceModeData._make(struct.unpack(forceModeDataFmt, content))
            pass
        elif type_ == 8:
            return AdditionalInfo._make(struct.unpack(additionalInfoFmt, content))
            pass
        elif type_ == 9:
            # Calibration data used by UR internally
            return None
            pass
        elif type_ == 10:
            # Safety data undocumented
            return None
            pass
        elif type_ == 11:
            # Undocumented package that comes when Polyscope uses Simulated Robot
            return None
            pass
        else:
            print 'Unknown subpackage in Robot Status.'
            print "Subpackage position/type/length:", i, '/', type_, '/', len(content)
            return None
