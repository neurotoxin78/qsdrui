
import SoapySDR
from SoapySDR import * #SOAPY_SDR_ constants
import numpy as np
#import matplotlib
import matplotlib.pyplot as plt
#matplotlib.use('Qt5Agg')
sample_rate = 1e6
center_freq = 100e6
gain = 0
rx_chan = 0 # only 1 channel on RSP1A
sdr = SoapySDR.Device(dict(driver="sdrplay"))
sdr.setSampleRate(SOAPY_SDR_RX, rx_chan, sample_rate)
sdr.setFrequency(SOAPY_SDR_RX, rx_chan, center_freq)
sdr.setGainMode(SOAPY_SDR_RX, rx_chan, False) # turn off AGC
sdr.setGain(SOAPY_SDR_RX, rx_chan, gain)
rxStream = sdr.setupStream(SOAPY_SDR_RX, SOAPY_SDR_CF32, [rx_chan])
sdr.activateStream(rxStream) #start streaming
num_samps = 10000
buff = np.array([0]*num_samps, np.complex64)
#receive some samples
sr = sdr.readStream(rxStream, [buff], len(buff))
print("samples received:", sr.ret) # number of samples read or the error code
#shutdown the stream
sdr.deactivateStream(rxStream) #stop streaming
sdr.closeStream(rxStream)
print(buff[0:20])
plt.figure(0)
plt.plot(np.real(buff), '.-')
plt.plot(np.imag(buff), '.-')
plt.figure(1)
PSD = 10*np.log10(np.abs(np.fft.fftshift(np.fft.fft(buff)))**2)
f = np.linspace(-sample_rate/2, sample_rate/2, num_samps)
plt.plot(f, PSD)
plt.show()
print(dir(sdr))
print(sdr.listGains(SOAPY_SDR_RX, rx_chan))
print(sdr.getBandwidth(SOAPY_SDR_RX, rx_chan))
print(sdr.listAntennas(SOAPY_SDR_RX, rx_chan))
