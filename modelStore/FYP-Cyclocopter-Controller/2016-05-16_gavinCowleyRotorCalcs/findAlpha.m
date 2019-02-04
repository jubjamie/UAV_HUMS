% loops to find a given physical alpha using cyclocopter_power.m

set(0,'defaultFigureVisible','off');

thetaMax=0.1; % incidence start point (AoA)
cyclocopter_power;

close all;
while max(max(pitch))<10, % physical alpha target
    close all;
    thetaMax=thetaMax+.1 % incidence alpha step size
    cyclocopter_power;
end

set(findobj(0,'type','figure'),'visible','on');
set(0,'defaultFigureVisible','on');
