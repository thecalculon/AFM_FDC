%% Calculate radius of curvature
% Takes  a folder with two txt files (before and after cross section) and
% calculates the radius (r_list) of the before/after and also height
% (Hmax_list) if one wants that.

red=[0.8500 0.3250 0.0980];
blue=[0 0.4470 0.7410];

% Import cross sections from gwyddion files 
myFolder = pwd;
filePattern = fullfile(myFolder, '**/*.txt');
theFiles = dir(filePattern);

r_list=[];
Hmax_list=[];
error_list=[];
for k = 1:2
    
    baseFileName = theFiles(k).name;
    fullFileName = fullfile(theFiles(k).folder, baseFileName);
    I = readmatrix(fullFileName, 'Delimiter','  ');
    error=[];
    for i= 1% [1 3 5 7 9 11 13 15 17] % If you have created several cross sections, loop over odd numbers
        szI=size(I);
        I1 = I(:,i:i+1); %The current cross section x- and z-data.
        
        
        H1 =  max(max(I1(:,2)));
        [pos1] = find(I1(:,2)==H1);
        
        
        h1 = flip(I1(1:pos1, 2));
        h2 = I1(pos1:end, 2);
        
        lb = find(h1<(H1/2));
        ub = find(h2<(H1/2));
        
        
        marg=0; %you can add a marginal for the fit if the cross section looks very uneven in some point
        xfit=I1(pos1 - lb(1) +marg:pos1 + ub(1)-marg, 1);
        yfit=I1(pos1 - lb(1)+marg:pos1 + ub(1)-marg, 2);
        if i==1 %which curve you want to look at
            [xc, yc, r, avec] = circlefit(xfit, yfit); %fit a cricle to the top half of the curve
            r_list(k)=r;
            Hmax_list(k)=H1;
        end
        
        th = deg2rad(35):pi/50:pi-deg2rad(35);
        xunit = r * cos(th);
        yunit = r * sin(th) + yc;

        th2 = 0:pi/50:2*pi;
        xunit2=(r-5*10^-9)* cos(th2); %"5" is with a tip radius of 5 nm 
        yunit2=(r-5*10^-9)* sin(th2) + yc+5*10^-9;
            figure(k)
        plot(I(:,1)*10^9-xc*10^9, I(:,2)*10^9, 'LineWidth',2, 'Color','r') %original cross section 
        hold on
        plot(xunit*10^9, yunit*10^9, 'LineWidth',1.5, 'Color','k') %Fitted curve in som range th
        plot(xunit2*10^9, yunit2*10^9, 'LineWidth',1.5, 'Color','k', 'LineStyle','--') %Fitted curve with tip correction 
        set(gca, 'FontSize', 14)
        xlabel('X (nm)')
        ylabel('Height (nm)')
        %title(k)
        hleg1=legend('Lineprofile', 'Fitted arc', 'Tip-corrected EV shape');
        set(hleg1,'position',[0 0 0.7 0.15])
        axis([-100 100 0 100])    
        %% Error calculation - maybe check this again 
        %looks at the difference between the first circle fit and a cross
        %section in an other dircetion 
        v = [xfit, yfit];
        cc = [xc, yc];
        d=sqrt((v(:,1)-xc).^2+(v(:,2)-yc).^2) - r;
        error(:,i) = sum(d.^2);
        error=error(error~=0);
            %Plot the curve and fit for each vesicle 
    end
    error_list(:,k)=error; hold on
    if k == 1
    Ione = I;
    xcone = xc;
    end
end


%%  Plot the values

plot(Ione(:,1)*10^9-xcone*10^9, Ione(:,2)*10^9, 'LineWidth',2, 'Color','r'); hold on; %original cross section 
plot(I(:,1)*10^9-xc*10^9, I(:,2)*10^9, 'LineWidth',2, 'Color','y') %original cross section 
hold on
plot(xunit*10^9, yunit*10^9, 'LineWidth',2, 'Color','k') %Fitted curve in som range th
plot(xunit2*10^9, yunit2*10^9, 'LineWidth',2, 'Color','k', 'LineStyle','--') %Fitted curve with tip correction 
set(gca,'linew',2, 'fontsize', 20) 
xlabel('X (nm)'); 
ylabel('Height (nm)')
hleg1=legend('Profile (before)', 'Profile (after)' , 'Fitted arc', 'Tip-corrected EV shape');
axis([-100 100 0 100])
box

%%
function [xCenter, yCenter, radius, a] = circlefit(x, y)
% [xCenter, yCenter, radius, a] = circlefit(X, Y)
%     x ^ 2 + y ^ 2 + a(1) * x + a(2) * y + a(3) = 0

numPoints = numel(x);
xx = x .* x;
yy = y .* y;
xy = x .* y;
A = [sum(x),  sum(y),  numPoints;
     sum(xy), sum(yy), sum(y);
     sum(xx), sum(xy), sum(x)];
B = [-sum(xx + yy) ;
     -sum(xx .* y + yy .* y);
     -sum(xx .* x + xy .* y)];
a = A \ B;
xCenter = -.5 * a(1);
yCenter = -.5 * a(2);
radius  =  sqrt((a(1) ^ 2 + a(2) ^ 2) / 4 - a(3));
end

