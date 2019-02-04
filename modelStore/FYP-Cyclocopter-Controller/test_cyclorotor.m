numPoints = 1000; %                      Number of eccentric points to test
omega     = 1; %                      Cyclorotor angular velocity (rad/s)
eta       = [0 0 0]; %  Cyclorotor linear velocity (w.r.t body frame) (m/s)

% Set up holding matricies
F_p = zeros(3, numPoints);
F   = zeros(3, numPoints);

% Generate eccentric points to test
i   = linspace(0, 2*pi, numPoints);

% Get force vectors of cyclorotor at i eccentric points
for j = 1:numPoints
    tic
    [F(:, j), ~, F_p(:, j)] = Cyclorotor(omega, i(j), eta);
    time(j) = toc;
end

% Plot force components and magnitude
plot( i, F(1, :), '-k' );
hold all
plot( i, F(2, :), ':k' );
plot( i, F(3, :), '--k' );
plot( i, sqrt(F(3, :).^2 + F(1, :).^2), '-.k' );
plot( i, -sqrt(F(3, :).^2 + F(1, :).^2), '-.k' );
hold off

legend('F_x', 'F_y', 'F_z', '|F|', 'Location', 'southeast');
xlabel('Eccentric Point Rotational Displacement [rad]');
ylabel('Force [N]');


% Plot force components pre and post indudced velocity calculations
figure;
plot( i, F(1, :), '-k' );
hold all
plot( i, F_p(1, :), '--k' );
plot( i, F(3, :), '-k' );
plot( i, F_p(3, :), '--k' );
hold off

legend('F', 'F_{(pre)}', 'Location', 'southeast');
xlabel('Eccentric Point Rotational Displacement [rad]');
ylabel('Force [N]');


% Calculate force and torque speed curves
F_v = zeros(3, numPoints);
t_v = zeros(3, numPoints);

for j = 1:numPoints
    [F_v(:, j), t_v(:, j), ~] = Cyclorotor( j*2, 0.2, [0 0 0]);
end

figure;
plot((1:numPoints).*2, F_v(1, :), '-k');
hold all
plot((1:numPoints).*2, F_v(3, :), '--k');
plot((1:numPoints).*2, t_v(2, :), '-.k');
hold off

legend('F_x', 'F_z', 'Motor Torque', 'Location', 'northwest');
xlabel('\omega [rad/s]');
ylabel('Force [N] / Torque[Nm]');
