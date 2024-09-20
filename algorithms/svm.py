import mne
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.decomposition import PCA
import plotly.graph_objs as go
import plotly.io as pio
import matplotlib.pyplot as plt

raw_rest = mne.io.read_raw_edf('dane/22.05.2024/MM/Parts/rest.edf', preload=True)
raw_bridge = mne.io.read_raw_edf('dane/22.05.2024/MM/Parts/bridge.edf', preload=True)
raw_chess = mne.io.read_raw_edf('dane/22.05.2024/MM/Parts/chess.edf', preload=True)

raw_rest = raw_rest.crop(tmin=10, tmax=11)
raw_bridge = raw_bridge.crop(tmin=10, tmax=11)
raw_chess = raw_chess.crop(tmin=10, tmax=11)

selected_channels = ['Fz', 'Cz', 'Pz', 'Oz']
raw_rest.pick(selected_channels)
raw_bridge.pick(selected_channels)
raw_chess.pick(selected_channels)

data_rest = raw_rest.get_data().T
data_bridge = raw_bridge.get_data().T
data_chess = raw_chess.get_data().T

labels_rest = np.zeros(data_rest.shape[0])
labels_bridge = np.ones(data_bridge.shape[0])
labels_chess = np.full(data_chess.shape[0], 2)

data = np.vstack([data_rest, data_bridge, data_chess])
labels = np.concatenate([labels_rest, labels_bridge, labels_chess])

X_train, X_test, y_train, y_test = train_test_split(data, labels, test_size=0.3, random_state=42)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

pca = PCA(n_components=3)
X_train_pca = pca.fit_transform(X_train_scaled)
X_test_pca = pca.transform(X_test_scaled)

svm_model = SVC(kernel='rbf', C=1.0, random_state=42, verbose=True)
svm_model.fit(X_train_pca, y_train)

y_pred = svm_model.predict(X_test_pca)

conf_matrix = confusion_matrix(y_test, y_pred)
print("Macierz pomyłek:")
print(conf_matrix)

class_report = classification_report(y_test, y_pred, target_names=['Spoczynkowy', 'Brydż', 'Szachy'])
print("Raport klasyfikacji:")
print(class_report)

plt.figure(figsize=(8, 6))
plt.imshow(conf_matrix, interpolation='nearest', cmap=plt.cm.Blues)
plt.title("Macierz pomyłek")
plt.colorbar()
tick_marks = np.arange(3)
plt.xticks(tick_marks, ['Spoczynkowy', 'Brydż', 'Szachy'])
plt.yticks(tick_marks, ['Spoczynkowy', 'Brydż', 'Szachy'])
plt.ylabel('Etykieta rzeczywista')
plt.xlabel('Przewidywana etykieta')
plt.show()

trace_rest = go.Scatter3d(
    x=X_train_pca[y_train == 0, 0],
    y=X_train_pca[y_train == 0, 1],
    z=X_train_pca[y_train == 0, 2],
    mode='markers',
    name='Spoczynkowy',
    marker=dict(
        size=5,
        color='blue',
        opacity=0.8
    )
)

trace_bridge = go.Scatter3d(
    x=X_train_pca[y_train == 1, 0],
    y=X_train_pca[y_train == 1, 1],
    z=X_train_pca[y_train == 1, 2],
    mode='markers',
    name='Brydż',
    marker=dict(
        size=5,
        color='orange',
        opacity=0.8
    )
)

trace_chess = go.Scatter3d(
    x=X_train_pca[y_train == 2, 0],
    y=X_train_pca[y_train == 2, 1],
    z=X_train_pca[y_train == 2, 2],
    mode='markers',
    name='Szachy',
    marker=dict(
        size=5,
        color='green',
        opacity=0.8
    )
)

layout = go.Layout(
    scene=dict(
        xaxis=dict(
            title=dict(
                text='Składnik główny 1',
                font=dict(size=24)
            ),
            tickfont=dict(size=16)
        ),
        yaxis=dict(
            title=dict(
                text='Składnik główny 2',
                font=dict(size=24)
            ),
            tickfont=dict(size=16)
        ),
        zaxis=dict(
            title=dict(
                text='Składnik główny 3',
                font=dict(size=24)
            ),
            tickfont=dict(size=16)
        )
    ),
    title=dict(
        text='RBF SVM - Wizualizacja w 3D z legendą',
        font=dict(size=20)
    ),
    legend=dict(
        font=dict(size=24)
    )
)
fig = go.Figure(data=[trace_rest, trace_bridge, trace_chess], layout=layout)
pio.write_html(fig, file='wykres_svm_3d_z_legenda.html', auto_open=True)
