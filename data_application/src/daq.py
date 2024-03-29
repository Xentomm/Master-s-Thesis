from Automation.BDaq import *
from Automation.BDaq.InstantAiCtrl import InstantAiCtrl
from Automation.BDaq.BDaqApi import AdxEnumToString, BioFailed
from PyQt5.QtCore import QThread
import pandas as pd
import csv
import os

class DataCollectionThread(QThread):
    def __init__(self, device_description, profile_path, channel_count, start_channel, folder_path):
        super().__init__()
        self.device_description = device_description
        self.profile_path = profile_path
        self.channel_count = channel_count
        self.start_channel = start_channel
        self.folder_path = folder_path

    def run(self):
        instance_ai_obj = InstantAiCtrl(self.device_description)
        instance_ai_obj.loadProfile = self.profile_path

        with open(os.path.join(self.folder_path, 'ekg_data.csv'), 'a', newline='') as ekg_csvfile:
            ekg_csvwriter = csv.writer(ekg_csvfile)

            with open(os.path.join(self.folder_path, 'gsr_data.csv'), 'a', newline='') as gsr_csvfile:
                gsr_csvwriter = csv.writer(gsr_csvfile)
                
                while not self.isInterruptionRequested():
                    ret, scaled_data = instance_ai_obj.readDataF64(self.start_channel, self.channel_count)
                    if BioFailed(ret):
                        break
                    for i in range(self.start_channel, self.start_channel + self.channel_count):
                        if i == 0:
                            ekg_csvwriter.writerow([scaled_data[i - self.start_channel]])
                        else:
                            gsr_csvwriter.writerow([abs(scaled_data[i - self.start_channel])])

        instance_ai_obj.dispose()

    def stop(self):
        self.threadActive = False
        self.quit()