import pandas as pd
import numpy as np

class sponge:

    def __init__(self, inputFileArr, outputFileArr):
        self.inputFileArr = inputFileArr
        self.outputFileArr = outputFileArr

    def cleaningBinned(self, binnedFile):
        # so im thinking this functions runs through a single binned file and cleans it
        # then it returns a cleaned binned file with the amount of pings in the file and the max and min ping number
        # later in a different function with gather all the info and combine the files into one dataframe
        df_binned = pd.read_parquet(binnedFile)

        minPingBinned = df_binned.pingNum.min()
        maxPingBinned = df_binned.pingNum.max()
        binnedAmount = maxPingBinned - minPingBinned

        df_binned = df_binned[df_binned['pingNum'] > minPingBinned]
        df_binned = df_binned[df_binned['pingNum'] <= maxPingBinned]
        df_binned = df_binned[df_binned['channel'] == 0]
        df_binned = df_binned.reset_index(drop=True)
        return df_binned, binnedAmount, minPingBinned, maxPingBinned
    
    def cleaningStave(self, staveFile, minPing, maxPing):

        df_stave = pd.read_parquet(staveFile)

        df_stave = df_stave[df_stave['pingNum'] > minPing]
        df_stave = df_stave[df_stave['pingNum'] <= maxPing]
        df_stave = df_stave[df_stave['channel']%2 == 0]
        df_stave = df_stave[['sample']]
        df_stave = df_stave.reset_index(drop=True)

        return df_stave
    
    def combined(self):
        inputFileList = self.inputFileArr
        outputFileList = self.outputFileArr

        cleannedInputs = []
        cleannedOutputs = []
        numberOfPings = 0
        
        for i in range(len(inputFileList)):
            
            staveFile = inputFileList[i]
            binnedFile = outputFileList[i]
            df_binned, binnedAmount, minPingBinned, maxPingBinned = self.cleaningBinned(binnedFile)
            df_stave = self.cleaningStave(staveFile, minPingBinned, maxPingBinned)
            cleannedInputs.append(df_stave)
            cleannedOutputs.append(df_binned)
            numberOfPings += binnedAmount

        binned = pd.concat(cleannedOutputs,axis=0)
        stave = pd.concat(cleannedInputs,axis=0)

        binned = binned.reset_index(drop=True)
        stave = stave.reset_index(drop=True)

        binnedAngles = binned[['angle']]
        binnedTWTT = binned[['twoWay']]

        binnedAngles = np.asarray(binnedAngles)
        binnedAngles = np.split(binnedAngles, numberOfPings)
        binnedAngles = np.asarray(binnedAngles)
        binnedAngles = binnedAngles.reshape(numberOfPings, 1,400)

        binnedTWTT = np.asarray(binnedTWTT)
        binnedTWTT = np.split(binnedTWTT, numberOfPings)
        binnedTWTT = np.asarray(binnedTWTT)
        binnedTWTT = binnedTWTT.reshape(numberOfPings, 1,400)

        stave = np.asarray(stave)
        stave = np.split(stave, numberOfPings)
        stave = np.asarray(stave)
        stave = stave.reshape(numberOfPings, 1, 47970)

        return stave, binnedAngles, binnedTWTT

    



    



