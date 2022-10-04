import os
import time
import QuTAG_HR
import pandas as pd

from datetime import datetime

qutag = QuTAG_HR.QuTAG()

channels = [1, 2]
qutag.setExposureTime(10)


CoincCounter_names = ['0(Start)','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31','32','1/2','1/3','2/3','1/4','2/4','3/4','1/5','2/5','3/5','4/5','1/2/3','1/2/4','1/3/4','2/3/4','1/2/5','1/3/5','2/3/5','1/4/5','2/4/5','3/4/5','1/2/3/4','1/2/3/5','1/2/4/5','1/3/4/5','2/3/4/5','1/2/3/4/5']

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

while True:
    try:
        time.sleep(10/1000)

        _singles = [qutag.getCoincCounters()[0][i] for i in channels]

        _coincidences = qutag.getCoincCounters()[0][coincidence_counter_index(channels)]

        print('Singles:', _singles,'|| Coincidences:', _coincidences)

    except KeyboardInterrupt:
        print('Keyboard input interrupted counts')

        raise
