import mne
import numpy as np
from hmmlearn import hmm
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler

rest_path = 'C:/Users/Adrian/Desktop/Magisterka/Badania/16.07.2024/2024-07-16_10-45-12_JJ75/Parts/rest.edf'
bridge_path = 'C:/Users/Adrian/Desktop/Magisterka/Badania/16.07.2024/2024-07-16_10-45-12_JJ75/Parts/bridge.edf'
chess_path = 'C:/Users/Adrian/Desktop/Magisterka/Badania/16.07.2024/2024-07-16_10-45-12_JJ75/Parts/chess.edf'

raw_rest = mne.io.read_raw_edf(rest_path, preload=True)
raw_bridge = mne.io.read_raw_edf(bridge_path, preload=True)
raw_chess = mne.io.read_raw_edf(chess_path, preload=True)


data_rest, times_rest = raw_rest.get_data(return_times=True)
data_bridge, times_bridge = raw_bridge.get_data(return_times=True)
data_chess, times_chess = raw_chess.get_data(return_times=True)


features_rest = np.var(data_rest, axis=1)
features_bridge = np.var(data_bridge, axis=1)
features_chess = np.var(data_chess, axis=1)


scaler = StandardScaler()
features_rest = scaler.fit_transform(features_rest.reshape(-1, 1))
features_bridge = scaler.fit_transform(features_bridge.reshape(-1, 1))
features_chess = scaler.fit_transform(features_chess.reshape(-1, 1))


n_states = 3

model_rest = hmm.GaussianHMM(n_components=n_states, covariance_type="spherical", n_iter=1000, random_state=42, verbose=True, tol=1e-4)
model_bridge = hmm.GaussianHMM(n_components=n_states, covariance_type="spherical", n_iter=1000, random_state=42, verbose=True, tol=1e-4)
model_chess = hmm.GaussianHMM(n_components=n_states, covariance_type="spherical", n_iter=1000, random_state=42, verbose=True, tol=1e-4)


model_rest.fit(features_rest)
model_bridge.fit(features_bridge)
model_chess.fit(features_chess)

model_rest.transmat_ += 1e-6
model_rest.transmat_ /= model_rest.transmat_.sum(axis=1, keepdims=True)

model_bridge.transmat_ += 1e-6
model_bridge.transmat_ /= model_bridge.transmat_.sum(axis=1, keepdims=True)

model_chess.transmat_ += 1e-6
model_chess.transmat_ /= model_chess.transmat_.sum(axis=1, keepdims=True)

hidden_states_rest = model_rest.predict(features_rest)
hidden_states_bridge = model_bridge.predict(features_bridge)
hidden_states_chess = model_chess.predict(features_chess)

print("Hidden States rest:", hidden_states_rest)
print("Hidden States bridge:", hidden_states_bridge)
print("Hidden States chess:", hidden_states_chess)


fig, axes = plt.subplots(1, 3, figsize=(18, 6)) 

axes[0].imshow(model_rest.transmat_, cmap='viridis', aspect='auto')
axes[0].set_title('HMM Transition Matrix (Rest)')
axes[0].set_xlabel('State')
axes[0].set_ylabel('State')
fig.colorbar(axes[0].images[0], ax=axes[0], orientation='vertical', label='Transition Probability')

axes[1].imshow(model_bridge.transmat_, cmap='viridis', aspect='auto')
axes[1].set_title('HMM Transition Matrix (Bridge)')
axes[1].set_xlabel('State')
axes[1].set_ylabel('State')
fig.colorbar(axes[1].images[0], ax=axes[1], orientation='vertical', label='Transition Probability')

axes[2].imshow(model_chess.transmat_, cmap='viridis', aspect='auto')
axes[2].set_title('HMM Transition Matrix (Chess)')
axes[2].set_xlabel('State')
axes[2].set_ylabel('State')
fig.colorbar(axes[2].images[0], ax=axes[2], orientation='vertical', label='Transition Probability')

plt.tight_layout()
plt.show()