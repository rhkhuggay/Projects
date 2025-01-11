function out = mdipole(V,d,sig,S,C)
%magnetic dipole = mdipole(Voltage(V), wire diameter(mm), resistivity(n*ohm*m), Coil area(mm^2), coil length(mm))
%This function calculates the magnetic dipole produced by an air magnetorquer.
%returns magnetic dipole in Am^2

m = (V*(pi*(d/2)^2)*S)/(sig*(10^(-9))*(10^3)*C);
out = m*(10^(-3))^2;
end
