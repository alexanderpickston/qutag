import os
import time
import QuTAG_HR
import pandas as pd

from datetime import datetime

qutag = QuTAG_HR.QuTAG()

channels = [1, 2]
qutag.setExposureTime(100)
aquisition_time = 3600
power = 1

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

for i in range(12):

    startTime = datetime.now().strftime("%F--%Hh-%Mm")

    s1 = []
    s2 = []
    cc = []
    tt = []

    for i in range(aquisition_time):
        
        _singles = [qutag.getCoincCounters()[0][i] for i in channels]
        _coincidences = qutag.getCoincCounters()[0][coincidence_counter_index(channels)]
        _time = datetime.now().time()

        s1.append(_singles[0])
        s2.append(_singles[1])
        cc.append(_coincidences)
        tt.append(_time)

        time.sleep(1)
        
        print('Time:', _time,'|| Singles:', _singles,'|| Coincidences:', _coincidences)

    df = pd.DataFrame({
        'Singles 1': s1,
        'Signles 2': s2,
        'Coincidences': cc,
        'Time': tt
    })

    cwd = os.getcwd()
    fName = "/DATA_" + str(power) + 'mW_' + startTime + ".csv"
    df.to_csv(cwd + fName)

    print('Complete')
print('Completed 12 hours')