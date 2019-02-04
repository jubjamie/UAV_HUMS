% Scripts adapted from work by Jon du Bois by Freddie Sherratt
% [2017-03-20]

% N.b All forces and velocities are with respect to the body frame

%-----------------------------------------------------------------------%
% Cyclorotor 
% Description: Script to estimate cyclocopter lift and power from very 
%              simple theory Jon du Bois, University of Bath,  
%              2014. updated May 2016.
% Inputs:      omega     = Cyclorotor angular velococity (rad/s)
%              epsilon   = Ecentric point angular displacement (rad)
%              eta_d     = Cyclorotor linear velocity [3x1] (m/s)
% Paramaters:  tolerance = Iteration break percentage point
% Ouput:       F_c       = Force vector [3x1] (N)
%              t_c       = Torque vector [3x1] (Nm)
%              F_c_pre   = Force vector before induced velocity
%              t_c_pre   = Torque vector before induced velocity
%-----------------------------------------------------------------------%
function [F_c, t_c] = Cyclorotor(omega, epsilon, eta_d)
%function [F_c, t_c, F_c_pre] = Cyclorotor(omega, epsilon, eta_d)


    % Force and torque vector placeholders
    F_c     = [0; 0; 0];
    t_c     = [0; 0; 0];
    %F_c_pre     = [0; 0; 0];

    % If the cyclorotor is spinning
    if omega > 0
        
        %-------------------------- PARAMATERS -------------------------%
        tolerance  = 0.01; %                         Accuracy break point
        numPoints  = 200; %                     Numbers of azimuth points
        numBlades  = 4; %                                Number of blades

        r          = 0.069; %                            Rotor radius (m)
        chord      = 0.040; %                          Aerofoil chord (m)
        span       = 0.100; %                           Aerofoil span (m)
        rho        = 1.225; %                        Air density (kg/m^3)
        d          = 0.014; %Distance between aerofoil link positions (m)
        l          = 0.070; %                   Length of control arm (m)
        e          = 0.007; %               Eccentric point magnitude (m)

        A          = span * chord; %                      Wing area (m^2)
        v          = omega * r; %               Tangential velocity (m/s)
        planformA  = r * 2 * span; %                  Planform area (m^2)
        
        % Constants
        PI_D_TWO = pi / 2;
        PI_M_TWO = 2 * pi;
        RHO_M_PLAN = rho * planformA;
        
        %---------------------------------------------------------------%

        % Generate linearly spaced vector of azimuth point for 1 blade
        az       = zeros(numBlades, numPoints);
        az(1, :) = linspace(0, PI_M_TWO, numPoints);

        % Create additional blades
        for i = 2:numBlades
            az(i, :) = mod(az(i - 1, :) + PI_M_TWO /...
                       numBlades, PI_M_TWO);
        end

        % Angle of Incidence (AoI)
        theta = getAoI(az, epsilon, r, d, l, e);

        % Aerofoil force at each azimuth point
        [cl, cd] = getLiftDrag(theta);
        
        % L, D coefficient
        LD_coeff = 0.5 * rho * A .* v^2;

        % Lift & drag relative to AoA (angle of attack)
        L = LD_coeff .* cl;
        D = LD_coeff .* cd;
         
        % Force and torque vectors ignoring induced and forward velocity
        [FxT, FyT, ~, arg_F] = getFVec(az, L, D, r);
        
        FyTm = mean(FyT);
        FxTm = mean(FxT);
        
        % Pre induced velocity force vector
        %F_c_pre = [FxTm; 0;        FyTm];
        
        % Induced velocity (from T = rho * A * 2 * Vi^2  
        %=> Vi = sqrt( T / ( rho * A * 2 ) )
        Vi = sqrt( sqrt(FyTm^2 + FxTm^2) / (2 * RHO_M_PLAN) );
        
        %---------------------------------------------------------------%
        % Factor in the induced velocity, Vi
        %---------------------------------------------------------------%
        doneHere = false;

        % Loop here until accuracy achieved
        while ~doneHere 
            
            % Sum induced velocity vector components
            vx = Vi * cos(arg_F) - v * sin(az) + eta_d(1);
            vy = Vi * sin(arg_F) + v * cos(az) + eta_d(3);

            % Difference between AoI and AoA
            phi = atan2(vy, vx) - (az + PI_D_TWO);
            
            % L, D coefficient
            LD_coeff = 0.5 * rho * A .* ( vx.^2 + vy.^2 );

            % Lift & drag relative to AoI (Angle of Incidence)
            La = LD_coeff .* cl; 
            Da = LD_coeff .* cd;

            % Lift & drag relative to tangential velocity
            L = Da .* sin( phi ) + La .* cos( phi ); 
            D = Da .* cos( phi ) - La .* sin( phi );

            [FxT, FyT, MT, arg_F] = getFVec(az, L, D, r);
            
            % Mean Forces
            FyTm = mean(FyT);
            FxTm = mean(FxT);
            
            % Downdraft velocity
            Vi2 = sqrt( sqrt( FyTm^2 + FxTm^2 ) / (2 * RHO_M_PLAN) );

            % Break out of loop when specified tolerance achieved
            if ( abs(Vi - Vi2) / Vi ) < tolerance
                doneHere = true;

                % Produce return force and torque vectors for all blades
                F_c = [FxTm; 0;        FyTm];
                t_c = [0;    mean(MT); 0   ];
            end

            Vi = Vi2;
        end

    end


%-----------------------------------------------------------------------%
% getLiftDrag
% Description: Thin aerofoil theory approximation to local lift 
%              coefficient. Slightly bodgy estimate of local drag 
%              coefficient based on NACA0012 at Reynolds number of 
%              100,000. I hope to improve on the options available here.
% Arguments:   alpha = Angle of Attack (rad)
% Returns:     cl    = lift coefficient
%              cd    = drag coefficient
%-----------------------------------------------------------------------%
function [cl,cd] = getLiftDrag(alpha)
    % To do:
    % - add tip/downwash effects due to AR, and maybe span efficiency 
    %   factor? (new function perhaps? keep local cl and alpha_eff here?)
    % - include option for cl0 for cambered aerofoils?
    % - improve options for cd calculation: other Re nums, aerofoils

    % assume thin aerofoil theory for cl
    cl = 2 * pi * alpha;

    % using very approx. cd for NACA0012 from airfoiltools.com, 
    % Re=100,000 (see screenshot, orange line is Re=100,000; blue line is  
    % Re=50,000; dirty orange is Re=1,000,000)
    cd = 0.015 + 0.03 * cl.^2;


%-----------------------------------------------------------------------%
% getAoI
% Description: Calculate angle of incidence for each azimuth point 
%              provided based on the ecentric point angle
% Arguments:   alpha   = vector of azimuth points
%              epsilon = ecentric point angle
%              r       = Rotor radius  
%              d       = Distance between aerofoil link positions
%              l       = Length of control arm
%              e       = Eccentric point magnitude  
% Returns:     alpha   = aparent angle of attack
%-----------------------------------------------------------------------%
function [theta] = getAoI(az, epsilon, r, d, l, e)

    PI_D_TWO = pi / 2;
    
    a  = sqrt(e^2 + r^2 - 2*e*r * cos(az + epsilon + PI_D_TWO));

    lambda_1 = asin(cos(az + epsilon) * e./a);

    lambda_2 = acos((a.^2 + d^2 - l^2)./(2 .* a*d));

    theta = PI_D_TWO - lambda_1 - lambda_2; %                            AoA


%-----------------------------------------------------------------------%
% getFVec
% Description: Calculate the cyclorotor force vector and moment
% Arguments:   v     = Aerofoil velocity
%              az    = Azimuth angle
%              L     = Lift
%              D     = Drag
%              rho   = Air density
%              A     = Wing area
%              r     = Rotor radius
% Returns:     Fx    = Force in x
%              Fy    = Force in y
%              M     = Moment
%              arg_F = Force vector argument
%-----------------------------------------------------------------------%
function [Fx, Fy, M, arg_F] = getFVec(az, L, D, r)
    
    % Axle forces
    Fx  = L .* cos(az) + D .* sin(az); %            Horizontal component
    Fy  = L .* sin(az) - D .* cos(az); %              Vertical component
    M   = -D * r; %                                               Torque
    
    arg_F = atan2(Fy, Fx); %                Get argument of force vector
    
    Fx = sum(Fx);
    Fy = sum(Fy);
    M  = sum(M);

%---------------------------------EOF-----------------------------------%
