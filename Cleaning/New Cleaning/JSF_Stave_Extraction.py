import mmap 
import numpy as np
import pyarrow as pa
import pyarrow.parquet as pq
import array
import os 



def readJSF():
    schema = pa.schema([("sample", pa.float64()), ("channel", pa.int8()), ("pingNum", pa.uint32())])

    big_Table = []

    with open('DANIA_17__Stave.jsf', 'rb') as f:
        


        size = os.path.getsize('DANIA_17__Stave.jsf')
        print(size)
        headerSize = 16 
        
        pingNumCount = 0

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
                    # print(channel)

                    offset = headerSize + byteCount
                    sonarMessageData = mm[i+headerSize:i+headerSize+byteCount]


                    sample, channelArr, pingNumArr = collectingSamples(sonarMessageData, byteCount, channel)

                    sample = pa.array(sample)
                    channelArr = pa.array(channelArr)
                    pingNumArr = pa.array(pingNumArr)

                    table = pa.Table.from_arrays([sample, channelArr, pingNumArr], schema=schema)

                    big_Table.append(table)

                    # pingNum = int.from_bytes(sonarMessageData[8:12], byteorder='little', signed=False)
                    # weight = int.from_bytes(sonarMessageData[168:170], byteorder='little', signed=False)

                    i += offset
    table_concatenated = pa.concat_tables(big_Table)
    pq.write_table(table_concatenated,'real_numbers_STAVE.parquet')



def collectingSamples(byteList, byteCount, channel):
    pingNum = int.from_bytes(byteList[8:12], byteorder='little', signed=False)
    weight = int.from_bytes(byteList[168:170], byteorder='little', signed=False)
    sampleArray = byteList[240:byteCount]
   
    raw_samples = array.array('h', sampleArray)


    tempArr = np.array(raw_samples[::2])

    tempArr2 = np.array(raw_samples[1::2])


    weight = 2**-(weight) 

    tempArr2 = np.multiply(tempArr2, 1j)
    complexSample = np.add(tempArr, tempArr2)
    complexSample = np.multiply(complexSample, weight)

    conjugateData = np.conj(complexSample)

    sample = np.multiply(complexSample, conjugateData)
    
    sample = np.real(sample)
    sample = sample[1699:]
    sampleSize = len(sample)


    channelArr = [channel] * sampleSize
    pingNumArr = [pingNum] * sampleSize



    return sample, channelArr, pingNumArr 

readJSF()
 