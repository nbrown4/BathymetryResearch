# import pandas as pd
# import numpy as np
import tensorflow as tf
from tensorflow import keras
from keras.callbacks import Callback, ReduceLROnPlateau
from keras.models import Model
from keras.layers import Input, Dense

from matplotlib import pyplot as plt

# how do i use the data from a json file in a python script?
#
import json
import mmap 
import numpy as np
import pyarrow as pa
import pyarrow.parquet as pq
import array
import os 
import struct
from Extraction import *
from dataPrep import *

def read_json_file(file_name):
    
    with open(file_name) as f:
        data = json.load(f)
        keys = list(data.keys())

        inputs = data[keys[0]]
        outputs = data[keys[1]]

        inputs.sort(reverse=True)
        outputs.sort(reverse=True)
        return inputs, outputs
        
def readStave(inputList):
    listOfParquetInputs = []
    for i in inputList:
        execute = staveExtract(i)
        execute.readJSF()
        name = i[:-4] + '.parquet'
        listOfParquetInputs.append(name)
    return listOfParquetInputs

def readBinned(outputList):
    listOfParquetOutputs = []
    for i in outputList:
        execute = binnedExtract(i)
        execute.readJSF()
        name = i[:-4] + '.parquet'
        listOfParquetOutputs.append(name)
    return listOfParquetOutputs

def buildModel(inputStave, binned_angle, binned_twtt):

        inputs = Input(shape = (1,47970))
        hidden_Angle0 = Dense(400, kernel_initializer='lecun_normal', activation='selu')(inputs)
        # first layer was originally 1
        hidden_Angle1 = Dense(400, kernel_initializer='lecun_normal', activation='selu')(hidden_Angle0)
        # hidden_Angle2 = Dense(100, kernel_initializer='lecun_normal', activation='selu')(hidden_Angle1)
        output_Angle = Dense(400, name = "angle")(hidden_Angle1)

        hidden_twtt0 = Dense(400, activation='softmax')(inputs)
        # hidden_twtt1 = Dense(200, activation='softmax')(inputs) 
        # hidden_twtt2 = Dense(100, activation='softmax')(hidden_twtt1)
        output_twtt = Dense(400, name = "twtt")(hidden_twtt0)

        model = Model(inputs = inputs, outputs = [output_Angle, output_twtt])
        reduce_lr = ReduceLROnPlateau(monitor= 'accuracy', factor=0.5, patience=10, min_lr=1e-6, verbose=1) 
        model.compile(optimizer = tf.keras.optimizers.Adamax(), loss=tf.keras.losses.LogCosh(), metrics=['accuracy'])
        model.fit(inputStave, [binned_angle, binned_twtt], epochs=100, batch_size=16, verbose=1, validation_split=0.33,callbacks = [reduce_lr])
        print("In here")
        model.save('model2.h5')

def predict(inputList, outputList):



    cleaner = sponge(inputList, outputList)
    stave, binnedAngles, binnedTWTT = cleaner.combined()
    
    model = tf.keras.models.load_model('model2.h5')
    angles,twtt = model.predict(stave)

    angles = angles.reshape(435600)
    twtt = twtt.reshape(435600)

    real_angles = binnedAngles.reshape(435600)
    real_twtt = binnedTWTT.reshape(435600)

    df = pd.DataFrame({'predicted_Angles': angles, 'real_angles': real_angles, 'predicted_twtt': twtt, 'real_twtt': real_twtt})
    df['index'] = df.index

    plt.scatter(df['index'], df['real_angles'], color = 'black', s=.1)
    plt.scatter(df['index'], df['predicted_Angles'], color = 'red', s=.1)
    plt.legend(loc='upper left')
    plt.show()

    # how do i export a pandas dataframe to a csv file?
    df.to_csv('test.csv')



        

        



def main():
    inputList, outputList = read_json_file('fileSelection.json')
    parquetInputList = readStave(inputList)
    parquetOutputList = readBinned(outputList)
    predictingInput = parquetInputList[0:1]
    predictedOutput = parquetOutputList[0:1]


    cleanData = sponge(parquetInputList, parquetOutputList)
    stave, binnedAngles, binnedTWTT = cleanData.combined()

    buildModel(stave, binnedAngles, binnedTWTT)
    predict(predictingInput, predictedOutput)

    #!TODO so it looks like we are extracting the right stuff next thing is to put it inside a model
main()

