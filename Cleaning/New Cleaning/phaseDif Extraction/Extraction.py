import mmap 
import numpy as np
import pyarrow as pa
import pyarrow.parquet as pq
import array
import os 
import struct
class staveExtract:
    def __init__(self, inputFile):
        self.inputFile = inputFile

    def grabPhaseDif(self,storageArr):
        samplesPerChannel = []
        channelArr = []
    # format of the arr is [sonarMessageData, channel, byteCount] * 20
        for i in range(len(storageArr)):
            sonarMessageData = storageArr[i][0]
            byteCount = storageArr[i][2]

            pingNum = int.from_bytes(sonarMessageData[8:12], byteorder='little', signed=False)
            weight = int.from_bytes(sonarMessageData[168:170], byteorder='little', signed=False)
            sampleArray = sonarMessageData[240:byteCount]

            raw_samples = array.array('h', sampleArray)


            tempArr = np.array(raw_samples[::2])

            tempArr2 = np.array(raw_samples[1::2])


            weight = 2**-(weight) 

            tempArr2 = np.multiply(tempArr2, 1j)
            complexSample = np.add(tempArr, tempArr2)
            complexSample = np.multiply(complexSample, weight)

            complexSample = complexSample[1699:]
            # print(len(complexSample))


            samplesPerChannel.append(complexSample)
            channelArr.append(storageArr[i][1])

        samplesPerEvenChannel = samplesPerChannel[0::2]

        #! for now we are only grabbing the even channels
        port = samplesPerEvenChannel[:-1]
        portCopy = samplesPerEvenChannel[1:]
        processingMultiply = []
        for i in range(len(port)):
            processingMultiply.append(np.multiply(port[i], np.conj(portCopy[i])))

        processingMultiply = np.asarray(processingMultiply)    
        processingMultiply = processingMultiply.reshape(-1)

        phaseDif = np.angle(processingMultiply)

        length = len(phaseDif)
        # print(length)

        # channelArr = [channel] * length
        #! I guess channels dont really matter since we are only grabbing the even channels and they are all the same ping
        pingNumArr = [pingNum] * length


        return phaseDif, pingNumArr


    def readJSF(self):
        fileName = self.inputFile
        exportFileName = fileName[:-4] + '.parquet'

        schema = pa.schema([("sample", pa.float64()), ("pingNum", pa.uint32())])
        big_Table = []
        pingStorage = []


        with open (fileName, 'rb') as f:
            size = os.path.getsize(fileName)
            headerSize = 16
            i = 0

            with mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as mm:
                
                while i < size:

                    header = mm[i:i+headerSize]
                    subSystem = int.from_bytes(header[7:8], byteorder='little', signed=False)
                    channel = int.from_bytes(header[8:9], byteorder='big', signed=False)
                    byteCount = int.from_bytes(header[12:16], byteorder='little', signed=False)

                    if(subSystem == 0):
                        offset = headerSize + byteCount
                        i += offset

                    if(subSystem == 20):
                        offset = headerSize + byteCount
                        i += offset
                    if(subSystem == 21):
                        offset = headerSize + byteCount
                        i += offset
                    if(subSystem == 101):
                        offset = headerSize + byteCount
                        i += offset
                    if(subSystem == 102):
                        offset = headerSize + byteCount
                        i += offset
                    if(subSystem == 40):
                        offset = headerSize + byteCount
                        sonarMessageData = mm[i+headerSize:i+headerSize+byteCount]
                        container =[sonarMessageData, channel, byteCount]
                    
                        pingStorage.append(container)


                    
                        if channel == 19:
                            sample, pingNum = self.grabPhaseDif(pingStorage)
                            pingStorage = []

                            sample = pa.array(sample)
                            pingNum = pa.array(pingNum)

                            table = pa.Table.from_arrays([sample, pingNum], schema=schema)

                            big_Table.append(table)

                        i += offset
        table_concatenated = pa.concat_tables(big_Table)
        pq.write_table(table_concatenated,exportFileName)

class binnedExtract: 
    def __init__(self, inputFile):
        self.inputFile = inputFile

    def collectingBinnedData(self,bathyMessageData,channel,byteCount):
        pingNum = int.from_bytes(bathyMessageData[8:12], byteorder='little', signed=False)

        numSamples = int.from_bytes(bathyMessageData[12:14], byteorder='little', signed=False)

        timeToFirstSample = int.from_bytes(bathyMessageData[40:44], byteorder='little', signed=True)

        timeScaleFactor = struct.unpack('<f', bathyMessageData[48:52])[0]

        angleScaleFactor = struct.unpack('<f', bathyMessageData[56:60])[0]

        samples = array.array('H',bathyMessageData[80:byteCount])
        i = 86 
        filterFlag = []
        while i < byteCount:
            arr = struct.unpack('B', bathyMessageData[i:i+1])[0]
            filterFlag.append(arr)
            i += 8


        timeDelay = np.array(samples[0::4])
        angle = np.array(samples[1::4])




        timeToFirstSample = timeToFirstSample / (10**9)
        timeDelay = np.multiply(timeDelay,timeScaleFactor)
        twoWay = np.add(timeDelay,timeToFirstSample)
            
        pingNumArr = [pingNum]*numSamples
        channelArr = [channel]*numSamples
        angleScaleFactorArr = [angleScaleFactor]*numSamples

        
        return pingNumArr, channelArr, angleScaleFactorArr, twoWay, angle, filterFlag
        
    def readJSF(self):
        fileName = self.inputFile
        exportFileName = fileName[:-4] + '.parquet'

        schema = pa.schema([('pingNum', pa.int32()), ('channel', pa.int8()), ('angleScaleFactor', pa.float32()), ('twoWay', pa.float32()), ('angle', pa.int32()),('filterFlag', pa.int8())])

        big_Table = []

        with open (fileName, 'rb') as f:
            size = os.path.getsize(fileName)
            headerSize = 16
            i = 0
            with mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as mm:
                while i < size:
                    # Read header
                    header = mm[i:i+headerSize]

                    sonarMessage = int.from_bytes(header[4:6], byteorder='little', signed=True)
                    # subSystem = int.from_bytes(header[8:9], byteorder='big', signed=True)
                    channel = int.from_bytes(header[8:9], byteorder='big', signed=True)
                    byteCount = int.from_bytes(header[12:16], byteorder='little', signed=False)
                    

                    if(sonarMessage != 3000):
                        offset = headerSize + byteCount
                        i += offset
                    elif(sonarMessage == 3000):
                        offset = headerSize + byteCount

                        bathyMessageData = mm[i+headerSize:i+headerSize+byteCount]

                        
                        pingNumArr, channelArr, angleScaleFactorArr, twoWay, angle, filterFlag = self.collectingBinnedData(bathyMessageData,channel,byteCount)

                        pingNumArr = pa.array(pingNumArr)
                        channelArr = pa.array(channelArr)
                        angleScaleFactorArr = pa.array(angleScaleFactorArr)
                        twoWay = pa.array(twoWay)
                        angle = pa.array(angle)
                        filterFlag = pa.array(filterFlag)

                        table = pa.Table.from_arrays([pingNumArr, channelArr, angleScaleFactorArr,twoWay,angle,filterFlag], schema=schema)
                        # print(table)
                        big_Table.append(table)

                        i += offset

        table_concatenated = pa.concat_tables(big_Table)
        pq.write_table(table_concatenated, exportFileName)







