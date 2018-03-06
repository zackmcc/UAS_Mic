#!/usr/bin/env python

from gnuradio import gr, audio
from gnuradio.wxgui import stdgui2,fftsink2,scopesink2
from gnuradio import analog
import wx

class dial_tone(stdgui2.std_top_block):
	def __init__(self, frame, panel, vbox, argv):
		stdgui2.std_top_block.__init__(self, frame, panel, vbox, argv)

		sampling_rate = 44100
		
		# FFT block
		fft = fftsink2.fft_sink_f(panel, title="FFT display", fft_size=512, sample_rate=sampling_rate)
		vbox.Add(fft.win,4,wx.EXPAND)

		# Scope block
		scope = scopesink2.scope_sink_f(panel, title="Oscilloscope", sample_rate=sampling_rate)
		vbox.Add(scope.win,4,wx.EXPAND)
		
		# Source block
		src = analog.sig_source_f(sampling_rate,analog.GR_SIN_WAVE,540,0.5)

		# Destination block
		audio_dst = audio.sink(sampling_rate)

		# Connection
		self.connect(src,audio_dst)
		self.connect(src,fft)
		self.connect(src,scope)
		
# main function
if __name__ == '__main__':
	app = stdgui2.stdapp(dial_tone,"Dial Tone Example with GUI")
	app.MainLoop()
