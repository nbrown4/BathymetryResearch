try
  load('fpath.mat','fpath')
  [filename,fpath]=uigetfile([fpath '/*.jsf'], 'Which file to process?'); %open file and assign handle
catch
  [filename,fpath]=uigetfile('*.jsf', 'Which file to process?'); %open file and assign handle
end
save('fpath.mat','fpath')
fp = fopen([fpath,filename],'r');

gotNewPing = 0 ;
while 1 == 1
    [mH, data, header] = readJSF_V3_Bathy(fp) ;
    if mH.channel == 0
        gotNewPing = 1 ;
    end
    if mH.contentType == 1 && gotNewPing == 1 
        stave(mH.channel+1,:) = data.samples ;
        if mH.channel == 19
            break
        end
    end
end

portsamples = stave(1:2:end,:) ;
stbdsamples = flipud(stave(2:2:end,:)) ;

dr = 0.5 * header.soundspeed / header.fsample ; % sample resolution in meters
bottom = round(header.altitude/1000 / dr) ; % seabed start in the time series

dphs = mean(angle(conj(portsamples(1:9,:)) .* portsamples(2:10,:))) ; % average phase difference between staves
figure(1)
hold off
plot(dphs), hold on
plot(dphs(1:bottom),'r')
xlabel('sample number')
ylabel('phase difference (rad.)')
