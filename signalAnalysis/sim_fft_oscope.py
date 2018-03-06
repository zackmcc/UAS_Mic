#!/usr/bin/env python

#simple_fft_oscope.py

# import/include blocks from the main gnu radio package
from gnuradio import gr
from gnuradio import blocks
from gnuradio.wxgui import stdgui2, fftsink2, scopesink2
from gnuradio import analog
import wx

# create the top block
class gnuradioGUI(stdgui2.std_top_block):
    def __init__(self,frame,panel,vbox,argv):
        stdgui2.std_top_block.__init__(self,frame,panel,vbox,argv)
        
	self.sampling_rate = 441000;

	# FFT block
	fft = fftsink2.fft_sink_f(panel, title="FFT display", fft_size=512, sample_rate = self.sampling_rate)
	vbox.Add(fft.win,4,wx.EXPAND)

	# Scope block
	oscope = scopesink2.scope_sink_f(panel, title="Oscilloscope", sample_rate = self.sampling_rate)
	vbox.Add(oscope.win,4,wx.EXPAND)
	
	signal = analog.sig_source_f(self.sampling_rate,analog.GR_SAW_WAVE,10000,1000,0) 
	throttle = blocks.throttle(gr.sizeof_float,self.sampling_rate)

	self.connect(signal,throttle)
	self.connect(throttle,fft)
	self.connect(throttle,oscope)

if __name__ == '__main__':
	app = stdgui2.stdapp(gnuradioGUI,"Simple FFT & Oscope Display")
	app.MainLoop()
