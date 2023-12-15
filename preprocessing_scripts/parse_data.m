if isempty(which('eeglab'))
    addpath('/usr4/ugrad/myb24/Downloads/eeglab2022.1');
end
eeglab('nogui')

%% get files
fol = '/ad/eng/research/eng_research_lewislab/users/myb24/BE562';
binfile = [fol '/at_bins.txt'];

rawfiles = dir('/ad/eng/research/eng_research_lewislab/users/myb24/BE562/data/*/*/*.vhdr');

% get id
partid = cell(length(rawfiles),1);
for f= 1:length(rawfiles)
    name = strsplit(rawfiles(f).name,{'_' '-'});
    partid{f} = name{2};
end

%% run preprocessing
for p = 1:length(rawfiles)

    %% preprocessing 
    % get for preprocessed file already
    contfile = sprintf('%s/data/derivatives/eeglab/sub-%s_task-rsvp_continuous.set',fol,partid{p});
    EEG = pop_loadset(contfile);
        
    %% create epochs
    EEG_epoch = pop_epoch(EEG, {1;3}, [-.2 1]);
    EEG_epoch = eeg_checkset(EEG_epoch);
    
    %% get eventinfo
    eventsfntsv = sprintf('%s/data/sub-%s/eeg/sub-%s_task-rsvp_events.tsv',fol,partid{p},partid{p});
    eventlist = tdfread(eventsfntsv);

    %% create structs
    parsed = struct;
    sub = 0;
    for i = 1:EEG_epoch.trials
        idx = i - sub;
        if eventlist.visible(i) ~= 2
            % Average occiptal channels
            d = EEG_epoch.data(9,:,i) + EEG_epoch.data(22,:,i) + EEG_epoch.data(10,:,i);
            d = d./3;
    
            % Data information
            parsed(idx).data = d;
            parsed(idx).order_id = i;
    
            % Event information
            parsed(idx).visible = eventlist.visible(i);
            parsed(idx).position = eventlist.position(i);
            parsed(idx).direction = eventlist.direction(i);
            parsed(idx).accuracy = eventlist.accuracy(i);
        else
            sub = sub + 1;
        end
    end
    
    %% save epochs
    save(sprintf('%s/parsed_data/sub-%s_task-rsvp_parsed.mat',fol,partid{p}),'parsed','-v7.3');
    
end
