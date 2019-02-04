function [cl,cd]=getLiftDrag(alpha);
% [cl,cd]=getLiftDrag(alpha);
%
% Thin aerofoil theory approximation to local lift coefficient.
% Slightly bodgy estimate of local drag coefficient based on NACA0012 at
% Reynolds number of 100,000. I hope to improve on the options available
% here.
%
% alpha is the effective AoA
%

% To do:
% - add tip/downwash effects due to AR, and maybe span efficiency factor?
%   (new function perhaps? keep local cl and alpha_eff here?)
% - include option for cl0 for cambered aerofoils?
% - improve options for cd calculation: other Re nums, other aerofoils

% assume thin aerofoil theory for cl
cl=2*pi*alpha/180*pi;

% using very approx. cd for NACA0012 from airfoiltools.com, Re=100,000
% (see screenshot, orange line is Re=100,000; blue line is Re=50,000; dirty orange is Re=1,000,000)
cd = 0.015 + 0.03*cl.^2;
