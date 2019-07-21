import uuid
from datetime import datetime

import hdf5storage
import numpy as np
import pytz
from pynwb import NWBFile, NWBHDF5IO
from pynwb.misc import Units

out_path = 'G:\\My Drive\\Giocomo\\data\\npI5_0417_baseline_1.nwb'

# load matlab data
matfile = hdf5storage.loadmat('G:\\My Drive\\Giocomo\\data\\npI5_0417_baseline_1.mat')

# print variables inside matlab data
print(matfile.keys())

# setup general experimental variables
# timezones
timezone_cali = pytz.timezone('US/Pacific')
timezone_pa = pytz.timezone('US/Eastern')

# create times with the correct time zone
start_time = datetime(2018, 4, 3, 11)  # start of experiment
start_time_tz = timezone_cali.localize(start_time)

create_date = datetime.today()
create_date_tz = timezone_pa.localize(create_date)

uuid_identifier = uuid.uuid1()

# General experiment settings
"""
subject_id=
subject_date_of_birth =
subject_sex =
subject_species =
subject_description = 
subject_weight =
session_id= 'npI5_0417_baseline_1'
session_start_time =
experimenter =
experiment_description =
lab_name =
institution =
"""

# Create NWB file
nwbfile = NWBFile(session_description='demonstrate NWBFile basics',  # required
                  identifier=uuid_identifier.hex,  # required
                  session_id='0417',
                  session_start_time=start_time_tz,  # required
                  file_create_date=create_date_tz)  # optional
print(nwbfile)
print(create_date)
print(start_time)

# Adding trial information
nwbfile.add_trial_column('trial_contrast', 'visual contrast of the maze through which the mouse is running')
trial = np.ravel(matfile['trial'])
trial_nums = np.unique(trial)
position_time = np.ravel(matfile['post'])
# matlab trial numbers start at 1. To correctly index trial_contract vector, subtracting 1 from 'num' so index starts at 0
for num in trial_nums:
    trial_times = position_time[trial == num]
    nwbfile.add_trial(start_time=trial_times[0],
                      stop_time=trial_times[-1],
                      trial_contrast=matfile['trial_contrast'][num-1])

print(nwbfile)

# Add mouse position inside:
from pynwb.behavior import Position

position = Position()
position_virtual = np.ravel(matfile['posx'])
# position inside the virtual environment
position.create_spatial_series(name='Position',
                               data=position_virtual,
                               timestamps = position_time,
                               reference_frame='The start of the trial, which begins at the start of the virtual hallway.',
                               conversion=0.01,
                               description='Mouse location in the virtual hallway.',
                               comments='The values should be >0 and <400cm. Values greater than 400cm mean that the mouse briefly exited the maze.',)

# physical position on the mouse wheel
physical_posx = position_virtual
trial_gain = np.ravel(matfile['trial_gain'])
for num in trial_nums:
    print(num,trial_gain[num-1])
    physical_posx[trial == num] = physical_posx[trial == num]/trial_gain[num-1]

position.create_spatial_series(name='PhysicalPosition',
                               data=physical_posx,
                               timestamps=position_time,
                               reference_frame='Location on wheel re-referenced to zero at the start of each trial.',
                               conversion=0.01,
                               description='Physical location on the wheel since the beginning of the trial.',
                               comments='Physical location found by dividing the virtual position by the "trial_gain"')
nwbfile.add_acquisition(position)
print(nwbfile)

print(nwbfile.acquisition['Position'].get_spatial_series('PhysicalPosition'))

# Add timing of lick events, as well as mouse's virtual position during lick event
from pynwb.behavior import BehavioralEvents

lick_events = BehavioralEvents()
lick_events.create_timeseries('LickEvents',
                              data=np.ravel(matfile['lickx']),
                              timestamps=np.ravel(matfile['lickt']),
                              unit='unitless sensor values',
                              description = 'Mouse location in virtual hallway during a lick.')
nwbfile.add_acquisition(lick_events)
print(nwbfile)

# Add the recording device, a neuropixel probe
recording_device = nwbfile.create_device(name='neuropixel_probes')
electrode_group_description = 'single neuropixels probe http://www.open-ephys.org/neuropixelscorded'
electrode_group_name = 'probe1'
electrode_group_location = 'somewhere in visual area 1 (V1)'

electrode_group = nwbfile.create_electrode_group(electrode_group_name,
                                                 description=electrode_group_description,
                                                 location=electrode_group_location,
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
for idx in recording_electrodes:
    nwbfile.add_electrode(idx,
                          x=float(xcoords[idx]),
                          y=float(ycoords[idx]),
                          z=np.nan,
                          imp=np.nan,
                          location='V1',
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

print(nwbfile)

# Trying to add another Units table to hold the results of the automatic spike sorting
spike_template = matfile['sp'][0]['spikeTemplates'][0]
spike_template_ids = np.unique(spike_template)
# # do I need to add the other columns, spike_times and spike_times_idx?
# template_units = Units(name='TemplateUnits',
#                              id=spike_template_ids,
#                              description='units assigned during automatic spike sorting')

# how do I add information - only as a vector?  I'm not sure how to add the spike_times vector?
# I get TypeError: unrecognized argument: 'spike_times" and "spike_times_index"
template_units = Units(name='TemplateUnits',
                       description='units assigned during automatic spike sorting')
for i in range(10):
    template_units.add_unit(spike_times=spike_times)

nwbfile.add_acquisition(template_units)

with NWBHDF5IO(out_path, 'w') as io:
    io.write(nwbfile)


