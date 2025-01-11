function out = Power(V,d,sig,C,n)
%Power = Power(Voltage(V), wire diameter(mm), resistivity(n*ohm*m), coil length(mm), # of turns)
%This function calculates the power consumed by an air magnetorquer.
%returns Power in mW

P = (V^2*(pi*((d*10^(-3))/2)^2))/(sig*(10^(-9))*C*(10^(-3))*n);
out = P*(10^3);
end