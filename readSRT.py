import datetime as dt

zero = dt.datetime.strptime('00:00:00,000', '%H:%M:%S,%f')
tier2 = ['low','medium','high']
tier3 = ['isolated','following/preceding','simultaneous']

def extract(file):
    # recording = {frequency, tier2, tier3}
    recording = {'duration':0,'frequency': 0, 'low': 0, 'medium': 0, 'high': 0, 'isolated': 0, 'following/preceding': 0,
                 'simultaneous': 0}

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
                addTier(recording, tier)

    #frequency
    frequency = calcFreq(count, end)
    recording['frequency'] = frequency
    #duration
    avg_duration = avg_duration/count
    recording['duration']=avg_duration
    return (recording)

def addTier(recording, tier):
    # add annotation data to recording data
    if(tier in tier2 or tier in tier3 ):
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
