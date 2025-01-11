function out = Mass(p,d,C,n)
%Mass = Mass(linear density(kg/m^3), wire diameter(mm), coil length(mm), # of turns)
%This function calculates the mass of an air magnetorquer.
%returns Mass in g

kg = p*((10^(-3))^3)*(pi*(d/2)^2)*C*n;
out = kg*10^3;
end
