# """
# /*******************************************************************************
# Copyright (c) 1983-2021 Advantech Co., Ltd.
# ********************************************************************************
# THIS IS AN UNPUBLISHED WORK CONTAINING CONFIDENTIAL AND PROPRIETARY INFORMATION
# WHICH IS THE PROPERTY OF ADVANTECH CORP., ANY DISCLOSURE, USE, OR REPRODUCTION,
# WITHOUT WRITTEN AUTHORIZATION FROM ADVANTECH CORP., IS STRICTLY PROHIBITED.

# ================================================================================
# REVISION HISTORY
# --------------------------------------------------------------------------------
# $Log:  $
# --------------------------------------------------------------------------------
# $NoKeywords:  $
# */
# /******************************************************************************
# *
# * Windows Example:
# *    InstantAI.py
# *
# * Example Category:
# *    AI
# *
# * Description:
# *    This example demonstrates how to use Instant AI function.
# *
# * Instructions for Running:
# *    1. Set the 'deviceDescription' for opening the device.
# *    2. Set the 'profilePath' to save the profile path of being initialized device.
# *    3. Set the 'startChannel' as the first channel for scan analog samples
# *    4. Set the 'channelCount' to decide how many sequential channels to scan analog samples.
# *
# * I/O Connections Overview:
# *    Please refer to your hardware reference manual.
# *
# ******************************************************************************/
# """
# import sys
# sys.path.append('..')
# from CommonUtils import kbhit
# import time

# from Automation.BDaq import *
# from Automation.BDaq.InstantAiCtrl import InstantAiCtrl
# from Automation.BDaq.BDaqApi import AdxEnumToString, BioFailed

# import pandas as pd
# import keyboard

# #deviceDescription = "DemoDevice,BID#0"
# deviceDescription = "USB-4716,BID#0"
# profilePath = u"../../profile/DemoDevice.xml"

# channelCount = 2
# startChannel = 0

# result_data1 = []
# result_data2 = []

# def AdvInstantAI():
#     ret = ErrorCode.Success

#     # Step 1: Create a 'instantAiCtrl' for InstantAI function
#     # Select a device by device number or device description and specify the access mode.
#     # In this example we use ModeWrite mode so that we can fully control the device, including configuring, sampling, etc.
#     instanceAiObj = InstantAiCtrl(deviceDescription)
#     for _ in range(1):
#         instanceAiObj.loadProfile = profilePath   # Loads a profile to initialize the device

#         # Step 2: Read samples and do post-process, we show data here.
#         # print("Acquisition is in progress, any key to quit!")
#         while not keyboard.is_pressed('F2'):
#             # print("Jestem")
#             ret, scaledData = instanceAiObj.readDataF64(startChannel, channelCount)
#             if BioFailed(ret):
#                 break
#             for i in range(startChannel, startChannel + channelCount):
#                 # print("Channel %d data: %10.6f" % (i, scaledData[i-startChannel]))
#                 if i == 0:
#                     result_data1.append(scaledData[i-startChannel])
#                 else:
#                     result_data2.append(abs(scaledData[i-startChannel]))
#             # time.sleep(1)
#     names = ({"ekg": result_data1, "gsr": result_data2})
#     # print(names)
#     df = pd.DataFrame(names)
#     df.to_csv("data_application/collected/out.csv")
#     instanceAiObj.dispose()

#     if BioFailed(ret):
#         enumStr = AdxEnumToString("ErrorCode", ret.value, 256)
#         print("Some error occurred. And the last error code is %#x. [%s]" % (ret.value, enumStr))
#     return 0


# if __name__ == '__main__':
#     AdvInstantAI()

from Automation.BDaq import *
from Automation.BDaq.InstantAiCtrl import InstantAiCtrl
from Automation.BDaq.BDaqApi import AdxEnumToString, BioFailed
from PyQt5.QtCore import QThread
import pandas as pd
class DataCollectionThread(QThread):
    def __init__(self, device_description, profile_path, channel_count, start_channel):
        super().__init__()
        self.device_description = device_description
        self.profile_path = profile_path
        self.channel_count = channel_count
        self.start_channel = start_channel
        self.result_data1 = []
        self.result_data2 = []

    def run(self):
        instance_ai_obj = InstantAiCtrl(self.device_description)
        instance_ai_obj.loadProfile = self.profile_path # instance_ai_obj.loadProfile(self.profile_path)

        while not self.isInterruptionRequested():
            ret, scaled_data = instance_ai_obj.readDataF64(self.start_channel, self.channel_count)
            if BioFailed(ret):
                break
            for i in range(self.start_channel, self.start_channel + self.channel_count):
                if i == 0:
                    self.result_data1.append(scaled_data[i - self.start_channel])
                else:
                    self.result_data2.append(abs(scaled_data[i - self.start_channel]))

        instance_ai_obj.dispose()

    def stop(self):
        self.threadActive = False
        self.quit()

    def getData(self):
        names = {"ekg": self.result_data1, "gsr": self.result_data2}
        df = pd.DataFrame(names)
        return df