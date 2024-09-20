import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.decomposition import PCA
import plotly.graph_objs as go
import plotly.io as pio
import matplotlib.pyplot as plt
import pandas as pd

data_rest = pd.read_csv('ekg/ekg_data_rest.csv', header=None, nrows=10000)
data_bridge = pd.read_csv('ekg/ekg_data_bridge.csv', header=None, nrows=10000)
data_chess = pd.read_csv('ekg/ekg_data_chess.csv', header=None, nrows=10000)

data_rest = data_rest.values
data_bridge = data_bridge.values
data_chess = data_chess.values

labels_rest = np.zeros(data_rest.shape[0])
labels_bridge = np.ones(data_bridge.shape[0])
labels_chess = np.full(data_chess.shape[0], 2)

data = np.vstack([data_rest, data_bridge, data_chess])
labels = np.concatenate([labels_rest, labels_bridge, labels_chess])

X_train, X_test, y_train, y_test = train_test_split(data, labels, test_size=0.3, random_state=42)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

svm_model = SVC(kernel='rbf', C=1.0, random_state=42, verbose=True)
svm_model.fit(X_train_scaled, y_train)

y_pred = svm_model.predict(X_test_scaled)

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