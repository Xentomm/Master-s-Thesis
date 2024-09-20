import mne
import numpy as np
from scipy.fft import fft, fftfreq
import matplotlib.pyplot as plt
import os

raw_rest = mne.io.read_raw_edf('dane/24.07.2024/2024-07-24_10-19-46_MK78/Parts/rest.edf', preload=True) 
raw_bridge = mne.io.read_raw_edf('dane/24.07.2024/2024-07-24_10-19-46_MK78/Parts/bridge.edf', preload=True)
raw_chess = mne.io.read_raw_edf('dane/24.07.2024/2024-07-24_10-19-46_MK78/Parts/chess.edf', preload=True)

fs = raw_rest.info['sfreq']

frequency_bands = {
    'Delta (0.1-3.9 Hz)': (0.1, 3.9), 
    'Theta (4-7.9 Hz)': (4, 7.9),
    'Alpha (8-12.9 Hz)': (8, 12.9), 
    'Beta (13-29.9 Hz)': (13, 29.9),
    'Low Gamma (30-59.9 Hz)': (30, 59.9), 
    'High Gamma (60-100 Hz)': (60, 100)
}

def apply_fft(raw, fs):
    data = raw.get_data()
    fft_result = fft(data, axis=1)
    freqs = fftfreq(data.shape[1], 1/fs)[:data.shape[1]//2]
    power_spectrum = np.abs(fft_result[:, :data.shape[1]//2])**2
    return freqs, power_spectrum

output_dir = 'Wykresy fft'
os.makedirs(output_dir, exist_ok=True)

for band_name, (low_freq, high_freq) in frequency_bands.items():
    raw_rest = raw_rest.crop(tmin = 0, tmax = 61)
    raw_rest_copy = raw_rest.copy()
    raw_rest_copy.filter(l_freq=low_freq, h_freq=high_freq, fir_design='firwin')
    freqs_rest, power_rest = apply_fft(raw_rest_copy, fs)
    avg_power_rest = np.mean(power_rest, axis=0)
    max_power_rest = np.max(avg_power_rest)

    raw_bridge = raw_bridge.crop(tmin = 0, tmax = 61)
    raw_bridge_copy = raw_bridge.copy()
    raw_bridge_copy.filter(l_freq=low_freq, h_freq=high_freq, fir_design='firwin')
    freqs_bridge, power_bridge = apply_fft(raw_bridge_copy, fs)
    avg_power_bridge = np.mean(power_bridge, axis=0)
    max_power_bridge = np.max(avg_power_bridge)

    raw_chess = raw_chess.crop(tmin = 0, tmax = 61)
    raw_chess_copy = raw_chess.copy()
    raw_chess_copy.filter(l_freq=low_freq, h_freq=high_freq, fir_design='firwin')
    freqs_chess, power_chess = apply_fft(raw_chess_copy, fs)
    avg_power_chess = np.mean(power_chess, axis=0)
    max_power_chess = np.max(avg_power_chess)

    max_value = max(max_power_rest, max_power_bridge, max_power_chess)

    plt.figure(figsize=(15, 10))

    plt.subplot(3, 1, 1)
    plt.plot(freqs_rest, avg_power_rest, label=f'{band_name} - Stan spoczynku')
    plt.title(f'Spektrum mocy - Stan spoczynku ({band_name})', fontsize=22)
    plt.xlabel('Częstotliwość [Hz]', fontsize=20)
    plt.ylabel('Średnia moc', fontsize=20)
    plt.tick_params(axis='x', labelsize=18)
    plt.tick_params(axis='y', labelsize=18)
    plt.ylim(0, max_value)
    plt.xlim(low_freq, high_freq)
    plt.legend()
    plt.grid(True)
    
    plt.subplot(3, 1, 2)
    plt.plot(freqs_bridge, avg_power_bridge, label=f'{band_name} - Brydż')
    plt.title(f'Spektrum mocy - Brydż ({band_name})', fontsize=22)
    plt.xlabel('Częstotliwość [Hz]', fontsize=20)
    plt.ylabel('Średnia moc', fontsize=20)
    plt.tick_params(axis='x', labelsize=18)
    plt.tick_params(axis='y', labelsize=18)
    plt.ylim(0, max_value)
    plt.xlim(low_freq, high_freq)
    plt.legend()
    plt.grid(True)
    
    plt.subplot(3, 1, 3)
    plt.plot(freqs_chess, avg_power_chess, label=f'{band_name} - Szachy')
    plt.title(f'Spektrum mocy - Szachy ({band_name})', fontsize=22)
    plt.xlabel('Częstotliwość [Hz]', fontsize=20)
    plt.ylabel('Średnia moc', fontsize=20)
    plt.tick_params(axis='x', labelsize=18)
    plt.tick_params(axis='y', labelsize=18)
    plt.ylim(0, max_value)
    plt.xlim(low_freq, high_freq)
    plt.legend()
    plt.grid(True)
    
    plt.tight_layout()

    plot_filename = os.path.join(output_dir, f'spectrum_{band_name.replace(" ", "_")}.png')
    plt.savefig(plot_filename)

    plt.close()

print(f'Plots saved in directory: {output_dir}')