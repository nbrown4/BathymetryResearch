# import pandas as pd
# import numpy as np
# // {"filePick": [ "DANIA_17_.001_Stave.jsf", "DANIA_17_.002_Stave.jsf", "DANIA_17_.003_Stave.jsf","DANIA_17_.004_Stave.jsf","DANIA_17_.005_Stave.jsf","DANIA_19__Stave.jsf","DANIA_19_.001_Stave.jsf","DANIA_19_.002_Stave.jsf","DANIA_19_.003_Stave.jsf","DANIA_22_.002_Stave.jsf","DANIA_22_.003_Stave.jsf","DANIA_21_.002_Stave.jsf","DANIA_21_.003_Stave.jsf"], 
# // "filePick2": ["DANIA_17_.001__Binned.jsf", "DANIA_17_.002__Binned.jsf","DANIA_17_.003__Binned.jsf","DANIA_17_.004__Binned.jsf","DANIA_17_.005__Binned.jsf","DANIA_19___Binned.jsf","DANIA_19_.001__Binned.jsf","DANIA_19_.002__Binned.jsf","DANIA_19_.003__Binned.jsf","DANIA_22_.002__Binned.jsf","DANIA_22_.003__Binned.jsf","DANIA_21_.002_Stave.jsf","DANIA_21_.003_Stave.jsf"]}
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

        inputs = Input(shape = (1,43173))
        hidden_Angle0 = Dense(800, kernel_initializer='lecun_normal', activation='selu')(inputs)
        # first layer was originally 1
        # good model was 400
        hidden_Angle1 = Dense(200, kernel_initializer='lecun_normal', activation='selu')(hidden_Angle0)

        output_Angle = Dense(400, name = "angle")(hidden_Angle1)

        hidden_twtt0 = Dense(400, activation='softmax')(inputs)
        hidden_twtt1 = Dense(100, activation='softmax')(hidden_twtt0) 
        # hidden_twtt2 = Dense(100, activation='softmax')(hidden_twtt1)
        output_twtt = Dense(400, name = "twtt")(hidden_twtt1)

        model = Model(inputs = inputs, outputs = [output_Angle, output_twtt])
        reduce_lr = ReduceLROnPlateau(monitor= 'accuracy', factor=0.5, patience=5, min_lr=1e-6, verbose=1) 
        model.compile(optimizer = tf.keras.optimizers.Adam(), loss=tf.keras.losses.MeanAbsoluteError(), metrics=['accuracy'])
        # before it was adamax and logcash
        # 4/17/2023 @ 4:39 I changed the shapes from 1089, 1 , x to 1089,x,1 and increased validation i lied 
        print(model.summary())
        model.fit(inputStave, [binned_angle, binned_twtt], epochs=40, batch_size=32, verbose=1, validation_split=0.4,callbacks = [reduce_lr])
        model.save('model13PhaseDif.h5')

        # added a 100 layer to twtt
        # changed validation split to .4
        
def predict(inputList, outputList):



    cleaner = sponge(inputList, outputList)
    stave, binnedAngles, binnedTWTT = cleaner.combined()
    
    model = tf.keras.models.load_model('model13PhaseDif.h5')

    angles,twtt = model.predict(stave)

    setBinnedLength = angles.shape[0] * angles.shape[2]
    print(setBinnedLength)
    angles = angles.reshape(setBinnedLength)
    twtt = twtt.reshape(setBinnedLength)

    real_angles = binnedAngles.reshape(setBinnedLength)
    real_twtt = binnedTWTT.reshape(setBinnedLength)

    df = pd.DataFrame({'predicted_Angles': angles, 'real_angles': real_angles, 'predicted_twtt': twtt, 'real_twtt': real_twtt})
    df['index'] = df.index

    plt.scatter(df['index'], df['real_angles'], color = 'black', s=.1)
    plt.scatter(df['index'], df['predicted_Angles'], color = 'red', s=.1)
    plt.legend(loc='upper left')
    plt.show()

    df.to_csv('test13PhaseDif.csv')

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
