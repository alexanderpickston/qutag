import QuTAG_HR
import numpy as np
import time

CoincCounter_names = ['0(Start)','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31','32','1/2','1/3','2/3','1/4','2/4','3/4','1/5','2/5','3/5','4/5','1/2/3','1/2/4','1/3/4','2/3/4','1/2/5','1/3/5','2/3/5','1/4/5','2/4/5','3/4/5','1/2/3/4','1/2/3/5','1/2/4/5','1/3/4/5','2/3/4/5','1/2/3/4/5']

channels = [1, 2]

def coincidence_counter_index(channels):
    '''
    from the list of channels, fetch the index of the coincidence counter
    '''
    channel_list = [channels[i] for i in range(len(channels))]

    channel_list_string = []
    for i in channel_list:
        channel_list_string.append(str(i))

    ele = "/".join(channel_list_string)
    cc_index = CoincCounter_names.index(ele)
    
    return(cc_index)

qutag = QuTAG_HR.QuTAG()
exposure_time = 50

def exposure_time_multiplier(exposure_time):
    '''
    converting the exposure time (ms) to chunks of Hz 
    '''
    exposure_time_seconds = exposure_time/1000 # conversion from ms to s
    conversion = 1/exposure_time_seconds

    return(conversion)

_multiplier = int(exposure_time_multiplier(exposure_time))

buffer = []
singles1 = []
singles2 = []
coincidences = []

qutag.setExposureTime(exposure_time) # ms read time

while True:
    try: 

        for ii in range(_multiplier):
            
            time.sleep(exposure_time/1000) # conversion to ms

            _singles = [qutag.getCoincCounters()[0][i] for i in channels]
            _coincidences = qutag.getCoincCounters()[0][coincidence_counter_index(channels)]

            singles1.append(_singles[0])
            singles2.append(_singles[1])

            coincidences.append(_coincidences)
        
            if len(coincidences) >= _multiplier:
                print(
                    'Singles1: ', sum(singles1[-(_multiplier)::]), 
                    '| Singles2: ', sum(singles2[-(_multiplier)::]), 
                    '| Coincidences: ', sum(coincidences[-(_multiplier)::]),
                    '| eta: ', (sum(coincidences[-(_multiplier)::]) // np.sqrt(sum(singles1[-(_multiplier)::]) * sum(singles2[-(_multiplier)::])))
                )
        
    except KeyboardInterrupt:
        print('Keyboard interrupt')
        
        raise

qutag.deInitialize()