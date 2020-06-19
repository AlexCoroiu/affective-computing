import datetime as dt

zero = dt.datetime.strptime('00:00:00,000', '%H:%M:%S,%f')
tier2 = ['low','medium','high']
tier3 = ['isolated','following/preceding','simultaneous']

#frequency, t3
f_comb_0 = {'frequency': 0, 'isolated': 0, 'following/preceding': 0, 'simultaneous': 0}

#freuqnecy, t2, t3
f_comb_1 = {'frequency': 0, 'low': 0, 'medium': 0, 'high': 0, 'isolated': 0, 'following/preceding': 0,
                 'simultaneous': 0}
#frequency, t2, t3, duration
f_comb_2 = {'duration':0, 'frequency': 0, 'low': 0, 'medium': 0, 'high': 0, 'isolated': 0, 'following/preceding': 0,
                 'simultaneous': 0}

#defaults containing each feature
#always check which default feature combination is in use to know what to add to the recording data
f_use  = [0, 1, 2]
t3_use = [0, 1, 2]
t2_use =   [1, 2]
d_use  =     [2]

feature_combinations = [f_comb_0, f_comb_1, f_comb_2]

#fc - feature combination
def extract(file, fc):
    # recording
    recording = feature_combinations[fc].copy()

    # read recording
    with open(file, 'r') as file:
        count = 0
        avg_duration = 0
        end = zero
        #read file
        while True:
            # for each annotation:
            line = file.readline()
            if not line or len(line)<2: break

            count = int(line.replace('\n',''))
            (duration, end) = calcTimes(file.readline().replace('\n', '')) #saves laughter ending time for frequency
            avg_duration = avg_duration + duration.seconds

            #read tiers
            while True:
                tier = file.readline().replace('\n', '')
                if(len(tier)<3): break
                addTier(recording, tier, fc)

    #frequency
    if(fc in f_use):
        frequency = calcFreq(count, end)
        recording['frequency'] = frequency
    #duration
    if(fc in d_use):
        avg_duration = avg_duration/count
        recording['duration']=avg_duration
    return (recording)

def addTier(recording, tier,d ):
    # add annotation data to recording data
    if(((tier in tier2) and (d in t2_use))
            or ((tier in tier3) and (d in t3_use))):
        recording[tier] = recording.get(tier) + 1

def calcFreq(count, end):
    s = (end - zero).seconds
    # frequency in 10 minutes
    f = count * 600 / s
    return f


def calcTimes(text):
    timestamps = text.split(' --> ')
    start = dt.datetime.strptime(timestamps[0], '%H:%M:%S,%f')
    end = dt.datetime.strptime(timestamps[1], '%H:%M:%S,%f')
    return (end - start, end) # last laughter ending time will be used for frequency
