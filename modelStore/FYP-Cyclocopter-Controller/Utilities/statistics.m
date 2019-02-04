% statistics
% Gather statistics on simulation results - at the moment only standard
% deviation

% Analayse each DOF for performance, [x, y, z, phi, theta, psi]
for i = 1:length(ws)-1;
    for j = 1:6

        % Offset analysis by start_time seconds
        time_sel = actual(i, j).Time > 15;
        time = actual(i, j).Time(time_sel);

        % Interpolate demand to match number of time steps of actual
        demand_interp = interp1(demand(i, j).Time, demand(i, j).Data,...
                                time);

        err = actual(i, j).Data(time_sel) - demand_interp; %        Error

        std_deviation(i, j) = std(err); %              Standard deviation
        max_deviation(i, j) = max(abs(err)); %              Maximum error
        
    end
    
    wind(i, :) = rms(wind_speed(i).Data);
end

figure;
f1 = fit(wind(1:19, 1), std_deviation(:, 1), 'poly2');
f2 = fit(wind(1:19, 2), std_deviation(:, 2), 'poly2');
f3 = fit(wind(1:19, 3), std_deviation(:, 3), 'poly2');

plot(wind(1:19, 1), std_deviation(1:19, 1), 'k-');
hold all
plot(wind(1:19, 2), std_deviation(1:19, 2), 'k--');
plot(wind(1:19, 3), std_deviation(1:19, 3), 'k-.');
plot(f1, 'k:');
plot(f2, 'k:');
plot(f3, 'k:');
hold off
ylabel('\sigma [m]');
xlabel('Disturbance RMS Magnitude [m]');
legend('x \sigma', 'y \sigma', 'z \sigma', 'trendline');

figure;
f1 = fit(wind(1:19, 4), std_deviation(:, 4), 'poly2');
f2 = fit(wind(1:19, 5), std_deviation(:, 5), 'poly2');
f3 = fit(wind(1:19, 6), std_deviation(:, 6), 'poly2');

plot(wind(1:19, 4), std_deviation(1:19, 4), 'k-');
hold all
plot(wind(1:19, 5), std_deviation(1:19, 5), 'k--');
plot(wind(1:19, 6), std_deviation(1:19, 6), 'k-.');
plot(f1, 'k:');
plot(f2, 'k:');
plot(f3, 'k:');
hold off
ylabel('\sigma [rad]');
xlabel('Disturbance RMS Magnitude [rad]');
legend('\phi \sigma', '\theta \sigma', '\psi \sigma', 'trendline');