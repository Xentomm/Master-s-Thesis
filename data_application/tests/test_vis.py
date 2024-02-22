import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

NUM_OF_FRAMES = 5

input_dir = input("Dir: ")

dir_path = f"data_application/collected/{input_dir}/"

df = pd.read_csv(dir_path + "output_daq.csv")

npz_data = np.load(dir_path + "data.npz")
print("Keys in the npz file:")
for key in npz_data.keys():
    print(key)
frames_camera = npz_data['cameraData']
frames_lepton = npz_data['leptonData']

# Plotting CSV data
fig_csv, axs_csv = plt.subplots(2)
axs_csv[0].plot(df["ekg"][:10000])
axs_csv[0].set_title("EKG")
axs_csv[1].plot(df["gsr"][:10000])
axs_csv[1].set_title("GSR")

# Plotting data from NPZ file
fig_npz, axs_npz = plt.subplots(2, NUM_OF_FRAMES, figsize=(15, 6))
for i in range(NUM_OF_FRAMES):
    axs_npz[0, i].imshow(frames_camera[i])
    axs_npz[0, i].set_title(f"Camera Frame {i+1}")
    axs_npz[1, i].imshow(frames_lepton[i])
    axs_npz[1, i].set_title(f"Lepton Frame {i+1}")

plt.show()
