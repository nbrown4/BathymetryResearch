import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os


def sub80samples(filename):
    channelArr = []
    pingNumArr = []
    sampleStorage = []

    i = 0
    print(os.getcwd)
    with open(f"Website\static\DataFiles\{filename}",  'rb') as file:
        # byte = f.read(1)
        # og num is 50717
        while(i < 100):

            startOfMessage = np.fromfile(file, 'int16',  1)
            # print("Start of Message: ",  startOfMessage)

            version = np.fromfile(file, 'int8',  1)
            # print("Version: ",  version)

            sessionId = np.fromfile(file, 'int8',  1)
            # print("SessionID: ",  sessionId)

            sonarMessage = np.fromfile(file, 'int16', 1)
            # print("SonarMessage: ",  sonarMessage)
            
            sonarCommand = np.fromfile(file, 'int8', 1)
            # print("SonarCommand: ",  sonarCommand)

            subSystem = np.fromfile(file, 'int8', 1)
            # print("SubSystem: ",  subSystem)

            channel = np.fromfile(file, 'int8', 1)
            # channelNum.append(channel) 


            # print("Channel: ",  channel)

            sequence = np.fromfile(file, 'int8', 1)
            # print("Sequence: ",  sequence)

            reservedHeader = np.fromfile(file, 'int16', 1)
            # print("ReservedHeader: ",  reservedHeader)

            byteCount = np.fromfile(file, 'uint32', 1)
            # print("ByteCount: ",  byteCount)
            # x = byteCount[0]
            

            if(subSystem == 0):
                np.fromfile(file, 'int8',  byteCount[0])
                # pd.DataFrame(skip).to_csv("skipper")
                # print(skip)

            if(subSystem == 20):
                np.fromfile(file, 'int8',  byteCount[0])
            if(subSystem == 21):
                np.fromfile(file, 'int8',  byteCount[0])
            if(subSystem == 101):
                np.fromfile(file, 'int8',  byteCount[0])
            if(subSystem == 102):
                np.fromfile(file, 'int8',  byteCount[0])


            
            if(subSystem == 40):
                # print("Start of Message: ",  startOfMessage)
                # print("Version: ",  version)
                # print("SessionID: ",  sessionId)
                # print("SonarMessage: ",  sonarMessage)
                # print("SonarCommand: ",  sonarCommand)
                # print("SubSystem: ",  subSystem)
                # print("Channel: ",  channel)
                # print("Sequence: ",  sequence)
                # print("ReservedHeader: ",  reservedHeader)
                # print("ByteCount: ",  byteCount)
                
                seconds = np.fromfile(file, 'uint8', 4)
                # print("Seconds: ",  seconds)

                startDepth = np.fromfile(file, 'int32', 1)
                # print("StartDepth: ",  startDepth)

                pingNum = np.fromfile(file, 'uint32', 1)
                # pingNumArr.append(pingNum)
                # print("PingNum: ",  pingNum)

                #! Array number

                reserved0 = np.fromfile(file, 'int32', 1)
                # print("Reserved0: ",  reserved0)

                msb = np.fromfile(file, 'uint16', 1)
                # print("Msb: ",  msb)

                lsb = np.fromfile(file, 'uint16', 1)
                # print("LSB: ",  lsb)

                lsb2 = np.fromfile(file, 'uint16', 1)
                # print("LSB2: ",  lsb2)

                reserved1 = np.fromfile(file, 'int16', 3)
                # print("N/A: ",  reserved1)

                iDcode = np.fromfile(file, 'int16', 1)
                # print("TraceIDCode: ",  iDcode)

                validityFlag = np.fromfile(file, 'uint16', 1)
                # print("ValidityFlag: ",  validityFlag)

                reserved2 = np.fromfile(file, 'uint16', 1)
                # print("Reserved2:",  reserved2)

                dataFormat = np.fromfile(file, 'int16', 1)
                # print("DataFormat: ",  dataFormat)

                antennaDist1 = np.fromfile(file, 'int16', 1)
                # print("AntennaDist1: ",  antennaDist1)

                antennaDist2 = np.fromfile(file, 'int16', 1)
                # print("AntennaDist2: ",  antennaDist2)

                reserved3 = np.fromfile(file, 'uint16', 2)
                # print("Reserved3: ",  reserved3)

                kp = np.fromfile(file, 'float32', 1)
                # print("Kp: ",  kp)

                heave = np.fromfile(file, 'float32', 1)
                # print("Heave: ",  heave)

                reserved4 = np.fromfile(file, 'uint8', 12)
                # print("Reserved4: ",  reserved4)

                pulseInfo =np.fromfile(file, 'float32', 2)
                # print("PulseInfo: ",  pulseInfo)

                reserved5 = np.fromfile(file, 'int32', 1)
                # print("Reserved4: ",  reserved4)

                gapFillerLateralPositionOffset =np.fromfile(file, 'single', 1)
                # print("GapFillerLateralPositionOffset: ",  gapFillerLateralPositionOffset)

                lon = np.fromfile(file, 'int32', 1)
                # print("Longitude: ",  lon)

                lat = np.fromfile(file, 'int32', 1)
                # print("Latitude ",  lat)

                positionUnit = np.fromfile(file, 'int16', 1)
                # print("PositionUnit: ",  positionUnit)

                    # We shall figure this out later
                # if(positionUnit == 2): 
                #     longitude = (lon/10000)/60
                #     latitude = (lat/10000)/60
                annotation = np.fromfile(file, 'uint8', 24)
                # print("Annotation: ",  annotation)

                samples = np.fromfile(file, 'uint16', 1)
                # print("Samples: ",  samples)

                sampleInterval = np.fromfile(file, 'uint32', 1)
                # print("Sample Interval: ",  sampleInterval)

                adcGain = np.fromfile(file, 'uint16', 1)
                # print("ADCGain: ",  adcGain)

                transmitLevel = np.fromfile(file, 'int16', 1)
                # print("Transmit Level: ",  transmitLevel)

                reserved6 = np.fromfile(file, 'int16', 1)
                # print("Reserved6: ",  reserved6)

                startF = np.fromfile(file, 'uint16', 1)
                # print("StartF: ",  startF)
                # Convert to HZ

                stopF = np.fromfile(file, 'uint16', 1)
                # print("StopF: ",  stopF)
                # Convert to HZ

                pulseLength = np.fromfile(file, 'uint16', 1)
                # print("Pulse Length: ",  pulseLength)
                # Converting 

                pressure = np.fromfile(file, 'int32', 1)
                # print("Pressure: ",  pressure)

                depth = np.fromfile(file, 'int32', 1)
                # print("Depth: ",  depth)

                fs = np.fromfile(file, 'uint16', 1)
                # print("Fs: ",  fs)

                pulse_id = np.fromfile(file, 'uint16', 1)
                # print("Pulse ID: ",  pulse_id)

                altitude = np.fromfile(file, 'uint32', 1)
                # altitudeArr.append(altitude[0])
                # print("Altitude: ",  altitude)

                #! array here

                soundSpeed = np.fromfile(file, 'float32', 1)
                # print("Sound Speed: ",  soundSpeed)

                mixerFreq = np.fromfile(file, 'float32', 1)
                # print("MixerFreq: ",  mixerFreq)

                year = np.fromfile(file, 'int16', 1)
                # print("Year: ",  year)

                day = np.fromfile(file,  'uint16', 1)
                # print("Day: ",  day)

                hours = np.fromfile(file, 'uint16', 1)
                # print("Hours: ",  hours)

                minutes = np.fromfile(file, 'uint16', 1)
                # print("Minutes: ",  minutes)

                seconds = np.fromfile(file, 'uint16', 1)
                # print("Seconds: ",  seconds)

                timeBasis = np.fromfile(file, 'int16', 1)
                # print("TimeBasis: ",  timeBasis)

                weight = np.fromfile(file, 'int16', 1)
                # print("Weight: ",  weight)

                numPulses = np.fromfile(file, 'int16', 1)
                # print("NumPulses: ",  numPulses)

                compassHeading = np.fromfile(file, 'uint16', 1)
                # print("CompassHeading: ",  compassHeading)
                # Have to convert to something

                pitch = np.fromfile(file, 'int16', 1)
                # print("Pitch: ",  pitch)
                # Have to convert to something

                roll = np.fromfile(file, 'int16', 1)
                # print("Roll: ",  roll)
                # Have to convert to something

                reserved7= np.fromfile(file, 'int16', 2)
                # print("Reserved7: ",  reserved7)

                triggerSource = np.fromfile(file, 'int16', 1)
                # print("TriggerSource: ",  triggerSource)

                markNumber = np.fromfile(file, 'int16', 1)
                # print("MarkNumber: ",  markNumber)

                posFixHours = np.fromfile(file, 'int16', 1)
                # print("PosFixHours: ",  posFixHours)

                posFixMinutes = np.fromfile(file, 'int16', 1)
                # print("PosFixMinutes: ",  posFixMinutes)

                postFixSeconds = np.fromfile(file, 'int16', 1)
                # print ("PostFixSeconds: ",  postFixSeconds)

                # postfixSecondsArr.append(postFixSeconds)
                #! seconds

                course = np.fromfile(file, 'int16', 1)
                # print("Course: ",  course)

                speed = np.fromfile(file, 'int16', 1)
                # print("Speed: ",  speed)

                posFixDay = np.fromfile(file, 'int16', 1)
                # print("PosFixDay: ",  posFixDay)
                
                posFixYear = np.fromfile(file, 'int16', 1)
                # print("PosFixYear: ",  posFixYear)

                millisecondsToday = np.fromfile(file, 'uint32', 1)
                # print("MillisecondsToday: ",  millisecondsToday)

                # millisecondsTodayArr.append(millisecondsToday[0])


                #! Array here

                maxADCValue = np.fromfile(file, 'uint16', 1)
                # print("MaxADCValue: ",  maxADCValue)

                reserved8 = np.fromfile(file, 'uint16', 2)
                # print("Reserved8: ",  reserved8)

                sonarVersion = np.fromfile(file, 'int8', 6)
                # print("SonarVersion: ",  sonarVersion)

                sphericalCorrection = np.fromfile(file, 'int32', 1)
                # print("SphericalCorrection: ",  sphericalCorrection)

                packetNumber = np.fromfile(file, 'uint16', 1)
                # print("PacketNumber: ",  packetNumber)

                ADCDecimation = np.fromfile(file, 'int16', 1)
                # print("AdcDecimation: ",  ADCDecimation)

                reserved9 = np.fromfile(file, 'int16', 1)
                # print("Reserved9: ",  reserved9)

                waterTemperature = np.fromfile(file, 'uint16', 1)
                # print("WaterTemperature: ",  waterTemperature)

                layBack = np.fromfile(file, 'float32', 1)
                # print("LayBack: ",  layBack)

                reserved10 = np.fromfile(file, 'int32', 1)
                # print("Reserved10: ",  reserved10)
    
                cableOut = np.fromfile(file, 'uint16', 1)
                # print("CableOut: ",  cableOut) 

                reserved11 = np.fromfile(file, 'int16', 1)



                

                
                
                numSamples = int((byteCount[0] - 240)/4)
                #! I explicetely casted to int because loop cant take in numpy.float64 values

                tempArr = []
                tempArr2 = []

                for y in range((numSamples*2)):
                    # print(y)
                    temp = (np.fromfile(file, 'int16',  1))

                    if y%2 == 0:
                        tempArr.append(temp[0])
                    else:
                        tempArr2.append(temp[0])

                # print(tempArr2[-10:])
                arrSize = len(tempArr)
                
                nuWeight = int(weight[0])
                complexSample = []
                
                for x in range(arrSize):

                    complexNum = (tempArr[x] + tempArr2[x]*1j) * (2**-(nuWeight))
                    # num = complex(complexNum)
                    complexSample.append(complexNum)

                    # some = np.append(sample_data, complexNum)  
                # print(complexSample)
                conjugateData = np.conj(complexSample)
                sample_data = np.array(complexSample)

            
                sample = np.multiply(sample_data,  conjugateData)
                nuSample = []
                

                sampleSize = len(sample)
                for v in range (sampleSize):
                    a = (sample[v].real)
                    nuSample.append(a)
                    
                # print(sample)
                # print(sampleSize)
                for z in range(sampleSize):

                    

                    channelArr.append(channel[0])

                    pingNumArr.append(pingNum[0])

                    sampleStorage.append(nuSample[z])


            i+=1
    a = {'sample':sampleStorage, 'channel': channelArr,  'pingNum': pingNumArr}

    df = pd.DataFrame.from_dict(a)
    df = df = df[df['pingNum'] == 64209]
    df = df[df['channel'] == 2]
    plt.clf()
    plt.plot(df)
    plt.savefig('Website/static/my_plot.png')
    return(df)


