import uuid
from datetime import datetime

import hdf5storage
import numpy as np
import pytz
from pynwb import NWBFile, NWBHDF5IO
from pynwb.misc import Units
from pynwb.file import Subject
from pynwb.behavior import Position, BehavioralEvents

def convert(input_file,
            session_start_time,
            subject_date_of_birth,
            subject_id='L5',
            subject_description='wild-type',
            subject_sex='M',
            subject_weight='11.6g',
            subject_species='Mus musculus',
            subject_genotype='',
            subject_brain_region='Medial Entorhinal Cortex',
            surgery='Probe: +/-3.3mm ML, 0.2mm A of sinus, then as deep as possible',
            session_id='npI5_0417_baseline_1',
            experimenter='Kei Masuda',
            experiment_description='Virtual Hallway Task',
            institution='Stanford University School of Medicine',
            lab_name='Giocomo Lab'):
    """
    Read in the .mat file specified by input_file and convert to .nwb format.

    Parameters
    ----------
    input_file : np.ndarray (..., n_channels, n_time)
        the .mat file to be converted
    subject_id : string
        the unique subject ID number for the subject of the experiment
    subject_date_of_birth : datetime ISO 8601
        the date and time the subject was born
    subject_description : string
        important information specific to this subject that differentiates it from other members of it's species
    subject_sex : string
        Male or Female
    subject_weight :
        the weight of the subject around the time of the experiment
    subject_species : string
        the name of the species of the subject
    subject_brain_region : basestring
        the name of the brain region where the electrode probe is recording from
    surgery : str
        information about the subject's surgery to implant electrodes
    session_id: string
        human-readable ID# for the experiment session that has a one-to-one relationship with a recording session
    session_start_time : datetime
        date and time that the experiment started
    experimenter : string
        who ran the experiment, first and last name
    experiment_description : string
        what task was being run during the session
    institution : string
        what institution was the experiment performed in
    lab_name : string
        the lab where the experiment was performed

    Returns
    -------
    nwbfile : NWBFile
        The contents of the .mat file converted into the NWB format.  The nwbfile is saved to disk using NDWHDF5
    """

    # input matlab data
    matfile = hdf5storage.loadmat(input_file)

    # output path for nwb data
    def replace_last(source_string, replace_what, replace_with):
        head, _sep, tail = source_string.rpartition(replace_what)
        return head + replace_with + tail
    outpath = replace_last(input_file, '.mat', '.nwb')

    create_date = datetime.today()
    timezone_cali = pytz.timezone('US/Pacific')
    create_date_tz = timezone_cali.localize(create_date)

    # if loading data from config.yaml, convert string dates into datetime
    if isinstance(session_start_time,str):
        session_start_time = datetime.strptime(session_start_time, '%B %d, %Y %I:%M%p')
        session_start_time = timezone_cali.localize(session_start_time)

    if isinstance(subject_date_of_birth,str):
        subject_date_of_birth = datetime.strptime(subject_date_of_birth, '%B %d, %Y %I:%M%p')
        subject_date_of_birth = timezone_cali.localize(subject_date_of_birth)

    # create unique identifier for this experimental session
    uuid_identifier = uuid.uuid1()

    # Create NWB file
    nwbfile = NWBFile(session_description=experiment_description,  # required
                      identifier=uuid_identifier.hex,  # required
                      session_id=session_id,
                      experiment_description=experiment_description,
                      experimenter=experimenter,
                      surgery=surgery,
                      institution=institution,
                      lab=lab_name,
                      session_start_time=session_start_time,  # required
                      file_create_date=create_date_tz)  # optional

    # add information about the subject of the experiment
    experiment_subject = Subject(subject_id=subject_id,
                                 species=subject_species,
                                 description=subject_description,
                                 date_of_birth=subject_date_of_birth,
                                 weight=subject_weight,
                                 sex=subject_sex)

    nwbfile.subject = experiment_subject

    # Adding trial information
    nwbfile.add_trial_column('trial_contrast', 'visual contrast of the maze through which the mouse is running')
    trial = np.ravel(matfile['trial'])
    trial_nums = np.unique(trial)
    position_time = np.ravel(matfile['post'])
    # matlab trial numbers start at 1. To correctly index trial_contract vector,
    # subtracting 1 from 'num' so index starts at 0
    for num in trial_nums:
        trial_times = position_time[trial == num]
        nwbfile.add_trial(start_time=trial_times[0],
                          stop_time=trial_times[-1],
                          trial_contrast=matfile['trial_contrast'][num-1][0])


    # Add mouse position inside:
    position = Position()
    position_virtual = np.ravel(matfile['posx'])
    # position inside the virtual environment
    sampling_rate = 1/(position_time[1] - position_time[0])
    position.create_spatial_series(name='Position',
                                   data=position_virtual,
                                   starting_time=position_time[0],
                                   rate=sampling_rate,
                                   reference_frame='The start of the trial, which begins at the start '
                                                   'of the virtual hallway.',
                                   conversion=0.01,
                                   description='Subject position in the virtual hallway.',
                                   comments='The values should be >0 and <400cm. Values greater than '
                                            '400cm mean that the mouse briefly exited the maze.',)

    # physical position on the mouse wheel
    physical_posx = position_virtual
    trial_gain = np.ravel(matfile['trial_gain'])
    for num in trial_nums:
        physical_posx[trial == num] = physical_posx[trial == num]/trial_gain[num-1]

    position.create_spatial_series(name='PhysicalPosition',
                                   data=physical_posx,
                                   starting_time=position_time[0],
                                   rate=sampling_rate,
                                   reference_frame='Location on wheel re-referenced to zero '
                                                   'at the start of each trial.',
                                   conversion=0.01,
                                   description='Physical location on the wheel measured '
                                               'since the beginning of the trial.',
                                   comments='Physical location found by dividing the '
                                            'virtual position by the "trial_gain"')
    nwbfile.add_acquisition(position)

    # Add timing of lick events, as well as mouse's virtual position during lick event
    lick_events = BehavioralEvents()
    lick_events.create_timeseries('LickEvents',
                                  data=np.ravel(matfile['lickx']),
                                  timestamps=np.ravel(matfile['lickt']),
                                  unit='centimeter',
                                  description = 'Subject position in virtual hallway during the lick.')
    nwbfile.add_acquisition(lick_events)

    # Add the recording device, a neuropixel probe
    recording_device = nwbfile.create_device(name='neuropixel_probes')
    electrode_group_description = 'single neuropixels probe http://www.open-ephys.org/neuropixelscorded'
    electrode_group_name = 'probe1'
    electrode_group_location = 'medial entorhinal cortex'

    electrode_group = nwbfile.create_electrode_group(electrode_group_name,
                                                     description=electrode_group_description,
                                                     location=subject_brain_region,
                                                     device=recording_device)

    # Add information about each electrode
    xcoords = np.ravel(matfile['sp'][0]['xcoords'][0])
    ycoords = np.ravel(matfile['sp'][0]['ycoords'][0])
    data_filtered_flag = matfile['sp'][0]['hp_filtered'][0][0]
    if data_filtered_flag:
        filter_desc = 'The raw voltage signals from the electrodes were high-pass filtered'
    else:
        filter_desc = 'The raw voltage signals from the electrodes were not high-pass filtered'

    num_recording_electrodes = xcoords.shape[0]
    recording_electrodes = range(0, num_recording_electrodes)

    # create electrode columns for the x,y location on the neuropixel  probe
    # the standard x,y,z locations are reserved for Allen Brain Atlas location
    nwbfile.add_electrode_column('relativex','electrode x-location on the probe')
    nwbfile.add_electrode_column('relativey','electrode y-location on the probe')

    for idx in recording_electrodes:
        nwbfile.add_electrode(idx,
                              x=np.nan,
                              y=np.nan,
                              z=np.nan,
                              relativex=float(xcoords[idx]),
                              relativey=float(ycoords[idx]),
                              imp=np.nan,
                              location='medial entorhinal cortex',
                              filtering=filter_desc,
                              group=electrode_group)


    # Add information about each unit, termed 'cluster' in giocomo data
    # create new columns in unit table
    nwbfile.add_unit_column('quality', 'the labels that you gave to the clusters during manual sorting in phy (1=MUA, '
                                       '2=Good, 3=Unsorted)')
    cluster_ids = matfile['sp'][0]['cids'][0][0]
    cluster_quality = matfile['sp'][0]['cgs'][0][0]
    # spikes in time
    spike_times = np.ravel(matfile['sp'][0]['st'][0])  # the time of each spike
    spike_cluster = np.ravel(matfile['sp'][0]['clu'][0])  # the cluster_id that spiked at that time

    for i, cluster_id in enumerate(cluster_ids):
        unit_spike_times = spike_times[spike_cluster == cluster_id]
        waveforms = matfile['sp'][0]['temps'][0][cluster_id]
        nwbfile.add_unit(id=int(cluster_id),
                         spike_times=unit_spike_times,
                         quality=cluster_quality[i],
                         waveform_mean=waveforms,
                         electrode_group=electrode_group)


    # Trying to add another Units table to hold the results of the automatic spike sorting
    # create TemplateUnits units table
    template_units = Units(name='TemplateUnits',
                           description='units assigned during automatic spike sorting')

    spike_templates = np.ravel(matfile['sp'][0]['spikeTemplates'][0])
    spike_template_ids = np.unique(spike_templates)

    for i, spike_template_id in enumerate(spike_template_ids):
        template_spike_times = spike_times[spike_templates == spike_template_id]
        template_units.add_unit(id=int(spike_template_id),
                                spike_times=template_spike_times,
                                electrode_group=electrode_group)

    # create ecephys processing module
    spike_template_module = nwbfile.create_processing_module(
        name='ecephys', description='units assigned during automatic spike sorting')

    # add template_units table to processing module
    spike_template_module.add(template_units)

    print(nwbfile)
    print('converted to NWB:N')
    print('saving ...')

    with NWBHDF5IO(outpath, 'w') as io:
        io.write(nwbfile)
        print('saved', outpath)

if __name__ == '__main__':
    default_data = dict(input_file='D:\\Data\\scenda\\giocomo\\npI5_0417_baseline_1.mat',
                        session_start_time='April 4, 2017 10:00AM',
                        subject_date_of_birth='April 4, 2016 12:15AM',
                        subject_id='L5',
                        subject_description='wild-type',
                        subject_sex='M',
                        subject_weight='11.6g',
                        subject_species='Mus musculus',
                        subject_genotype='',
                        subject_brain_region='Medial Entorhinal Cortex',
                        surgery='Probe: +/-3.3mm ML, 0.2mm A of sinus, then as deep as possible',
                        session_id='npI5_0417_baseline_1',
                        experimenter='Kei Masuda',
                        experiment_description='Virtual Hallway Task',
                        institution='Stanford University School of Medicine',
                        lab_name='Giocomo Lab')
    convert(**default_data)
