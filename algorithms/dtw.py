import mne
from fastdtw import fastdtw
from scipy.spatial.distance import euclidean
import matplotlib.pyplot as plt

stan_spoczynkowy = mne.io.read_raw_edf('dane/24.07.2024/2024-07-24_10-19-46_MK78/Parts/rest.edf', preload=True)
stan_brydz = mne.io.read_raw_edf('dane/24.07.2024/2024-07-24_10-19-46_MK78/Parts/bridge.edf', preload=True)
stan_szachy = mne.io.read_raw_edf('dane/24.07.2024/2024-07-24_10-19-46_MK78/Parts/chess.edf', preload=True)

stan_spoczynkowy = stan_spoczynkowy.crop(tmin=0, tmax=1)
stan_brydz = stan_brydz.crop(tmin=0, tmax=1)
stan_szachy = stan_szachy.crop(tmin=0, tmax=1)

wybrane_kanaly = ['Fz', 'Cz', 'Pz', 'Oz']

fig, axs = plt.subplots(2, 2, figsize=(14, 10))

for i, kanal in enumerate(wybrane_kanaly):
    eeg_spoczynkowy = stan_spoczynkowy.get_data(picks=kanal).squeeze()
    eeg_brydz = stan_brydz.get_data(picks=kanal).squeeze()
    eeg_szachy = stan_szachy.get_data(picks=kanal).squeeze()

    odleglosc_spoczynkowy_vs_brydz, _ = fastdtw(eeg_spoczynkowy, eeg_brydz, dist=2)
    odleglosc_spoczynkowy_vs_szachy, _ = fastdtw(eeg_spoczynkowy, eeg_szachy, dist=2)
    odleglosc_brydz_vs_szachy, _ = fastdtw(eeg_brydz, eeg_szachy, dist=2)

    print(f"Odległość DTW między stanem spoczynkowym a brydżem dla kanału {kanal}: {odleglosc_spoczynkowy_vs_brydz}")
    print(f"Odległość DTW między stanem spoczynkowym a szachami dla kanału {kanal}: {odleglosc_spoczynkowy_vs_szachy}")
    print(f"Odległość DTW między brydżem a szachami dla kanału {kanal}: {odleglosc_brydz_vs_szachy}")

    ax = axs[i // 2, i % 2]

    ax.plot(eeg_spoczynkowy, label='Stan spoczynkowy')
    ax.plot(eeg_brydz, label='Gra w brydża')
    ax.plot(eeg_szachy, label='Gra w szachy')
    ax.set_title(f'Kanał {kanal}', fontsize=20)
    ax.set_xlabel('Czas [s]', fontsize=20)
    ax.set_ylabel('Amplituda', fontsize=20)
    ax.tick_params(axis='x', labelsize=18)
    ax.tick_params(axis='y', labelsize=18)
    ax.legend()

plt.tight_layout()
plt.show()
