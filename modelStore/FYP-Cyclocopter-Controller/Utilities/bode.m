j = 1; % Select z data set [x, y, z, phi, theta, psi]

num = 1:length(ws(1:end-2));

for i = num % Loop through each data set
    % Offset analysis by start_time seconds
    timesel = actual(i, j).Time > 15 - mod(15, 2*pi/ws(i)) + 2*pi/ws(i);
    time = actual(i, j).Time(timesel);

    % Interpolate demand to match number of time steps of actual
    demand_interp = interp1(demand(i, j).Time, demand(i, j).Data,...
                            actual(i, j).Time);
    
    % Set prominence to 80% of maximum height
    prominence_act = 0.1 * max(actual(i, j).Data(timesel));
    prominence_dem = 0.1 * max(demand_interp(timesel));
    
    % Find local maxima for output curve, min height 0 and 80% prominence
    [pks_act, locs_act] = findpeaks(actual(i, j).Data,...
                                    'MinPeakHeight', -0.2,...
                                    'MinPeakProminence', prominence_act);
    locsel_act = locs_act > find(timesel, 1, 'first');
    % Find local maxima for demand curve
    [pks_dem, locs_dem] = findpeaks(demand_interp,...
                                    'MinPeakHeight', 0,...
                                    'MinPeakProminence', prominence_dem);
    locsel_dem = locs_dem > find(timesel, 1, 'first');

    % Match number of found maxima for output and demand
    len_act = length(locs_act(locsel_act));
    len_dem = length(locs_dem(locsel_dem));

    if len_act > len_dem
        len = len_dem;
    else
        len = len_act;
    end
    
    lensel = 1:len;

    % Get times and values of points to analyse
    act_time = actual(i, j).Time(locs_act(locsel_act));
    act_val  = pks_act(locsel_act);

    dem_time = actual(i, j).Time(locs_dem(locsel_dem));
    dem_val  = pks_dem(locsel_dem);

    % Calculate magnitude of output in dB
    mag(i)       = 10 * log10( mean(act_val(lensel)) /...
                               mean(dem_val(lensel)));
                           

    % Calculate phase angle in degrees
    phase_sec    = mean(dem_time(lensel) - act_time(lensel));
    phase_deg(i) = (360 / (2*pi)) * (phase_sec * ws(i));

% plot(act_time(lensel), act_val(lensel), 'kx');
% hold all
% plot(time, actual(i, j).Data(timesel));
% 
% plot(dem_time(lensel), dem_val(lensel), 'kx');
% plot(time, demand_interp(timesel));
% 
% hold off
end

%Plot Bode diagram
subplot(2, 1, 1);
semilogx(ws(num), mag, 'k');
ylabel('Magnitude [dB]');
xlabel('Frequency [rad/s]');
ylim([-25, 2]);

subplot(2, 1, 2);
semilogx(ws(num), phase_deg, 'k');
ylabel('Phase [degrees]');
xlabel('Frequency [rad/s');
ylim([-360, 45]);