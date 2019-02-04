%Tested in 5% increments
throttle = 0:5:100;

% Motor speed [RPM]
RPM = [0, 0, 0, 3150, 4200, 5080, 6140, 7000, 7700, 8450, 9280, 10000,...
       10660, 11000, 11600, 12300, 12850, 13400, 13900, 14300, 14300];
   
% Motor thrust [grams]
thrust_g = [0, 0, 0, 2, 5.5, 12, 17, 22, 27, 32, 40, 45.5, 52, 55, 61,...
           70, 74, 85, 90.5, 95, 95];

% Battery voltage [Volts]
V = [12.28, 12.28, 12.28, 12.26, 12.24, 12.22, 12.2, 12.16, 12.13,...
     12.09, 12.04, 11.99, 11.93, 11.87, 11.8, 11.5, 11.48, 11.46,...
     11.46, 11.46, 11.42];
 
% Battery current [Amps]
I = [0.11, 0.11, 0.11, 0.25, 0.33, 0.42, 0.57, 0.74, 0.89, 1.08, 1.32...
     1.57, 1.85, 2.07, 2.32, 2.72, 3.00, 3.47, 3.83, 4.18, 4.2];

% Motor angular velocity [rad/s]
omega = RPM .* (2 * pi / 60);

%Electrical power [W] into motor - remove current draw with 0 throttle
P_elec = V .* (I - I(1));

%Assuming 85% efficiency
P_mech = P_elec .* 0.85;

%Torque = power / angular velocity [Nm]
t = P_mech ./ omega;

%Thrust [N]
thrust = thrust_g .* (9.81 * 1e-3);

% Design controller for linera RPM and then add conversion from RPM to
% non-linear throttle output
f1 = fit(throttle', RPM', 'poly2');
plot(f1, throttle, RPM);
xlabel('throttle [%]');
ylabel('Motor angular velocity [RPM]');
c1 = coeffvalues(f1);

figure;
f2 = fit(RPM(~isnan(t))', t(~isnan(t))', 'poly2');
plot(f2, RPM, t);
xlabel('Motor angular velocity [RPM]');
ylabel('Torque [Nm]');
c2 = coeffvalues(f2);

figure;
f3 = fit(RPM', thrust', 'poly2');
plot(f3, RPM, thrust);
xlabel('Motor angular velocity [RPM]');
ylabel('Thrust [N]');
c3 = coeffvalues(f3);

