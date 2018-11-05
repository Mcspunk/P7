# TensorFlow and tf.keras
import tensorflow as tf
from tensorflow import keras

# Helper libraries
import numpy as np
import math as m
import matplotlib.pyplot as plt
import psycopg2 as psy
from db_connection import dbConnector as db

db_conn = db("sw703db.cgukp5oibqte.eu-central-1.rds.amazonaws.com", "SW703DB", "sw703", "sw703aoe")

db_conn.retrieveWins()


dataset, wins = db_conn.retrieveDataset()

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
class_name = ['Win', 'Lose']

model = keras.Sequential([
    keras.layers.Dense(150, input_dim=141),
    keras.layers.Dense(300, activation=tf.nn.relu),
    keras.layers.Dense(2, activation=tf.nn.softmax)
    ])

model.compile(optimizer=tf.train.AdamOptimizer(),
              loss='binary_crossentropy',
              metrics=['accuracy'])

model.fit(train_data, train_labels, epochs=5)

test_loss, test_acc = model.evaluate(test_data, test_labels)

print('Test acc: ', test_acc)

predictions = model.predict(validate_data)
print(predictions[1])
print(predictions[3])
print(predictions[2])

