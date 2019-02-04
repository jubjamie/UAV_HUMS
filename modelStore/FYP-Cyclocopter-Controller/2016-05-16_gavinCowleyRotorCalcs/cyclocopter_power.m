% script to estimate cyclocopter lift and power from very simple theory
% Jon du Bois, University of Bath, 2014
% updated May 2016 - trying numbers from Gavin's design
% this is a fork from Rob Worthing's calcs - use that one for development
% NB this doesn't have the right numbers in yet [2016-05-16]

% To do:
% - merge "specify pitch" version into this one to ensure it iterates to
%   find the induced velocity even when called from findAlpha()
% - change all the nomenclature in here so it actually makes sense
% - migrate a lot of the functionality into separate functions and check
%   rigour in the process.
% - Eventually see ifsome sort of multiple-stream-tube approach can be
%   taken

% angular speed etc.
omega=100;%1500/60*2*pi;
r=0.1;
v=omega*r;
chord=0.04;
span=0.1;
A=span*chord;
rho=1.225;


% assume pitch variation is sinusoidal with azimuth
if length(dbstack)<=1||~exist('thetaMax','var'),
    thetaMax=1; % max theta in degrees
end
az=linspace(0,2*pi,1001);
theta=thetaMax*sin(az);

% thin aerofoil theory for local flow
[cl,cd]=getLiftDrag(theta);

% plot results so far
figure;
subplot(3,1,1);
plot(az,theta);
xlabel('azimuth (rad)');
ylabel('theta (deg)');
title('aerofoil forces');
subplot(3,1,2);
plot(az,cd);
xlabel('azimuth (rad)');
ylabel('Cd');
subplot(3,1,3);
plot(az,cl);
xlabel('azimuth (rad)');
ylabel('Cl');

% aerofoil forces
L = 1/2 * rho * A * v^2 * cl;
D = 1/2 * rho * A * v^2 * cd;

