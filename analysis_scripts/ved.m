% Plots the average electrode for each timepoint
clear;

% Load training data
mydir = pwd;
idcs = strfind(mydir,'\');
loc = mydir(1:idcs(end)-1);
load([loc '\preprocessed_data\one_subject\train.mat']) % returns struct train
%train = train(1:10000);

%% Preallocate vectors
node_sums0 = [];
node_sums1 = [];
N = length(train);
t = -200:4:996;

for i = 1:length(train)
    if train(i).visible == 0
        node_sums0 = [node_sums0 ; train(i).data];
    else
        node_sums1 = [node_sums1 ; train(i).data];
    end
end

%node_sums1 = node_sums1(1:1161,:);

node_means0 = sum(node_sums0,1) ./ N;
node_means1 = sum(node_sums1,1) ./ N;

std0 = std(node_sums0,0,1)./20;
std1 = std(node_sums1,0,1)./20;

figure(1)
hold on;
x = 1:size(node_sums0,2);
%fill([x, flip(x)], [node_means0+std0, flip(node_means0-std0)], [0.8 0.8 0.8])
plot(t,node_means0)
title('Event Related Potentials C = "visible"')
xlabel('Time (ms)')
ylabel('Amplitude (mV)')

figure(2)
hold on;
x = 1:size(node_sums1,2);
%fill([x, flip(x)], [node_means1+std1, flip(node_means1-std1)], [0.8 0.8 0.8])
plot(t,node_means1)
title('Event Related Potentials C = "invisible"')
xlabel('Time (ms)')
ylabel('Amplitude (mV)')
