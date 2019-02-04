%Script to produce a lookup table for the cyclorotor

breakpoint_omega   = linspace(0, 10000 * (2*pi/60), 200); % Spaced every 50 RPM
breakpoint_epsilon = linspace(0, 2*pi, 360); % Spaced every 1 degrees

cyclorotor_lookup = zeros(length(omega), length(epsilon), 6);

for i = 1:length(omega)
    for j = 1:length(epsilon)
        [F, t] = Cyclorotor(omega(i), epsilon(j), [0 0 0]);
        cyclorotor_lookup(i, j, :) = [F; t];
    end
end

save('cyclorotor_lookup', 'cyclorotor_lookup', 'breakpoint_omega', 'breakpoint_epsilon');