% aerofoil forces (4 blades)
az2=az;
az2(2,:)=mod(az2+2*pi/4,2*pi);
az2(3,:)=mod(az2(2,:)+2*pi/4,2*pi);
az2(4,:)=mod(az2(3,:)+2*pi/4,2*pi);
theta2=thetaMax*sin(az2);
[cl2,cd2]=getLiftDrag(theta2);
L2 = 1/2 * rho * A * v^2 * cl2;
D2 = 1/2 * rho * A * v^2 * cd2;
figure;
subplot(3,1,1);
plot(az,theta2.','.');
xlabel('azimuth (rad)');
ylabel('theta (deg)');
title('aerofoil force coeffs (4 blades)');
subplot(3,1,2);
plot(az,cd2.','.');
xlabel('azimuth (rad)');
ylabel('Cd');
subplot(3,1,3);
plot(az,cl2.','.');
xlabel('azimuth (rad)');
ylabel('Cl');

% axle forces (4 blades)
Fx=L2.*cos(az2)+D2.*sin(az2);
Fy=L2.*sin(az2)-D2.*cos(az2);
M=-D2*r;
figure;
subplot(3,1,1);
plot(az,Fx.');
xlabel('azimuth (rad)');
ylabel('Fx');
title('axle forces (4 blades)');
subplot(3,1,2);
plot(az,Fy.');
xlabel('azimuth (rad)');
ylabel('Fy');
subplot(3,1,3);
plot(az,M.');
xlabel('azimuth (rad)');
ylabel('Moment');

% axle forces (total)
FxT=sum(Fx);
FyT=sum(Fy);
MT=sum(M);
figure;
subplot(3,1,1);
plot(az,FxT.');
xlabel('azimuth (rad)');
ylabel('Fx');
title('axle forces (total)');
subplot(3,1,2);
plot(az,FyT.');
xlabel('azimuth (rad)');
ylabel('Fy');
subplot(3,1,3);
plot(az,MT.');
xlabel('azimuth (rad)');
ylabel('Moment');

% power
pow=-MT*omega; % calculated from aerofoil drag
planformA=r*2*span;
V=(mean(FyT)/rho/planformA).^.5; % downdraft velocity (from F=mdot*V=rho*A*V*V)
pow(2,:)=FyT.*V; % calculated from air flow through planform area
figure;
plot(az,pow.');
xlabel('azimuth (rad)');
ylabel('power (Watts)');
legend('from aerofoil drag','from lift & planform area');

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%5
% OK, so now let's factor in the induced velocity, Vi. (i.e. the downdraft, V, calculated above)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%5

donehere=false;
while ~donehere
% aerofoil forces (4 blades)
v3=((v+V*cos(az2)).^2 + (V*sin(az2)).^2).^.5;                % magnitude of apparent velocity
apparentTheta=atan( (V*sin(az2)) ./ (v+V*cos(az2)) )*180/pi; % reduction of theta due to induced velocity
theta3=thetaMax*sin(az2)-apparentTheta; % account for Vi in angle of attack (AoA)
theta3=theta3+apparentTheta;            % ... but assume it's accounted for in the control as well
pitch=theta3+apparentTheta;             % ... and this is then the actual pitch of the aerofoil relative to the tangent
[cl3,cd3]=getLiftDrag(theta3);
L3a = 1/2 * rho * A * v3.^2 .* cl3; % lift & drag relative to AoA
D3a = 1/2 * rho * A * v3.^2 .* cd3;
L3b = L3a .* cos(apparentTheta*pi/180) - D3a .* sin(apparentTheta*pi/180); % lift & drag relative to tangential velocity
D3b = D3a .* cos(apparentTheta*pi/180) + L3a .* sin(apparentTheta*pi/180);
figure;
subplot(5,1,1);
plot(az,pitch.');
xlabel('azimuth (rad)');
ylabel('pitch (deg)');
title('Incl. Vi : aerofoil force coeffs (4 blades)');
subplot(5,1,2);
plot(az,theta3.');
xlabel('azimuth (rad)');
ylabel('theta (deg)');
subplot(5,1,3);
plot(az,v3.');
xlabel('azimuth (rad)');
ylabel('apparent vel');
subplot(5,1,4);
plot(az,cd3.');
xlabel('azimuth (rad)');
ylabel('Cd');
subplot(5,1,5);
plot(az,cl3.');
xlabel('azimuth (rad)');
ylabel('Cl');
%%%
figure;
subplot(4,1,1);
plot(az,L3a.');
xlabel('azimuth (rad)');
ylabel('Lift (rel AoA)');
title('Incl. Vi : aerofoil forces (4 blades)');
subplot(4,1,2);
plot(az,D3a.');
xlabel('azimuth (rad)');
ylabel('Drag (rel AoA)');
subplot(4,1,3);
plot(az,L3b.');
xlabel('azimuth (rad)');
ylabel('Lift (rel tangent)');
subplot(4,1,4);
plot(az,D3b.');
xlabel('azimuth (rad)');
ylabel('Drag(rel tangent)');

% axle forces (4 blades)
Fx3=L3b.*cos(az2)+D3b.*sin(az2);
Fy3=L3b.*sin(az2)-D3b.*cos(az2);
M3=-D3b*r;
figure;
subplot(3,1,1);
plot(az,Fx3.');
xlabel('azimuth (rad)');
ylabel('Fx');
title('Incl. Vi : axle forces (4 blades)');
subplot(3,1,2);
plot(az,Fy3.');
xlabel('azimuth (rad)');
ylabel('Fy');
subplot(3,1,3);
plot(az,M3.');
xlabel('azimuth (rad)');
ylabel('Moment');

% axle forces (total)
FxT3=sum(Fx3);
FyT3=sum(Fy3);
MT3=sum(M3);
figure;
subplot(3,1,1);
plot(az,FxT3.');
xlabel('azimuth (rad)');
ylabel('Fx');
title('Incl. Vi : axle forces (total)');
subplot(3,1,2);
plot(az,FyT3.');
xlabel('azimuth (rad)');
ylabel('Fy');
subplot(3,1,3);
plot(az,MT3.');
xlabel('azimuth (rad)');
ylabel('Moment');

max(mean(FxT3))

% power
pow=-MT3*omega; % calculated from aerofoil drag
planformA=r*2*span;
V3=(mean(FyT3)/rho/planformA).^.5; % downdraft velocity (from F=mdot*V=rho*A*V*V)
pow(2,:)=FyT3.*V3; % calculated from air flow through planform area
figure;
plot(az,pow.');
xlabel('azimuth (rad)');
ylabel('power (Watts)');
legend('from aerofoil drag','from lift & planform area');
title(['Incl. Vi=' num2str(V) ' (new Vi=' num2str(V3) ')']);
% NB you could iterate here until V==V3 if you wanted more accurate
% results

if length(dbstack)<=1, % permits looping in other code without looping this one too (bit of a hack)
    disp(['induced velocity error is ' num2str(abs(V-V3)/V*100) '%. Any key to continue iterations (Ctrl-C stops)']);
    pause;
    close all;
    V=V3
else
    donehere=true;
end
end
