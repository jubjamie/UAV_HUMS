%-----------------------------------------------------------------------%
% param_sweep
% Performs parametric sweep of simulink models - script is not generic
% and must be addapted for each test. Will take the four the variables 
% sent to the worksapce and seperate them out into two more usable 
% variables "demand" and "actual"
%-----------------------------------------------------------------------%
% Select model to test
model_sel = 1; %                         0 = cyclotcopter, 1 = quadcopter

% Cyclocopter
if model_sel == 0
    mdl = 'cyclocopter'; %            File name of simulink model to test
    simBlock = 'Cyclocoper Model'; %             Simulink block to change
    simVar   = 'ws'; %                           Block variable to update
    ws = linspace(0, 4.5, 20); %                     Winds speeds to test

% Quadcopter
elseif model_sel == 1
    mdl = 'quad';
    simBlock = 'Quadcopter Model';
    simVar   = 'ws';
    ws = linspace(0, 4.5, 20); %                     Winds speeds to test

% Frequency sweep
elseif model_sel == 2
    mdl = 'quad';
    simBlock = 'Sine Wave';
    simVar   = 'Frequency';
    ws = logspace(-2, 1, 20); %                       Frequencies to test
% Model Undefined
else
    fprintf('Undefined model\n');
    return
end

start_time = 15; %        Analysis start time, gives model time to settle


%------------------------------ Begin Testing --------------------------%

load_system(mdl); %                                  Load specified model
cs = getActiveConfigSet(mdl); %           Get current model configuration

fprintf('Initialising "%s" Simulation...\n', mdl);

for i = 1:length(ws) %                       Test at each speed specified
    
    % Update simulink block variable
    set_param([mdl, '/', simBlock], simVar, num2str(ws(i)));
    % Set simulation time
    %set_param(cs, 'StopTime', num2str(start_time + 10 * 2*pi * (1/ws(i))));
    
    fprintf('Run: %d of %d\n', i, length(ws)); %         Print out status
    
    try
        simOut = sim(mdl, cs); %                           Run simulation
    catch %                         Catch failed simulations and continue
        fprintf('Simulation failed with value %s = %d\n', simVar, ws(i));
    end
    
    % All simulink variables sent to "toWorkspace" blocks appear in 
    % the simOut object and must be extracted as below
    pos_demand   = get(simOut, 'pos_demand');
    position     = get(simOut, 'position');
    att_demand   = get(simOut, 'attitude_demand');
    attitude     = get(simOut, 'attitude');
    
    % Seperate out x, y and z results
    demand(i, 1) = pos_demand.x_Demand;  
    demand(i, 2) = pos_demand.y_Demand;
    demand(i, 3) = pos_demand.z_Demand;
    actual(i, 1) = position.x;
    actual(i, 2) = position.y;
    actual(i, 3) = position.z;
    
    % Seperate out roll, pitch and yaw results
    demand(i, 4) = att_demand.phi_Demand;
    demand(i, 5) = att_demand.theta_Demand;
    demand(i, 6) = att_demand.psi_Demand;
    actual(i, 4) = attitude.phi;
    actual(i, 5) = attitude.theta;
    actual(i, 6) = attitude.psi;
    
    wind_speed(i) = get(simOut, 'wind_speed');
end

%----------------------------------EOF----------------------------------%
