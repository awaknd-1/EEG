import numpy as np
import scipy as sp
from sklearn import preprocessing
from scipy import signal 
import scipy.io as sio
from scipy import stats
from math import *
import pywt


def create_wavelet(signals, n_data, srate, min_freq, max_freq, no_freq):
    frequencies = np.logspace(np.log10(min_freq),np.log10(max_freq),no_freq)
    times = np.arange(-1.5,1.5,1/srate)
    half_wavelet_size = (len(times)-1)/2
    n_wavelet = len(times)
    n_convolution = n_wavelet + n_data -1
    n_conv_pow2 = 2**(ceil(np.log2(abs(n_convolution))))
    wavelet_cycle = 4
    wavelet_x = list()
    for i in range(signals.shape[0]):
        # fft of the data
        fft_data = np.fft.fft(signals[i],n_conv_pow2)
        # initialize time frequency data
        tf_data = np.zeros([len(frequencies),n_data]).tolist()
        for fi in range(len(frequencies)):
            # create a wavelet and get its fft
            a = (np.pi*frequencies[fi]*np.sqrt(np.pi))**(-0.5)
            b = np.exp(2*1j*(np.pi)*frequencies[fi]*times)
            c = np.exp(-times**2/(2*(wavelet_cycle)/(2*(np.pi)*frequencies[fi]))**2)/frequencies[fi]
            wavelet = a*b*c
            fft_wavelet = np.fft.fft(wavelet,n_conv_pow2)
            #run convolution
            convolution_result_fft = np.fft.ifft(fft_wavelet*fft_data,n_conv_pow2)
            # note: here we remove the extra points from the power-of-2 FFT
            convolution_result_fft = convolution_result_fft[1:n_convolution]
            x = int(half_wavelet_size+1)
            convolution_result_fft = (convolution_result_fft[x: -int(half_wavelet_size)])
            tf_data[fi] = ((abs(convolution_result_fft))**2).reshape(1,-1)
        tf_data_array = np.concatenate(tf_data)
        wavelet_x.append(tf_data_array)
    return wavelet_x

#===================================================
# baseline normasation for complex morlet wavelet.
#=================================================== 
def normalisation_dwt(train,baseline):
    corr = []
    for i in range(train.shape[1]):
        c = (np.divide(train[:,i],baseline))
        corr.append(c)
    corrected = np.array(corr)
    corrected1 = np.clip((10*np.log10(corrected)),-40,40)
    return corrected1

#=================================================
# Baseline Creation.
#=================================================
# baseline start time:bt1, end time:bt2 
def baseline(train, bt1, bt2):
    basline = []
    length = len(train)
    for i in range(0,length):
        base = np.median(train[i,:,bt1:bt2],1)
        basline.append(base)
        
    baseline = np.asarray(basline)
    baseline = np.median(baseline,0)
    return baseline












