% Loads the vesicle information (top) and F/L extractions (bottom)
clear all
wt = readmatrix('vesicle_data.xlsx','Sheet', 'WT'); 
pko = readmatrix('vesicle_data.xlsx','Sheet', 'PKO');
cd63ko = readmatrix('vesicle_data.xlsx','Sheet', 'CD63KO');
wtsec = readmatrix('vesicle_data.xlsx','Sheet', 'WT-SEC');

% F/L slopes
wt_slope = readmatrix('FL-slopes.xlsx','Sheet','WT');
cd63ko_slope = readmatrix('FL-slopes.xlsx','Sheet','CD63KO');
panko_slope = readmatrix('FL-slopes.xlsx','Sheet','PanKO');
wtsec_slope = readmatrix('FL-slopes.xlsx','Sheet','WT-SEC');


%%
wt_slope(wt_slope ==0 ) = NaN;
wtsec_slope(wtsec_slope ==0 ) = NaN; 
cd63ko_slope(cd63ko_slope ==0 ) = NaN;
panko_slope(panko_slope ==0 ) = NaN;  

data = wtsec;
slope = wtsec_slope;

k = zeros(size(slope,1),size(slope,2));


for line = 1:length(data)

    R = data(line,3)*10^-9;
    H = data(line,2)*10^-9;
    KbT = 4.11*10^-21;
    
    V_t = (2*pi*R^2*H)/3;
    A_s = 2*pi*R*H*(2-H/(2*R));
    v = (6*sqrt(pi)*V_t)/(A_s^(3/2));
    
    R_s = sqrt(A_s)/(4*pi);
    for nslope = 1:length(slope)
        F = slope(line, nslope)*10^-3;
        L = 1;
        k(line, nslope) = (R_s^2*(1-v^(2/3))*(F/L))/KbT;
    end
end 

%disp(['k [KbT]' ]);
%disp(k);

k(k==0 ) = NaN;
%% Here I calculate mean and STD of the individual slopes
wt = readmatrix('bendmod_individual_data.xlsx','Sheet', 'WT'); 
pko = readmatrix('bendmod_individual_data.xlsx','Sheet', 'PKO');
cd63ko = readmatrix('bendmod_individual_data.xlsx','Sheet', 'CD63KO');
wtsec = readmatrix('bendmod_individual_data.xlsx','Sheet', 'WT-SEC');

% Without caring about the slopeless EVs

wt_kappa = nanmean(wt,2);
wt_kappa_std = nanstd(wt')';

pko_kappa = nanmean(pko,2);
pko_kappa_std = nanstd(pko')';

cd63ko_kappa = nanmean(cd63ko,2);
cd63ko_kappa_std = nanstd(cd63ko')';

wtsec_kappa = nanmean(wtsec,2);
wtsec_kappa_std = nanstd(wtsec')';