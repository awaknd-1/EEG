

import numpy as np
from scipy.stats import kurtosis, skew, moment
import pywt
import os


def temporal_features(d1):
    # rms 
    RMS = np.sqrt(np.mean(d1**2))
    # std
    STD = np.std(d1)
    # variance
    var = np.var(d1)
    # kurtosis
    K = kurtosis(d1)
    # skewness
    Sk = skew(d1)
    # 3rd order moment
    third = moment(d1,moment=3)
    # combine them 
    features = np.array([RMS,STD])#var,K,Sk,third])
    return features
    
# calculate temporal features on 3sec signal by dividing it into four windows.
def window_features(data, end, w):
    feature_list = np.zeros((data.shape[0],data.shape[2])).tolist()
    # create 5 windows staring at 0(w1) ending at end(w5) and w is the size of window.
    w1, w2, w3, w4, w5 = windows = np.arange(0,end,w)
    for i in range(data.shape[0]):
        for j in range(data.shape[2]): 
            # calculate features from each window
            f1, f2, f3, f4 = temporal_features(data[i,w1:w2,j]), temporal_features(data[i,w2:w3,j]),temporal_features(data[i,w3:w4,j]), temporal_features(data[i,w4:w5,j]) 
            # combine the features from window
            features = np.array([f1,f2,f3,f4])
            feature_list[i][j] = features
    feature_list = np.array(feature_list)
    feature_list = np.reshape(feature_list,(feature_list.shape[0],-1))
    return feature_list
            
            
    
    
# perform decompostion of signal at different levels;
# extract energy features from each band and combine them into a vector of len 18
# it is performed on each signal seprately for each class, later combined together at the end.
def dwt_feature(dataset, waveletname):
    dwt_features = np.zeros((dataset.shape[0],dataset.shape[2])).tolist()
    for i in range(dataset.shape[0]):
        for j in range(dataset.shape[2]):
            list_coeff = pywt.wavedec(dataset[i,:,j], waveletname) # this returns a list of detailed coefficients
            # features from all decomposition levels 
            list_coeff = list_coeff[:]
            features = decomp_level_features(list_coeff)
            dwt_features[i][j] = features
    dwt_features = np.array(dwt_features)
    dwt_features = np.reshape(dwt_features,(dwt_features.shape[0],-1))

    return dwt_features

def decomp_level_features(list_coeff):
    feature_level = list()
    for i in range(len(list_coeff)):
        # calculate features
        f1 = temporal_features(list_coeff[i])
        feature_level.append(f1)
    #feature_level = np.array(feature_level)
    #feature_level = feature_level.flatten()
    return feature_level




























