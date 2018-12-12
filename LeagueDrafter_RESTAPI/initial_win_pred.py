# TensorFlow and tf.keras
import tensorflow as tf
from tensorflow import keras
import os
# Helper libraries
import numpy as np
import os

#db_conn = db("sw703db.cgukp5oibqte.eu-central-1.rds.amazonaws.com", "SW703DB", "sw703", "sw703aoe")
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
'''
dataset, wins, champions = db_conn.retrieveDataset()
champions = sorted(champions)

# --- NN
#def trainModel():
#    model = keras.Sequential([
#        keras.layers.Dense(150, input_shape=(10,8)),
#        keras.layers.Dense(300, activation=tf.nn.relu, kernel_regularizer=keras.regularizers.l1(0.1)),
#        keras.layers.Dense(2, activation=tf.nn.softmax)
#        ])
#
#    model.compile(optimizer=keras.optimizers.Adam(lr=0.001, decay=0.1),
#                 loss='mean_squared_error',
#                  metrics=['accuracy'],)
#
#    model.fit(train_data, train_labels, epochs=5, batch_size=32)
#    model.save('savedNetwork.h5')
#    test_loss, test_acc = model.evaluate(test_data, test_labels)

    model.compile(optimizer=keras.optimizers.Adam(lr=0.001, decay=0.1),
                 loss='mean_squared_error',
                  metrics=['accuracy'],)

    model.fit(train_data, train_labels, epochs=5, batch_size=32)
    model.save('savedNetwork.h5')
    test_loss, test_acc = model.evaluate(test_data, test_labels)
'''

def loadModel():
    model = keras.models.load_model('savedNetwork.h5')
    model._make_predict_function()
    return model

def predictTeamComp(input):
    #trainModel()
    allyTeam = input[0:5]
    enemyTeam = input[5:10]
    enemyTeam.extend(allyTeam)
    #pred = np.reshape(createTempComp(input), (1,10,8))
    predAlly = createTempComp(input)
    tempAlly = np.array([predAlly, predAlly])
    predEnemy = createTempComp(enemyTeam)
    tempEnemy = np.array([predEnemy,predEnemy])
    allyFirstResult = trained_model.predict(tempAlly)[0][0]
    enemyResult = trained_model.predict(tempEnemy)[0][0]
    normalizer = 1 / (allyFirstResult + enemyResult)
    allyWin = normalizer*allyFirstResult
    return allyWin



def createTempComp(input):
    resultTC = np.zeros(141, dtype=int)
    for i in range(0, 5):
        resultTC[input[i]] = 1

    for i in range(5, 10):
        resultTC[input[i]] = -1
    return resultTC

trained_model = loadModel()
