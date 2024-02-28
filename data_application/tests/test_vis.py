import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

'''
The following script reads data from CSV and NPZ files and plots the EKG and GSR data from the CSV file,
along with camera and Lepton frames from the NPZ file.
'''

def plot_data_from_files(input_dir, num_of_frames=5, sample_size=10000):
    dir_path = f"data_application/collected/{input_dir}/"
    
    df = pd.read_csv(dir_path + "output_daq.csv")
    npz_data = np.load(dir_path + "data.npz")

    frames_camera = npz_data['cameraData']
    frames_lepton = npz_data['leptonData']

    fig_csv, axs_csv = plt.subplots(2)
    axs_csv[0].plot(df["ekg"][:sample_size])
    axs_csv[0].set_title("EKG")
    axs_csv[1].plot(df["gsr"][:sample_size])
    axs_csv[1].set_title("GSR")

    fig_npz, axs_npz = plt.subplots(2, num_of_frames, figsize=(15, 6))
    for i in range(num_of_frames):
        axs_npz[0, i].imshow(frames_camera[i])
        axs_npz[0, i].set_title(f"Camera Frame {i+1}")
        axs_npz[1, i].imshow(frames_lepton[i])
        axs_npz[1, i].set_title(f"Lepton Frame {i+1}")

    plt.show()

# print("Keys in the NPZ file:")
# for key in npz_data.keys():
#     print(key)
    
input_dir = input("Dir: ")
plot_data_from_files(input_dir)