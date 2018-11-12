# TensorFlow and tf.keras
import tensorflow as tf
from tensorflow import keras

# Helper libraries
import numpy as np
import math as m
import psycopg2 as psy
from db_connection import dbConnector as db
from sklearn.model_selection import GridSearchCV
from keras.wrappers.scikit_learn import KerasClassifier

db_conn = db("sw703db.cgukp5oibqte.eu-central-1.rds.amazonaws.com", "SW703DB", "sw703", "sw703aoe")

dataset, wins = db_conn.retrieveDataset()

ta = int(len(dataset)*0.7)
te = int(ta + len(dataset)*0.2)

# --- Find data
train_data = np.array(dataset[:ta])#, dtype=list)
test_data = np.array(dataset[ta:te])#, dtype=list)
validate_data = np.array(dataset[te:])
train_labels = np.array(wins[:ta])
test_labels = np.array(wins[ta:te])
validate_labels = np.array(wins[te:])


batch_list = [16, 32]
epochs_list= [1, 2]
results = []

# --- NN
for i in batch_list:
    for k in epochs_list:
        model = keras.Sequential([
            keras.layers.Dense(150, input_shape=(10, 8)),
            keras.layers.Dense(300, activation=tf.nn.relu, kernel_regularizer=keras.regularizers.l1(0.1)),
            keras.layers.Dense(2, activation=tf.nn.softmax)
            ])

        model.compile(optimizer=keras.optimizers.Adam(lr=0.001, decay=0.1),
                      loss='mean_squared_error',
                      metrics=['accuracy'])

        model.fit(train_data, train_labels, epochs=k, batch_size=i)

        test_loss, test_acc = model.evaluate(test_data, test_labels)

        results.append([i, k, test_acc])

        #print('Test acc: ', test_acc)

print(results)
