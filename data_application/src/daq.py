from Automation.BDaq import *
from Automation.BDaq.InstantAiCtrl import InstantAiCtrl
from Automation.BDaq.BDaqApi import AdxEnumToString, BioFailed
from PyQt5.QtCore import QThread
import pandas as pd
import csv
class DataCollectionThread(QThread):
    def __init__(self, device_description, profile_path, channel_count, start_channel):
        super().__init__()
        self.device_description = device_description
        self.profile_path = profile_path
        self.channel_count = channel_count
        self.start_channel = start_channel
        # self.result_data1 = []
        # self.result_data2 = []
        self.result_dict = {"ekg": [], "gsr": []}

    def run(self):
        instance_ai_obj = InstantAiCtrl(self.device_description)
        instance_ai_obj.loadProfile = self.profile_path

        while not self.isInterruptionRequested():
            ret, scaled_data = instance_ai_obj.readDataF64(self.start_channel, self.channel_count)
            if BioFailed(ret):
                break
            for i in range(self.start_channel, self.start_channel + self.channel_count):
                if i == 0:
                    self.result_dict["ekg"].append(scaled_data[i - self.start_channel])
                else:
                    self.result_dict["gsr"].append(abs(scaled_data[i - self.start_channel]))

        instance_ai_obj.dispose()

    # def run(self, folder_path):
    #     instance_ai_obj = InstantAiCtrl(self.device_description)
    #     instance_ai_obj.loadProfile = self.profile_path

    #     with open(os.path.join(folder_path, 'ekg_data.csv', 'a', newline='') as ekg_csvfile:
    #         ekg_csvwriter = csv.writer(ekg_csvfile)

    #         with open(os.path.join(folder_path, 'gsr_data.csv'), 'a', newline='') as gsr_csvfile:
    #             gsr_csvwriter = csv.writer(gsr_csvfile)
                
    #             while not self.isInterruptionRequested():
    #                 ret, scaled_data = instance_ai_obj.readDataF64(self.start_channel, self.channel_count)
    #                 if BioFailed(ret):
    #                     break
    #                 for i in range(self.start_channel, self.start_channel + self.channel_count):
    #                     if i == 0:
    #                         ekg_csvwriter.writerow([scaled_data[i - self.start_channel]])
    #                     else:
    #                         gsr_csvwriter.writerow([abs(scaled_data[i - self.start_channel])])

    #     instance_ai_obj.dispose()

    def stop(self):
        self.threadActive = False
        self.quit()

    def getData(self):
        # names = {"ekg": self.result_data1}
        # names1 = {"gsr": self.result_data2}
        # df = pd.DataFrame(names)
        # df1 = pd.DataFrame(names1)
        result = pd.DataFrame(self.result_dict)
        # return df, df1
        return result