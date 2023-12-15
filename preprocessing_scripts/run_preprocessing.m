
function run_preprocessing

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
    % check for preprocessed file already
    contfile = sprintf('%s/data/derivatives/eeglab/sub-%s_task-rsvp_continuous.set',fol,partid{p});
    if ~isempty(dir(contfile))
        %         EEG = pop_loadset(contfile);
        fprintf('Skipping %s...\n',partid{p})
        EEG = pop_loadset(contfile);
        continue
    else % do preprocessing
        
        fprintf('Processing %s...\n',partid{p})

        %% load data
        EEG = pop_loadbv(rawfiles(p).folder,rawfiles(p).name);
        EEG = eeg_checkset(EEG);
        
        setname = partid{p};
        EEG.setname = setname;
        EEG = eeg_checkset(EEG);
        
        %% preprocess data
        
        % add Cz channel and re-reference, adding Cz back into dataset
        EEG=pop_chanedit(EEG, 'append',63,'changefield',{64 'labels' 'Cz'},'setref',{'' 'Cz'});
        Czloc = struct('labels',{'Cz'},'type',{''},'theta',{0},'radius',{0},'X',{5.2047e-15},'Y',{0},'Z',{85},'sph_theta',{0},'sph_phi',{90},'sph_radius',{85},'urchan',{64},'ref',{''},'datachan',{0});
        EEG = pop_reref( EEG, [],'refloc',Czloc);
        EEG = eeg_checkset(EEG);
        
        % high pass filter
        EEG = pop_eegfiltnew(EEG, 0.1,[]);
        
        % low pass filter
        EEG = pop_eegfiltnew(EEG, [],100);
        
        % downsample
        EEG = pop_resample(EEG, 250);
        EEG = eeg_checkset(EEG);
                
        % create eventlist
        EEG  = pop_creabasiceventlist( EEG , 'AlphanumericCleaning', 'on', 'BoundaryNumeric', { -99 }, 'BoundaryString', { 'boundary' });
        EEG = eeg_checkset(EEG);
        
        % save preprocessed data
        EEG = pop_saveset(EEG, 'filename', sprintf('/ad/eng/research/eng_research_lewislab/users/myb24/BE562/data/derivatives/eeglab/sub-%s_task-rsvp_continuous.set',partid{p}));
    
    end
    
    %% create epochs
    EEG_epoch = pop_epoch(EEG, {1;3}, [-.2 1]);
    EEG_epoch = eeg_checkset(EEG_epoch);
    
    %% get eventinfo
    eventsfntsv = sprintf('%s/data/sub-%s/eeg/sub-%s_task-rsvp_events.tsv',fol,partid{p},partid{p});
    eventlist = tdfread(eventsfntsv);

    %% convert to cosmo
    ds = cosmo_flatten(permute(EEG_epoch.data,[3 1 2]),{'chan','time'},{{EEG_epoch.chanlocs.labels},EEG_epoch.times},2);
    ds.a.meeg=struct(); %or cosmo thinks it's not a meeg ds 
    ds.sa = eventlist;
    cosmo_check_dataset(ds,'meeg');
    
    %% save epochs
    save(sprintf('%s/data/derivatives/cosmomvpa/sub-%s_task-rsvp_cosmomvpa.set',fol,partid{p}),'ds','-v7.3')
    
end

end
