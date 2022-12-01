try
  load('fpath.mat','fpath')
  [filename,fpath]=uigetfile([fpath '/*.jsf'], 'Which file to process?'); %open file and assign handle
catch
  [filename,fpath]=uigetfile('*.jsf', 'Which file to process?'); %open file and assign handle
end
save('fpath.mat','fpath')
fp = fopen([fpath,filename],'r');

PoBathyCtr = 1 ;
StBathyCtr = 1 ;
PortRange = NaN(5000,5000) ;
PortAngle = NaN(5000,5000) ;
PortAmp = NaN(5000,5000) ;
PortSig = NaN(5000,5000) ;
PortMaxSound = -1 ;

StbdRange = NaN(5000,5000) ;
StbdAngle = NaN(5000,5000) ;
StbdAmp = NaN(5000,5000) ;
StbdSig = NaN(5000,5000) ;
StbdMaxSound = -1 ;
ip = 1;
pitch = NaN(1,5000) ;
roll = NaN(1,5000) ;
heave = NaN(1,5000) ;

cs = 1530 ;
figureOffset = 10 ;

while 1 == 1
  [mH, data, header] = readJSF_V3_Bathy(fp) ;

  if mH.contentType < 1 % should check for cause of error to display information about break condition
    break
  end

  if mH.contentType == 42 % bathy data
    df = find(data.Filter_flag == 0);
    if header.channel == 0 % port
      PortRange(PoBathyCtr, 1:length(df)) = data.TWTT(df) .* cs / 2.0;
      PortAngle(PoBathyCtr,  1:length(df)) = -data.Angle(df) ;
      PortAmp(PoBathyCtr,  1:length(df)) = data.Amp(df) ;
      PortSig(PoBathyCtr,  1:length(df)) = data.Sigma(df) ;
      PortHeader(PoBathyCtr) = header ;
      if size(df,2) > PortMaxSound
        PortMaxSound = size(df,2) ;
      end
      PoBathyCtr = PoBathyCtr + 1 ;
      if ~mod(PoBathyCtr,100)
        fprintf('.')
      end
    elseif header.channel == 1 % Stbd
      StbdRange(StBathyCtr, 1:length(df)) = data.TWTT(df) .* cs / 2.0;
      StbdAngle(StBathyCtr,  1:length(df)) =  data.Angle(df)  ;
      StbdAmp(StBathyCtr,  1:length(df)) = data.Amp(df) ;
      StbdSig(StBathyCtr,  1:length(df)) = data.Sigma(df) ;
      StbdHeader(StBathyCtr) = header ;
      if size(df,2) > StbdMaxSound
        StbdMaxSound = size(df,2) ;
      end

      StBathyCtr = StBathyCtr + 1 ;

    end
    if ip ==1
      slsHeader = header;
    end
  elseif mH.contentType == 43 %Bathy Motion Data
    pitch(ip) = data.pitch;
    roll(ip) = data.roll;
    heave(ip) = data.heave;
    ip = ip+1;
    if ~mod(ip,100)
      fprintf('.')
    end
  end
end
fprintf('\n')

BathyCtr = min(PoBathyCtr,StBathyCtr) - 1;

PortRange = PortRange(1:BathyCtr,1:PortMaxSound) ;
PortAngle = PortAngle(1:BathyCtr,1:PortMaxSound) ;
PortAmp = PortAmp(1:BathyCtr,1:PortMaxSound) ;
PortSig = PortSig(1:BathyCtr,1:PortMaxSound) ;

StbdRange =  StbdRange(1:BathyCtr,1: StbdMaxSound) ;
StbdAngle =  StbdAngle(1:BathyCtr,1: StbdMaxSound) ;
StbdAmp =  StbdAmp(1:BathyCtr,1: StbdMaxSound) ;
StbdSig =  StbdSig(1:BathyCtr,1: StbdMaxSound) ;

PortX = PortRange.*sin(PortAngle);
PortY = repmat((1:size(PortX,1))',1,size(PortX,2)) ;
StbdX = StbdRange.*sin(StbdAngle);
StbdY = repmat((1:size(StbdX,1))',1,size(StbdX,2)) ;

PortZ = -PortRange.*cos(PortAngle);
StbdZ = -StbdRange.*cos(StbdAngle);

figure(1+figureOffset)
clf
bathyX = ([fliplr(PortX) zeros(BathyCtr,1) StbdX]);
bathyZ = ([fliplr(PortZ) zeros(BathyCtr,1) StbdZ]);
imagesc(bathyZ)
caxis([min(bathyZ(bathyZ ~= 0)),min(0,max(bathyZ(bathyZ ~= 0)))])
title(['Bathymetry  ' filename],'interpreter','none')
axis xy
colormap (jet)
colorbar

figure(2+figureOffset)
amp = ([fliplr(PortAmp) zeros(BathyCtr,5) StbdAmp]);
imagesc(amp)
caxis([min(amp(amp ~= 0)), max(amp(amp ~= 0))])
title(['Amplitude  ' filename],'interpreter','none')
axis xy
colormap(gray)
colorbar

figure(3+figureOffset)
subplot(3,1,1);
plot(roll)
title('Roll')
subplot(3,1,2);
plot(pitch)
title('Pitch')
subplot(3,1,3);
plot(heave)
title('Heave')



