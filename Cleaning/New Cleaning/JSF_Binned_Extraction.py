import mmap 
import numpy as np
import pyarrow as pa
import pyarrow.parquet as pq
import array
import os 
import struct

def main():
    with open('DANIA_17___Binned.jsf', 'rb') as f:

        schema = pa.schema([('pingNum', pa.int32()), ('channel', pa.int8()), ('angleScaleFactor', pa.float32()), ('twoWay', pa.float32()), ('angle', pa.int32())])

        big_Table = []

        size = os.path.getsize('DANIA_17___Binned.jsf')
        headerSize = 16
        i = 0
        x = True

        with mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as mm:
            while i < size:
                # Read header
                header = mm[i:i+headerSize]

                sonarMessage = int.from_bytes(header[4:6], byteorder='little', signed=True)
                # subSystem = int.from_bytes(header[8:9], byteorder='big', signed=True)
                channel = int.from_bytes(header[8:9], byteorder='big', signed=True)
                byteCount = int.from_bytes(header[12:16], byteorder='little', signed=False)
                # print("SonarMessage: ", sonarMessage)
                # print("SubSystem: ", subSystem)
                # print("Channel: ", channel)
                # print("ByteCount: ", byteCount)
                

                if(sonarMessage != 3000):
                    offset = headerSize + byteCount
                    i += offset
                elif(sonarMessage == 3000):
                    offset = headerSize + byteCount

                    bathyMessageData = mm[i+headerSize:i+headerSize+byteCount]

                    
                    pingNumArr, channelArr, angleScaleFactorArr, twoWay, angle = collectingBinnedData(bathyMessageData,channel,byteCount)

                    pingNumArr = pa.array(pingNumArr)
                    channelArr = pa.array(channelArr)
                    angleScaleFactorArr = pa.array(angleScaleFactorArr)
                    twoWay = pa.array(twoWay)
                    angle = pa.array(angle)

                    table = pa.Table.from_arrays([pingNumArr, channelArr, angleScaleFactorArr,twoWay,angle], schema=schema)
                    print(table)
                    big_Table.append(table)

                    i += offset

    table_concatenated = pa.concat_tables(big_Table)
    pq.write_table(table_concatenated,'JSF_BINNED_Extract.parquet')






            







def collectingBinnedData(bathyMessageData,channel,byteCount):
    pingNum = int.from_bytes(bathyMessageData[8:12], byteorder='little', signed=False)

    numSamples = int.from_bytes(bathyMessageData[12:14], byteorder='little', signed=False)

    timeToFirstSample = int.from_bytes(bathyMessageData[40:44], byteorder='little', signed=True)

    timeScaleFactor = struct.unpack('<f', bathyMessageData[48:52])[0]

    angleScaleFactor = struct.unpack('<f', bathyMessageData[56:60])[0]

    samples = array.array('H',bathyMessageData[80:byteCount])

        # samples = array.array('H', samples)

    timeDelay = np.array(samples[0::4])
    angle = np.array(samples[1::4])

    timeToFirstSample = timeToFirstSample / (10**9)
    timeDelay = np.multiply(timeDelay,timeScaleFactor)
    twoWay = np.add(timeDelay,timeToFirstSample)
        
    pingNumArr = [pingNum]*numSamples
    channelArr = [channel]*numSamples
    angleScaleFactorArr = [angleScaleFactor]*numSamples

    return pingNumArr, channelArr, angleScaleFactorArr, twoWay, angle



main()








