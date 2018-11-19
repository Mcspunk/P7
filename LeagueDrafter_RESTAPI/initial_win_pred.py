# TensorFlow and tf.keras
import tensorflow as tf
from tensorflow import keras

# Helper libraries
import numpy as np
import os
from db_connection import dbConnector as db

db_conn = db("sw703db.cgukp5oibqte.eu-central-1.rds.amazonaws.com", "SW703DB", "sw703", "sw703aoe")

dataset, wins, champions = db_conn.retrieveDataset()
champions = sorted(champions)

ta = int(len(dataset)*0.7)
te = int(ta + len(dataset)*0.2)

# --- Find data
train_data = np.array(dataset[:ta])
test_data = np.array(dataset[ta:te])
validate_data = np.array(dataset[te:])
train_labels = np.array(wins[:ta])
test_labels = np.array(wins[ta:te])
validate_labels = np.array(wins[te:])

# --- NN
def trainModel():
    model = keras.Sequential([
        keras.layers.Dense(150, input_shape=(10,8)),
        keras.layers.Dense(300, activation=tf.nn.relu, kernel_regularizer=keras.regularizers.l1(0.1)),
        keras.layers.Dense(2, activation=tf.nn.softmax)
        ])

    model.compile(optimizer=keras.optimizers.Adam(lr=0.001, decay=0.1),
                 loss='mean_squared_error',
                  metrics=['accuracy'],)

    model.fit(train_data, train_labels, epochs=5, batch_size=32)
    model.save('savedNetwork.h5')
    test_loss, test_acc = model.evaluate(test_data, test_labels)

def loadModel():
    model = keras.models.load_model('savedNetwork.h5')
    return model

def predictTeamComp(input):
    #trainModel()
    pred = np.reshape(createTempComp(input), (1,10,8))
    return trained_model.predict(pred)[0][0][0]


def createTempComp(input):
    resultTC = []
    for i in range(0,5):
        k = []
        k.append(1)
        k.extend(champions[input[i]])
        resultTC.append(k)
    for i in range(5,10):
        k = []
        k.append(-1)
        k.extend(champions[input[i]])
        resultTC.append(k)
    return np.array(resultTC)


trained_model = loadModel()
