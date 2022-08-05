from pydoc import classname
import SoapySDR
from SoapySDR import * #SOAPY_SDR_ constants
import numpy as np

class device(object):
    def __init__(self, buffer_len=1024, timeout_us=5):
        # настройка SDR устройства
        self.device = SoapySDR.Device(dict(driver="sdrplay"))
        self.sample_rate = 1e6
        self.center_freq = 100e6
        self.gain = 0
        self.rx_chan = 0 # only 1 channel on RSP1A
        self.sample_buffer = self._sampleBuffer(buffer_len)
        self.timeout_us = int(5e6) 
    def _sampleBuffer(self, num_samps):
        return np.array([0]*num_samps, np.complex64)
    def startStream(self):
        self.rxStream = self.device.setupStream(SOAPY_SDR_RX, SOAPY_SDR_CF32, [self.rx_chan])
        self.device.activateStream(self.rxStream) #start streaming
    def stopStream(self):
        self.device.deactivateStream(self.rxStream) #stop streaming
        self.device.closeStream(self.rxStream)
    def readStream(self):
        #buffer = self._sampleBuffer(num_samps)
        status = self.device.readStream(self.rxStream, [self.sample_buffer], len(self.sample_buffer),timeoutUs=self.timeout_us)
        return status, self.sample_buffer
    def getInfo(self):
        return self.device.getHardwareInfo()
    def getGains(self):
        return self.device.listGains(SOAPY_SDR_RX, self.rx_chan)
    def getBandwidth(self):
        return self.device.getBandwidth(SOAPY_SDR_RX, self.rx_chan)
    def getAntennas(self):
        return self.device.listAntennas(SOAPY_SDR_RX, self.rx_chan)
    def setSampleRate(self, sample_rate):
        self.sample_rate = sample_rate
        self.device.setSampleRate(SOAPY_SDR_RX, self.rx_chan, sample_rate)
    def setCenterFreq(self, center_freq):
        self.center_freq = center_freq
        self.device.setFrequency(SOAPY_SDR_RX, self.rx_chan, center_freq)
    def setGain(self, gain):
        self.gain = gain
        self.device.setGain(SOAPY_SDR_RX, self.rx_chan, gain)   
    def setAntenna(self, antenna):
        self.antenna = antenna
        self.device.setAntenna(SOAPY_SDR_RX, self.rx_chan, antenna)
    def setBandwidth(self, bandwidth):
        self.bandwidth = bandwidth
        self.device.setBandwidth(SOAPY_SDR_RX, self.rx_chan, bandwidth) 
    def setGainMode(self, gain_mode):
        self.gain_mode = gain_mode
        self.device.setGainMode(SOAPY_SDR_RX, self.rx_chan, gain_mode)      
    def setDcOffsetMode(self, dc_offset_mode):
        self.dc_offset_mode = dc_offset_mode
        self.device.setDCOffsetMode(SOAPY_SDR_RX, self.rx_chan, dc_offset_mode)     
