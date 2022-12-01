function [messageHeader,data,header] = readJSF_V3_Bathy(fileid)
%Use fopen to open file for reading prior to calling.


data =[];
messageHeader.contentType=-1;
header = [] ;

%start , look for SonarMessageHeaderType
while 1==1
  messageHeader.startOfMessage = fread(fileid,1,'int16');
  messageHeader.version = fread(fileid,1,'int8');
  [messageHeader.sessionId,cnt] = fread(fileid,1,'int8');

  %check if we read any data ....  (EOF ?)
  if cnt == 0
    messageHeader.contentType = -4 ;
    return
  end

  %Check if valid message
  if (messageHeader.startOfMessage ~= hex2dec('1601') )
    messageHeader.contentType =-1;  %Not valid JSF format data or lost sync!
    return
  end

  messageHeader.messageType = fread(fileid,1,'int16');
  messageHeader.commandType = fread(fileid,1,'int8');
  messageHeader.subsystem = fread(fileid,1,'int8');  %0 = SB, 20 = SSL, 21 = SSH, 40 = bathy
  messageHeader.channel= fread(fileid,1,'uint8');  %0=port, 1 = stbd for SS systems
  messageHeader.sequenceNo = fread(fileid,1,'int8');
  fread(fileid,1,'int16');%Reserved field, 16 bits

  [messageHeader.byteCount,cnt] = fread(fileid,1,'uint32'); %Size of data block  which follows

  if isempty(messageHeader.messageType) || cnt == 0
    messageHeader.contentType = -4;
    return
  end

  if messageHeader.messageType == 80 || messageHeader.messageType == 3000 || messageHeader.messageType == 3001 || ...
      messageHeader.messageType == 3002 || messageHeader.messageType == 3004

    switch messageHeader.messageType
      case 80  %Sonar Trace Data (JsfDefs.h)
        if messageHeader.subsystem == 40 
          messageHeader.contentType = 1 ;
          header.seconds = fread(fileid,1,'uint32'); %in seconds
          header.startDepth = fread(fileid,1,'int32'); %in samples
          header.pingNum = fread(fileid,1,'uint32');
          header.reserved0 = fread(fileid,1,'int32');


          header.MSB = fread(fileid,1,'uint16');                                %bytes 16-17
          %decode for Freq MSBs
          header.startFreqAdd=bitand(header.MSB,15);
          header.endFreqAdd = bitand(header.MSB,240)/16;
          header.addSamples = bitand(header.MSB,3840)/256;

          header.LSB = fread(fileid,1,'uint16');                                 %bytes 18-19
          header.addSampleInterval = bitand(header.LSB,255);
          header.fractionalCourse = bitshift(header.LSB,-8) ;
          header.LSB2 = fread(fileid,1,'uint16');                                %bytes 20-21
          header.reserved1 = fread(fileid,3,'int16');                            %bytes 22-27
          header.iDCode = fread(fileid,1,'int16');                               %bytes 28-29 (always = 1)
          header.validityFlag = fread(fileid,1,'uint16');                        %bytes 30-31
          header.reserved2 = fread(fileid,1,'uint16');                           %bytes 32-33
          header.dataFormat = fread(fileid,1,'int16');                           %bytes 34-35
          % 0 = 1 short/sample Env dat
          % 1 = 2 shorts/sample Analytic
          % 2 = 1 short/sample RAW
          header.AntennaDist1 = fread(fileid,1,'int16');                          %bytes 36-37
          header.AntennaDist2 = fread(fileid,1,'int16');                          %bytes 38-39
          header.reserved3 = fread(fileid,2,'uint16');                            %bytes 40-43
          header.KP = fread(fileid,1,'float32');                                  %bytes 44-47
          header.heave = fread(fileid,1,'float32');                               %bytes 48-51
          header.reserved4 = fread(fileid,12,'uint8');                            %bytes 52-63
          header.pulseInfo = fread(fileid,2,'float32');                           %bytes 64-71
          header.reserved5 = fread(fileid,1,'int32');                             %bytes 72-75
          header.gapFillerLateralPositionOffset = fread(fileid,1,'single');       %bytes 76-79
          header.lon = fread(fileid, 1, 'int32') ; % Longiture or X               %bytes 80-83
          header.lat = fread(fileid, 1, 'int32') ; % Latitude or Y                %bytes 84-87
          header.positionunit = fread(fileid, 1, 'int16') ; % Coordinate Units    %bytes 88-89
          % 1 = X, Y in millimeters
          % 2 = Latitude, longitude in minutes of arc times 10000
          % 3 = X, Y in decimeters
          if header.positionunit == 2
            header.lon = (header.lon / 10000) / 60 ; % convert to degrees
            header.lat = (header.lat / 10000) / 60 ; % convert to degrees
          end

          header.annotation = fread(fileid,24,'uint8');                           %bytes 90-113
          header.samples = fread(fileid,1,'uint16');                              %bytes 114-115
          header.sampleInterval = fread(fileid,1,'uint32'); %ns                   %bytes 116-119
          header.ADCGain = fread(fileid,1,'uint16');                              %bytes 120-121
          header.transmitlevel = fread(fileid,1,'int16');
          %bytes 122-123
          header.reserved6 = fread(fileid,1,'int16');                             %bytes 124-125
          header.startf = fread(fileid,1,'uint16');                               %bytes 126-127
          %Starting frequency in DecaHz
          header.startf= (header.startf + header.startFreqAdd*2^16)*10;  %Hz
          header.stopf = fread(fileid,1,'uint16');                               %bytes 128-129
          %ie multiply this value by 10 for Hz.
          header.stopf=(header.stopf + header.endFreqAdd*2^16)*10;  %Hz
          if mod(messageHeader.channel,2) == 0 % needed since concatinating all channels irrespective of side
            header.portstartf =  header.startf ;
            header.portstopf =  header.stopf ;
          else
            header.stbdstartf =  header.startf ;
            header.stbdstopf =  header.stopf ;
          end
          header.pulselength = fread(fileid,1,'uint16');                          %bytes 130-131
          header.pulselength = header.pulselength * 1e-3 + bitshift(header.LSB2,-4) * 1e-6;
          header.pressure = fread(fileid,1,'int32');                              %bytes 132-135
          header.depth = fread(fileid,1,'int32');                                 %bytes 136-139
          header.fs = fread(fileid,1,'uint16');                                   %bytes 140-141
          header.pulse_id=fread(fileid,1,'uint16');                               %bytes 142-143
          header.altitude   = fread(fileid,1,'uint32');                           %bytes 144-147
          header.soundspeed = fread(fileid,1,'float32');                          %bytes 148-151
          header.mixerFreq  = fread(fileid,1,'float32');                          %bytes 152-155
          header.date.year = fread(fileid,1,'int16');                             %bytes 156-157
          header.date.day = fread(fileid,1,'uint16');                             %bytes 158-159
          header.daytime.hours = fread(fileid,1,'uint16');                           %bytes 160-161
          %Note,hour, m, secs are not to be used
          %must use millisecondsToday for better resolution. !
          header.daytime.minutes = fread(fileid,1,'uint16');                         %bytes 162-163
          header.daytime.seconds = fread(fileid,1,'uint16');                         %bytes 164-165
          header.timeBasis = fread(fileid,1,'int16');                             %bytes 166-167
          header.weight = fread(fileid,1,'int16'); %  = block floating exponent   %bytes 168-169
          header.numpulses=fread(fileid,1,'int16');                               %bytes 170-171
          header.compassHeading = fread(fileid,1,'uint16');                       %bytes 172-173
          header.compassHeading = header.compassHeading / 100.0 ;
          header.pitch = fread(fileid,1,'int16');                                 %bytes 174-175
          header.pitch = header.pitch * 180.0 / 32768.0 ;
          header.roll = fread(fileid,1,'int16');                                  %bytes 176-177
          header.roll = header.roll * 180.0 / 32768.0 ;
          header.reserved7 = fread(fileid,2,'int16');                            %bytes 178-181
          header.triggerSource = fread(fileid,1,'int16');                         %bytes 182-183
          header.markNumber = fread(fileid,1,'int16');                            %bytes 184-185
          header.posFixHours = fread(fileid,1,'int16');                           %bytes 186-187
          header.posFixMinutes = fread(fileid,1,'int16');                         %bytes 188-189
          header.posFixSeconds = fread(fileid,1,'int16');                         %bytes 190-191
          header.course = fread(fileid,1,'int16');                                %bytes 192-193
          header.speed = fread(fileid,1,'int16');                                 %bytes 194-195
          header.posFixDay = fread(fileid,1,'int16');                             %bytes 196-197
          header.posFixYear = fread(fileid,1,'int16');                            %bytes 198-199
          header.millisecondsToday = fread(fileid,1,'uint32');                    %bytes 200-203
          header.milliseconds = mod(header.millisecondsToday,1000);
          header.timeStamp = header.seconds + header.milliseconds/1e3 ;
          header.maxADCValue = fread(fileid,1,'uint16');                          %bytes 204-205
          header.reserved8 = fread(fileid,2,'uint16');                            %bytes 206-209
          header.SonarVersion = fread(fileid,6,'int8');                           %bytes 210-215
          header.sphericalCorection = fread(fileid,1,'int32');                    %bytes 216-219
          header.packetNumber = fread(fileid,1,'uint16');                         %bytes 220-221
          header.ADCDecimation = fread(fileid,1,'int16');                         %bytes 222-223
          header.reserved9 = fread(fileid,1,'int16');                             %bytes 224-225
          header.waterTemperature = fread(fileid,1,'uint16');                     %bytes 226-227
          header.layback = fread(fileid,1,'float32');                             %bytes 228-231
          header.reserved10 = fread(fileid,1,'int32');                             %bytes 232-235
          header.cableOut = fread(fileid,1,'uint16');                             %bytes 236-237
          header.reserved11 = fread(fileid,1,'int16');                            %bytes 238-239

          switch header.dataFormat
            case {0, 2, 3}    % 16 bit sampes, real only
              %Note numOfSamples should = to numSamples
              numSamples = (messageHeader.byteCount - 240)/2;  %bytes - sizeof header by 2
              temp = fread(fileid,[1,numSamples],'int16');
              sample_data = temp * 2^-header.weight ;
            case 6    % 32 Bit samples Real
              %Note numOfSamples should = to numSamples
              numSamples = (messageHeader.byteCount - 240)/4;  %bytes - sizeof header by 2
              temp = fread(fileid,[1,numSamples],'int32');
              sample_data = temp * 2^-header.weight ;
            case {1, 9}   % 16 bit IQ
              numSamples = (messageHeader.byteCount - 240)/4;  %bytes - sizeof header by 4
              temp = fread(fileid,[2,numSamples],'int16');
              %Make this [2,N] array, a complex [1x N] array
              sample_data = ( temp(1,:)  + 1i * temp(2,:)) * 2^-header.weight;
            case 7   %Complex FPoint
              numSamples = (messageHeader.byteCount - 240)/8;  %bytes - sizeof header by 4
              temp = fread(fileid,[2,numSamples],'float32');
              %Make this [2,N] array, a complex [1x N] array
              sample_data = ( temp(1,:)  + 1i * temp(2,:));
            otherwise
              %Read in the junk
              numSamples = (messageHeader.byteCount - 240)/2;  %bytes - sizeof header by 2
              sample_data = fread(fileid,[1,numSamples],'int16');
          end

          data.samples = sample_data ;   %Store one messageHeader.channel of data
          header.fsample=1/(header.sampleInterval*1e-9);  %Note granularity is 1 ns....
          return
        else
          %skip ahead in file   chew up block of data ...
          [dummy,cnt] = fread(fileid,(messageHeader.byteCount),'int8');
          if isempty(cnt) || isempty(dummy)
            messageHeader.contentType= -4;  % signal end of file, data not found
            return
          end
        end  %

      case 3000
        header.time.seconds = fread(fileid,1,'uint32');           %byte 0
        header.time.milliseconds = fread(fileid,1,'uint32') / 1e6 ;  %byte 4
        header.timeStamp = header.time.seconds + header.time.milliseconds / 1e3 ;
        header.pingNum = fread(fileid,1,'uint32');
        header.nsamps = fread(fileid,1,'uint16');
        header.channel = fread(fileid,1,'uint8');
        header.algo = fread(fileid,1,'uint8');                       %Algorithm used
        header.numPulses = fread(fileid,1,'uint8');              %byte 16
        header.pulsePhase = fread(fileid,1,'uint8');              %byte 17
        header.pulselength = fread(fileid,1,'uint16') / 1e6 ;                %byte 18-19
        header.pulsePower = fread(fileid,1,'float32'); %pulsepower       %byte 20
        header.startf = fread(fileid,1,'float32');         %byte 24
        header.stopf = fread(fileid,1,'float32');          %byte 28
        fread(fileid,1,'float32');                 %byte 32
        header.fsample = fread(fileid,1,'float32');                  %byte 36
        header.timeToFirstSample = fread(fileid,1,'uint32');      %byte 40         ! was firstSampleNo-1
        header.timeUncertainty = fread(fileid,1,'float32');                  %byte 44 timedelay uncertainty
        header.timeScaleFactor = fread(fileid,1,'float32');           %byte 48 timeScaleFactor
        %%%%%%   /2 above because we will double and fix the Delay_indexes...
        fread(fileid,1,'float32');                  %byte 52 sclfactor error in%
        header.angleScaleFactor = fread(fileid,1,'float32');                %byte 56,
        fread(fileid,1,'float32');                     %byte 60-63, Reserved
        %compute time to first return
        header.timeToBottom = fread(fileid,1,'uint32');             %byte 64, first echo
        fread(fileid,1,'uint8');                       % Rev Level of format = 2
        header.binData = fread(fileid,1,'uint8');                 %byte 69
        header.TVG = fread(fileid,1,'uint16');                      %byte 70-71
        header.swath = fread(fileid,1,'float32');        %byte 72-75
        header.binSize = fread(fileid,1,'float32');                      %byte 76-79

        %Format Rev 4

        SNRQUAL = zeros(header.nsamps,1) ;

        databuffer = fread(fileid, header.nsamps * 8,'*uchar') ;
        dataloc = 1 ;
        for lop = 1:header.nsamps
          count = 2 ; data.DelayIndex(lop) = double(typecast(databuffer(dataloc:dataloc+count-1),'uint16'));  dataloc = dataloc+count ;  %!Index error corrected 2/9/10
          count = 2 ; data.Angle(lop) = double(typecast(databuffer(dataloc:dataloc+count-1),'int16')); dataloc = dataloc+count ;
          count = 1 ; data.Amp(lop) = double(typecast(databuffer(dataloc:dataloc+count-1),'uint8')); dataloc = dataloc+count ;
          count = 1 ; data.Sigma(lop) = double(typecast(databuffer(dataloc:dataloc+count-1),'uint8')); dataloc = dataloc+count ;
          count = 1 ; data.Filter_flag(lop) = double(typecast(databuffer(dataloc:dataloc+count-1),'uint8')); dataloc = dataloc+count ;
          count = 1 ; SNRQUAL(lop)  = double(typecast(databuffer(dataloc:dataloc+count-1),'uint8')); dataloc = dataloc+count ;
        end
        %             for lop = 1:data.nsamps
        %                 data.DelayIndex(lop) = fread(fileid,1,'uint16');      %!Index error corrected 2/9/10
        %                 data.Angle(lop) = fread(fileid, 1 , 'int16');
        %                 data.Amp(lop) = fread(fileid, 1 ,'uint8');
        %                 data.Sigma(lop) = fread(fileid, 1,'uint8');
        %                 data.Filter_flag(lop) = fread(fileid, 1, 'uint8');
        %                 SNRQUAL(lop)  = fread(fileid, 1,'uint8');
        %             end

        data.TWTT = header.timeToFirstSample/1e9 + data.DelayIndex * header.timeScaleFactor ;
        data.Angle = header.angleScaleFactor * data.Angle/180*pi ;
        data.SNR = bitand(SNRQUAL,31)' ;
        data.QUAL = bitshift(SNRQUAL,-5)' ;
        messageHeader.contentType = 42 ;
        return

      case 3001 % motion from bathy processor
        header.time.seconds = fread(fileid, 1,'uint32') ;           %byte 0
        header.time.milliseconds = fread(fileid, 1,'uint32') / 1e6 ;  %byte 4
        header.timeStamp = header.time.seconds + header.time.milliseconds / 1e3 ;
        header.flags = fread(fileid, 1,'uint32') ;            %byte 8
        data.heading = fread(fileid, 1,'float32') ;               %byte 12
        data.heave = fread(fileid, 1,'float32') ;       %byte 16
        data.pitch = fread(fileid, 1,'float32') ;       %byte 20
        data.roll = fread(fileid, 1,'float32') ;         %byte 24
        data.yaw = fread(fileid, 1,'float32');                 %byte 28
        messageHeader.contentType = 43 ;
        return
      case 3002 % CTD from bathy processor
        header.time.seconds = fread(fileid, 1, 'uint32');              %byte 0
        header.time.milliseconds  = fread(fileid, 1, 'uint32') / 1e6;  %byte 4
        header.timeStamp = header.time.seconds + header.time.milliseconds / 1e3 ;
        header.flags =fread(fileid, 1, 'uint32');                     %byte 8
        data.absolutePressure = fread(fileid, 1, 'single');            %byte 12
        data.waterTemperature = fread(fileid, 1, 'single');            %byte 16
        data.salinity = fread(fileid, 1, 'single');                    %byte 20
        data.conductivity = fread(fileid, 1, 'single');                %byte 24
        data.soundSpeed = fread(fileid, 1, 'single');                  %byte 28
        data.depth = fread(fileid, 1, 'single');                       %byte 32
        messageHeader.contentType = 45 ;
        return
 
      case 3003 % altitude from bathy processor
        header.time.seconds = fread(fileid, 1, 'uint32');              %byte 0
        header.time.milliseconds  = fread(fileid, 1, 'uint32') / 1e6;  %byte 4
        header.timeStamp = header.time.seconds + header.time.milliseconds / 1e3 ;
        header.flags = fread(fileid, 1, 'uint32');                     %byte 8
        data.altitude = fread(fileid, 1, 'single');            %byte 12
        data.speed = fread(fileid, 1, 'single');            %byte 16
        data.heading = fread(fileid, 1, 'single');            %byte 16
        messageHeader.contentType = 46 ;
        return

      case 3004 % situation from bathy processor
        header.time.seconds = fread(fileid, 1,'uint32') ;             %byte 0
        header.time.milliseconds = fread(fileid, 1,'uint32') / 1e6 ;  %byte 4
        header.timeStamp = header.time.seconds + header.time.milliseconds / 1e3 ;
        header.flags = fread(fileid, 1,'uint16') ;                    %byte 8
        data.UTMzone = fread(fileid, 1,'uint16') ;                    %byte 10
        data.easthing = fread(fileid, 1,'double') ;                    %byte 12
        data.northing = fread(fileid, 1,'double') ;                   %byte 20
        data.lat = fread(fileid, 1,'double') ;                   %byte 28
        data.lon = fread(fileid, 1,'double') ;                  %byte 36
        data.speed = fread(fileid, 1,'float32');                      %byte 44
        data.heading = fread(fileid, 1,'float32');                    %byte 48
        data.height = fread(fileid, 1,'float32');                     %byte 52
        messageHeader.contentType = 44 ;
         return

      otherwise  %not a handled data type
        %skip ahead in file
        [dummy,cnt] = fread(fileid,(messageHeader.byteCount),'int8');
        if isempty(cnt) || isempty(dummy)
          messageHeader.contentType= -4;  % signal end of file, data not found
          return
        end
    end
  elseif messageHeader.byteCount > 0
    [dummy,cnt] = fread(fileid,(messageHeader.byteCount),'int8');
    if isempty(cnt) || isempty(dummy)
      messageHeader.contentType= -4;  % signal end of file, data not found
      return
    end
  end
end

