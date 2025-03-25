%% Read data from afm
%myFolder is the folder with your .txt-files of force curves
%Fo is the force-responce, z1 is indentation-data with bending correction,
%z7 is without bending correction.
clear all
myFolder = ['221216ev6_08nN'];

[Fo, z1, z7, zdiff]  = extractCurves(myFolder);  
z1 = -1*z1;

%% Calculate KA tilde values
%  The values are stored in kval for each indentation.
%  The parameters (first pos and last entry (for calculating the linear
%  slope)) might need to be fine-tuned for individual EVs/indentations.

kval = []; 
%clf
plotta = true;
for ii = 1 : size(z1,2)
    first_pos = find(z1(1:floor(end/2),ii) > 0, 1)+20; % >0 OG: + 201
    last_entry = first_pos+50;                        % OG + 150
    last_entry = find(Fo(1:floor(end/2),ii) > 80, 1);
    first_pos = last_entry-100;
    p = polyfit(z1(first_pos:last_entry,ii), Fo(first_pos:last_entry,ii),1);
    f = polyval(p,z1(first_pos:last_entry,ii));
    kval(ii) = p(1);
    if plotta == 1
        plot(z1(1:floor(end/2),ii),Fo(1:floor(end/2),ii), 'linewidth',2); hold on;
        %plot(z1(floor(end/2):end,ii),Fo(floor(end/2):end,ii), 'linewidth',2); hold on;
        %plot(z1(first_pos:last_entry,ii),f,'-','linewidth',4,'color','red')
        box on; set(gca,'TickLength', [0.01 0], 'FontSize', 22, 'linewidth',2);
        %legend({'Approach', 'Retract'}, 'location','NE')
        xlabel('Indentation (nm)'); ylabel('Force (pN)'); title('Indentation curve');
        ylim([-50 1000]); yticks([ -100 0, 200, 400, 600 800]); 
        xlim([-150 50])
        %w = waitforbuttonpress;clf % Untag this if you want to see
        %individual curves
    end
end

axis square,
range = 1:length(kval);

%% Takes all individual linstiff values and plots the spread
% Can probably be implemented nicer, but yeah.

inddata = readmatrix('linstiff_individual_data.xlsx','Sheet','WT');

%% Showing KA-tilde for a single EV
clf
plot(1:150,inddata(2,end-150:end-1),'.','markersize',25,'color','#FF0100');
xlabel('FDC');ylabel('$\tilde{K_A}$ (mN/m)','interpreter','latex');
box on; set(gca,'TickLength', [0.01 0], 'FontSize', 22, 'linewidth',2);
axis square
title('Single EV') %FF0100, FFE000
%exportgraphics(gcf,'all_linstiff.pdf','ContentType','vector')

yline(mean(inddata(2,end-150:end-1))); hold on;
yline(mean(inddata(2,end-150:end-1))+std(inddata(2,end-150:end-1)/2));hold on;
yline(mean(inddata(2,end-150:end-1))-std(inddata(2,end-150:end-1)/2))


%% Hard coded for this example, to show one EV and average
% Calculate kappa values
%clf

figure(3)
kval = []; 
plotta = true;
for ii =1 : size(z1,2)
    [~,max_i] = max(Fo(:,ii));
    if plotta == 1
        plot(z1(1:max_i,ii),Fo(1:max_i,ii), 'linewidth',2,'Color',['#FFE000' .25]); hold on;
        box on; set(gca,'TickLength', [0.01 0], 'FontSize', 20, 'linewidth',2);
        xlabel('Indentation (nm)'); ylabel('Force (pN)');  
        xlim([-5, 50]); ylim([-60,900]);
    end
end 

makeavg_z = NaN(3000,150);
makeavg_f = NaN(3000,150);
[~, imaxf] = max(Fo);

for ii= 1 : 150 % HARD CODED
    makeavg_f(:,ii) = [Fo(1:imaxf(ii),ii) ; repmat(NaN,3000-length(Fo(1:imaxf(ii))),1)];
    makeavg_z(:,ii) = [z1(1:imaxf(ii),ii) ; repmat(NaN,3000-length(Fo(1:imaxf(ii))),1)];
end
mfo = nanmean(makeavg_f,2);
mz1 = nanmean(makeavg_z,2);
plot(mz1(1:end-1450), mfo(1:end-1450), 'linewidth',3,'Color',['#FF0100']);
axis square

%% Fdc

function [Fo, z1, z7, zdiff] = extractCurves(myFolder)
filePattern = fullfile(myFolder, '**/*.txt');
theFiles = dir(filePattern);
z7=0;
zdiff=0;

for k = 1 : length(theFiles)
    baseFileName = theFiles(k).name;
    fullFileName = fullfile(theFiles(k).folder, baseFileName);
    data = readmatrix(fullFileName,'NumHeaderLines',79, 'Delimiter',' ');
    szD=size(data);
    F(1:szD(1),k) = data(:, 2); %vertical deflection parameter
    z1(1:szD(1),k) = data(:, 1); %height (tip adjusted)
    z7(1:szD(1),k) = data(:, 7); %height (measured)
end

Fo=F/10^-12;
z1=z1/10^-9;
z7=z7/10^-9;

Fsz=size(Fo);
Zsz=size(z1);

Fn=zeros(Fsz(2),1);
Zn=zeros(Zsz(2),1);
end