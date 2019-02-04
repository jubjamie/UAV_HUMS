%-----------------------------------------------------------------------%
% Cyclocopter_body
% Description: Cylocopter body model, a new set of state derivatives is
%              calculated based on the previous set of states. These are
%              then resolved using simulink to get the new set of states.
%              All Force and Torque arguments w.r.t to body frame
% Arguments: Fc1        = Left cyclorotor force vector [3x1] (N)
%            tc1        = Left cyclorotor torque vector [3x1] (Nm)
%            Fc2        = Right cyclorotor force vector [3x1] (N)
%            tc2        = Right cyclorotor torque vector [3x1] (Nm)
%            Fp         = Balancing prop force vector [3x1] (N)
%            tp         = Balancing prop torque vector [3x1] (Nm)
%            oldStates  = Previous body states [12x1] (N, Nm)
% Returns:   xi_dd      = Linear acceleration states w.r.t inertial frame
%                         [3x1] (m/s^2)
%            omega_d    = Angular acceleration states w.r.t body frame  
%                         [3x1] (rad/s^2)
%            psi_d      = Angular velocity states w.r.t inertial frame 
%                         [3x1] (rad/s)
%-----------------------------------------------------------------------%
function [xi_dd, omega_d, eta_d] = CyclocopterBody(Fc1, tc1, Fc2, tc2,...
                                                Fp, tp, oldStates)

%----------------------------- Constants -------------------------------%
g = 9.81; % Gravity (m/s^2)

m = 0.26; % Aircraft Mass (kg)

L1 = 0.245; % Origin to rear prop distance (m)
L2 = 0.109; % Origin to center of cyclorotor (m)
%L3 = 0.005; % Origin to CoM (m)

% Aircraft Inertia (Kg m/s^2)
Ixx = 13.3e-3; 
Iyy = 10.2e-3; 
Izz = 5.2e-3;

% Aerodynamic drag
Ax = 0;%0.25; 
Ay = 0;%0.25; 
Az = 0;%0.25;


%----------------------------- Enumeration -----------------------------%
% Seperate out old states into the four sets for linear and angular 
% position and velocity respectively
xi_d   = oldStates(1:3);
%xi     = oldStates(4:6)
omega  = oldStates(7:9);
eta    = oldStates(10:12);


% Seperate out angular displacements
a = eta(1); %                                                  phi (roll)  
b = eta(2); %                                               theta (pitch)
c = eta(3); %                                                   psi (yaw) 


%--------------------------- Helper Matrices ---------------------------%
W_n_inv = [1  0          -sin(b); %   Angular velocity Jacobian (inverse)
           0  cos(a)   cos(b) * sin(b);
           0 -sin(a)   cos(b) * cos(a) ];

% Rotational matrix, BF to IF, ZYX Euler
R = [cos(c)*cos(b), cos(c)*sin(b)*sin(c) - sin(c)*cos(a),...
     cos(c)*sin(b)*cos(a) + sin(c)*sin(a);
     sin(c)*cos(b), sin(c)*sin(b)*sin(a) + cos(c)*cos(a)...
     sin(c)*sin(b)*cos(a) - cos(c)*sin(a);
     -sin(b), cos(b)*sin(a), cos(b)*cos(a)];


I   = [Ixx 0   0; %                                Inertial tensor matrix
       0   Iyy 0;
       0   0   Izz ];

G   = [0; 0; -g]; %                                        Gravity matrix

% Moment transformation Matrices
T_c = [0 0 1; %                                                Cyclorotor
       0 0 0;
       1 0 0];

T_p = [0 0 0; %                                            Balancing prop
       0 0 1;
       0 0 0];

Ad  = [Ax  0  0; %                                            Drag matrix
       0   Ay 0;
       0   0  Az];
 

%------------------------- Calculate New States ------------------------%
Fd      = (1/m) * Ad * R * xi_d; %                       Aerodynamic drag

% Linear acceleration from F = m * xi_dd
xi_dd   = G + (1/m) * R * (Fc1 + Fc2 + Fp) - Fd;

% Torques
t_m     = tc1 + tc2 + tp; %                                 Motor torques
t_F     = (T_c * (Fc2 - Fc1) * L2) + (T_p * Fp * L1); %           Moments
    
t_b     = t_m + t_F; %                                            Sum all

% Angular acceleration from Eulers equation for rigid body dynamics
omega_d = I \ (t_b  - cross(omega, I * omega));
eta_d   = W_n_inv * omega;

%--------------------------------- EOF ---------------------------------%
