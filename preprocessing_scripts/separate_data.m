% Create test and train data
clear;

test = struct([]);
train = struct([]);

%% get files
fol = '/ad/eng/research/eng_research_lewislab/users/myb24/BE562';

rawfiles = dir('/ad/eng/research/eng_research_lewislab/users/myb24/BE562/parsed_data/*.mat');

%% run preprocessing
for i = 1:length(1)
    loc = sprintf("%s/%s", rawfiles(i).folder, rawfiles(i).name);
    load(loc); % Returns struct called parsed
    N = length(parsed);
    idx = randperm(N);
    trainS = idx(1:round(N*0.8));
    testS = idx(round(N*0.8):N);

    train = [train parsed(trainS)];
    test = [test parsed(testS)];
    disp(i)
    
end

save("separated_data/train.mat", 'train','-v7.3')
save("separated_data/test.mat", 'test','-v7.3')