def Script_3000(filename):
    # from cmath import pi
    import numpy as np
    contentType = -1
    cnt = 0
    i = 0 

    # startfArr = []
    # startOfMessageArr =[]

    pingArr = []
    channelArr = []
    delayIndexArr = []
    angleArr = []
    pingKeyArr = []

    #dateTime
    secondsArr = []
    nanosecondsArr = []

    timeScaleArr = []
    timeFirst = []
    angleScaleArr = []
    # data of time stamp,  ping number,  channel,  delay index,  and angle.


    with open(f"Website\static\DataFiles\{filename}",  "rb") as file:

        while(i < 2000):
            i+=1


            startOfMessage = np.fromfile(file, 'int16',  1)
            # startOfMessageArr.append(startOfMessage)
            # print("Start of Message: ",  startOfMessage)

            version = np.fromfile(file, 'int8',  1)
            # print("Version: ",  version)

            sessionId = np.fromfile(file, 'int8',  1)
            # print("SessionID: ",  sessionId)

            sonarMessage = np.fromfile(file, 'int16', 1)
            # print("SonarMessage: ",  sonarMessage)
            
            sonarCommand = np.fromfile(file, 'int8', 1)
            # print("SonarCommand: ",  sonarCommand)

            subSystem = np.fromfile(file, 'int8', 1)
            # print("SubSystem: ",  subSystem)

            channel = np.fromfile(file, 'int8', 1)
            # channelNum.append(channel) 


            # print("Channel: ",  channel)

            sequence = np.fromfile(file, 'int8', 1)
            # print("Sequence: ",  sequence)

            reservedHeader = np.fromfile(file, 'int16', 1)
            # print("ReservedHeader: ",  reservedHeader)

            byteCount = np.fromfile(file, 'uint32', 1)


            if (sonarMessage != 3000):
                np.fromfile(file, 'int8',  byteCount[0])
                # print(byteCount[0])
            

            if (sonarMessage == 3000):
                # print(byteCount[0])
                # print("hoes mad")
                bytesRead = 0

                seconds = np.fromfile(file,  'uint32',  1)

                

                # print(seconds)
                bytesRead += 4

                nanoseconds = np.fromfile(file,  'uint32',  1)

                

                # print(milliseconds)
                bytesRead += 4

                # timeStamp = (seconds + milliseconds) / ((1*10)**6)

                pingNum = np.fromfile(file,  'uint32',  1)
                pingArr.append(pingNum)
                bytesRead += 4

                nsamps = np.fromfile(file,  'uint16',  1)
                bytesRead += 2

                channel = np.fromfile(file,  'uint8',  1)
                bytesRead += 1

                algo = np.fromfile(file,  'uint8',  1)
                bytesRead += 1

                numPulses = np.fromfile(file,  'uint8',  1)
                bytesRead += 1

                pulsePhase = np.fromfile(file,  'uint8',  1) 
                bytesRead += 1

                pulseLength = np.fromfile(file,  'uint16',  1) #/ ((1*10)**6)
                bytesRead += 2

                pulsePower = np.fromfile(file,  'float32',  1)
                bytesRead += 4

                startf = np.fromfile(file,  'float32',  1)

                # startfArr.append(startf)

                
                # print(startf)
                stopf = np.fromfile(file,  'float32',  1)
                bytesRead += 8

                random = np.fromfile(file,  'float32',  1)
                bytesRead += 4

                fsample = np.fromfile(file,  'float32',  1)
                bytesRead += 4

                timeToFirstSample = np.fromfile(file,  'uint32',  1)
                

                # print("TimetoFirstSample", timeToFirstSample)
                bytesRead += 4

                timeUncertantity = np.fromfile(file,  'float32',  1)
                timeScaleFactor = np.fromfile(file,  'float32',  1)
                

                # print("TimeScaleFactor", timeScaleFactor)
                bytesRead += 8

                random2 = np.fromfile(file,  'float32',  1)
                bytesRead += 4
                
                angleScaleFactor = np.fromfile(file,  'float32',  1)
                bytesRead += 4
                # print("Angle Scale Factor: ",  angleScaleFactor)

                random3 = np.fromfile(file,  'float32',  1)
                bytesRead += 4

                timeToBottom = np.fromfile(file,  'uint32',  1)
                # print(timeToBottom)
                bytesRead += 4

                random4 = np.fromfile(file,  'uint8',  1)
                bytesRead += 1

                binData = np.fromfile(file,  'uint8',  1)
                # print(binData)
                bytesRead += 1

                tvg = np.fromfile(file,  'uint16',  1)
                bytesRead += 2

                swath = np.fromfile(file,  'float32',  1)
                bytesRead += 4

                binSize = np.fromfile(file,  'float32',  1)
                # print(binSize)
                bytesRead += 4


                
                

                for z in range(nsamps[0]):
                    nanosecondsArr.append(nanoseconds[0])
                    secondsArr.append(seconds[0])

                    channelArr.append(channel[0])

                    pingKeyArr.append(pingNum[0])
                    angleScaleArr.append(angleScaleFactor[0])
                    timeScaleArr.append(timeScaleFactor[0])
                    timeFirst.append(timeToFirstSample[0])

                    timeDelay = np.fromfile(file,  'uint16',  1)
                    
                    delayIndexArr.append(timeDelay[0])

                    bytesRead += 2
                    angle = np.fromfile(file,  'int16',  1)

                    angleArr.append(angle[0])

                    bytesRead += 2
                    amp = np.fromfile(file,  'uint8',  1)
                    bytesRead += 1
                    sigma = np.fromfile(file,  'uint8',  1)
                    bytesRead += 1

                    filterFlag = np.fromfile(file,  'uint8',  1)
                    bytesRead += 1
                    anything = np.fromfile(file,  'uint8',  1)
                    bytesRead += 1
                    
                    # bytesRead+=8

                    
                
                # print(binSize[0])
                
                np.fromfile(file, 'int8',  (byteCount[0] - bytesRead)) 
                    
                    
            # if(messageType == 3001 )
    a = { 'Channel': channelArr,  'DelayIndex': delayIndexArr,  'Angle': angleArr,  'Seconds': secondsArr,  'Nanoseconds': nanosecondsArr,  'PingKey':pingKeyArr,  'TimeToFirst': timeFirst,  'TimeScaleFactor': timeScaleArr,  'AngleScaleFactor': angleScaleArr}

    df = pd.DataFrame.from_dict(a,  orient='index')
    df = df.transpose()

    df['Nanoseconds'] = df['Nanoseconds'].astype(str)
    df['Nanoseconds']= df.Nanoseconds.str[:3]

    df['Nanoseconds'] = '.' + df['Nanoseconds']

    df['dateTime']=pd.to_datetime(df['Seconds'],   unit='s',  origin='unix')
    df['dateTime'] = df['dateTime'].dt.strftime('%Y-%d-%m %H:%M:%S')
    df['dateTime'].astype(str)
    df['dateTime'] = df['dateTime'] + df['Nanoseconds']


    df['TWTT'] = (df['TimeToFirst']/(10**9)) + (df['DelayIndex'] * df['TimeScaleFactor'])

    df['Angle'] = df['Angle'] * df['AngleScaleFactor']

    df = df[['PingKey',  'Channel',  'TWTT',  'Angle',  'dateTime']]
    
    
   
        

    print(df)

    # df['Angle'] = df['Angle']/180*np.pi
    # df['nuAngle'] = df['AngleScaleFactor'] * df['Angle']
    # df['Angle'] = df['Angle']  * (10**5)
    # df['PingNum'].astype(str)
    
    return(df)

                
    