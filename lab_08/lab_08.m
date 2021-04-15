function main

% Input parameters
A = 1.0;
sigma = 1.0;

% Borders of calculation
mult = 5;
step = 0.005;
t = -mult:step:mult;

% Pulse generation
x = gauspls(t,A,sigma);

% Impulsive noise generation
count = 20;
M = 0.4;
n = impnoise(length(x),count,M);
z = x+n;

width = 3;
eps = M/4;

y1 = z;
smooth = @(x) mean(x);
for i = 1:length(z)
    y1(i) = ampsmooth(y1, i, smooth, width, eps);
end

y2 = z;
smooth = @(x) med(x);
for i = 1:length(z)
    y2(i) = ampsmooth(y2, i, smooth, width, eps);
end

%
% PLOTTING
%

figure(1)
plot(t,z,'black',t,y1,'r');
title('Mean Method');
figure(2)
plot(t,z,'black',t,y2,'b');
title('Median method');
end

% Gaussian pulse generation
function y = gauspls(x,A,s)
	y = A * exp(-(x/s).^2);
end

% Impulsive noise generation
function y = impnoise(size,N,mult)
    y = zeros(1,size);
 	y(round(unifrnd(1,size,[1,N]))) = mult*unifrnd(0,1,[1,N]);
end

% Amplitude smoothing
function y = ampsmooth(A, i, SMTH, W, eps)
    y = A(i);
    if (i - W < 1)
        S = SMTH(A(1:2*W + 1));
    else if (i + W > length(A))
            S = SMTH(A(length(A) - 2*W:length(A)));
        else
            S = SMTH(A(i - W:i + W));
        end
    end
    
    for i = 1:length(A)
        if eps < abs(A(i) - S)
            y = S;
        end
    end
end

% median function
function y = med(A)
    rk = sort(A);
    y = rk((length(A) + 1) / 2);
end
