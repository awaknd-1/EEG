

# this function creates the baseline from training spectrograms.
def baseline(train):
    # training data dimensions samples, electrodes, frequnecy, times
    length, elect, f, t = train.shape
    # chnage the time axes with electrodes
    train_baseline = train
    baseline = np.zeros((length, elect)).tolist()
    for ele in range(elect): 
        for i in range(length):
            # mean across time for the frequncy
            baseline[i][ele] = np.mean(train_baseline[i,ele,:,0:8],1) 
    baseline = np.asarray(baseline)
    baseline = np.mean(baseline,0)
    baseline = np.mean(baseline,0)
    return baseline

# performs baseline normalization of spectrograms of EEG signals  
def normalisation(train,baseline):
    corr = list()
    # dividing baseline over all time points
    for i in range(0,train.shape[-1]):
        c = (np.divide(train[:,i],baseline))
        
        corr.append(c)
        
    corrected = np.asarray(corr)
    print(corrected.shape)
    # decibel conversion
    corrected1 = np.clip(10*np.log10(corrected),-20,20)
    return corrected1

# this perform group normalisation on the traing data
def group_normalisation(train,baseline):
    # length is samples of training data
    length, elect, f, t = train.shape
    train_list1 = np.zeros((length, elect)).tolist()
    # going through all the electrodes first.
    for ele in range(0,elect):
        # going through all the samples.
        for i in range(0,length):
            data = train[i,ele,:,:]
            train_data = normalisation(data,baseline)
            train_list1[i][ele] = train_data
    train_list1 = np.asarray(train_list1)
    return train_list1


















