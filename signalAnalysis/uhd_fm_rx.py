#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Lesson 3 - FM Rx
# Author: John Malsbury - Ettus Research
# Description: Working with the USRP!
# Generated: Sun Oct  2 10:59:32 2016
##################################################

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

from gnuradio import analog
from gnuradio import audio
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio import uhd
from gnuradio import wxgui
from gnuradio.eng_option import eng_option
from gnuradio.fft import window
from gnuradio.filter import firdes
from gnuradio.wxgui import fftsink2
from gnuradio.wxgui import forms
from gnuradio.wxgui import scopesink2
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
import time
import wx


class uhd_fm_rx(grc_wxgui.top_block_gui):

    def __init__(self):
        grc_wxgui.top_block_gui.__init__(self, title="Lesson 3 - FM Rx")

        ##################################################
        # Variables
        ##################################################
        self.width = width = 10000
        self.trans = trans = 1500
        self.samp_rate = samp_rate = 200e03
        self.audio_samp_rate = audio_samp_rate = 96e3
        self.CenterFrequency = CenterFrequency = 430e6

        ##################################################
        # Blocks
        ##################################################
        _width_sizer = wx.BoxSizer(wx.VERTICAL)
        self._width_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_width_sizer,
        	value=self.width,
        	callback=self.set_width,
        	label='width',
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._width_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_width_sizer,
        	value=self.width,
        	callback=self.set_width,
        	minimum=2000,
        	maximum=100000,
        	num_steps=100,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.Add(_width_sizer)
        _trans_sizer = wx.BoxSizer(wx.VERTICAL)
        self._trans_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_trans_sizer,
        	value=self.trans,
        	callback=self.set_trans,
        	label="Trans",
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._trans_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_trans_sizer,
        	value=self.trans,
        	callback=self.set_trans,
        	minimum=500,
        	maximum=5000,
        	num_steps=100,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.Add(_trans_sizer)
        _CenterFrequency_sizer = wx.BoxSizer(wx.VERTICAL)
        self._CenterFrequency_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_CenterFrequency_sizer,
        	value=self.CenterFrequency,
        	callback=self.set_CenterFrequency,
        	label='CenterFrequency',
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._CenterFrequency_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_CenterFrequency_sizer,
        	value=self.CenterFrequency,
        	callback=self.set_CenterFrequency,
        	minimum=50e6,
        	maximum=500e6,
        	num_steps=100,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.Add(_CenterFrequency_sizer)
        self.wxgui_scopesink2_0 = scopesink2.scope_sink_f(
        	self.GetWin(),
        	title="Scope Plot",
        	sample_rate=samp_rate,
        	v_scale=0,
        	v_offset=0,
        	t_scale=0,
        	ac_couple=False,
        	xy_mode=False,
        	num_inputs=1,
        	trig_mode=wxgui.TRIG_MODE_AUTO,
        	y_axis_label="Counts",
        )
        self.GridAdd(self.wxgui_scopesink2_0.win, 0, 0, 2, 4)
        self.wxgui_fftsink2_0 = fftsink2.fft_sink_c(
        	self.GetWin(),
        	baseband_freq=CenterFrequency,
        	y_per_div=10,
        	y_divs=10,
        	ref_level=0,
        	ref_scale=2.0,
        	sample_rate=samp_rate,
        	fft_size=1024,
        	fft_rate=15,
        	average=True,
        	avg_alpha=None,
        	title="FFT Plot",
        	peak_hold=False,
        )
        self.GridAdd(self.wxgui_fftsink2_0.win, 0, 4, 2, 4)
        self.uhd_usrp_source_0 = uhd.usrp_source(
        	",".join(("", "")),
        	uhd.stream_args(
        		cpu_format="fc32",
        		channels=range(1),
        	),
        )
        self.uhd_usrp_source_0.set_samp_rate(samp_rate)
        self.uhd_usrp_source_0.set_center_freq(CenterFrequency, 0)
        self.uhd_usrp_source_0.set_gain(0, 0)
        self.uhd_usrp_source_0.set_antenna("TX/RX", 0)
        self.rational_resampler_xxx_0 = filter.rational_resampler_fff(
                interpolation=441,
                decimation=2000,
                taps=None,
                fractional_bw=None,
        )
        self.low_pass_filter_0 = filter.fir_filter_ccf(1, firdes.low_pass(
        	1, samp_rate, width/2, trans, firdes.WIN_HAMMING, 6.76))
        self.blocks_wavfile_sink_0 = blocks.wavfile_sink("/home/student/Desktop/dem_data.wav", 1, 44100, 16)
        self.audio_sink_0 = audio.sink(44100, "", True)
        self.analog_wfm_rcv_0 = analog.wfm_rcv(
        	quad_rate=200e03,
        	audio_decimation=1,
        )

        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_wfm_rcv_0, 0), (self.rational_resampler_xxx_0, 0))    
        self.connect((self.low_pass_filter_0, 0), (self.analog_wfm_rcv_0, 0))    
        self.connect((self.rational_resampler_xxx_0, 0), (self.audio_sink_0, 0))    
        self.connect((self.rational_resampler_xxx_0, 0), (self.blocks_wavfile_sink_0, 0))    
        self.connect((self.rational_resampler_xxx_0, 0), (self.wxgui_scopesink2_0, 0))    
        self.connect((self.uhd_usrp_source_0, 0), (self.low_pass_filter_0, 0))    
        self.connect((self.uhd_usrp_source_0, 0), (self.wxgui_fftsink2_0, 0))    

    def get_width(self):
        return self.width

    def set_width(self, width):
        self.width = width
        self._width_slider.set_value(self.width)
        self._width_text_box.set_value(self.width)
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, self.width/2, self.trans, firdes.WIN_HAMMING, 6.76))

    def get_trans(self):
        return self.trans

    def set_trans(self, trans):
        self.trans = trans
        self._trans_slider.set_value(self.trans)
        self._trans_text_box.set_value(self.trans)
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, self.width/2, self.trans, firdes.WIN_HAMMING, 6.76))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.wxgui_scopesink2_0.set_sample_rate(self.samp_rate)
        self.wxgui_fftsink2_0.set_sample_rate(self.samp_rate)
        self.uhd_usrp_source_0.set_samp_rate(self.samp_rate)
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, self.width/2, self.trans, firdes.WIN_HAMMING, 6.76))

    def get_audio_samp_rate(self):
        return self.audio_samp_rate

    def set_audio_samp_rate(self, audio_samp_rate):
        self.audio_samp_rate = audio_samp_rate

    def get_CenterFrequency(self):
        return self.CenterFrequency

    def set_CenterFrequency(self, CenterFrequency):
        self.CenterFrequency = CenterFrequency
        self._CenterFrequency_slider.set_value(self.CenterFrequency)
        self._CenterFrequency_text_box.set_value(self.CenterFrequency)
        self.wxgui_fftsink2_0.set_baseband_freq(self.CenterFrequency)
        self.uhd_usrp_source_0.set_center_freq(self.CenterFrequency, 0)


def main(top_block_cls=uhd_fm_rx, options=None):

    tb = top_block_cls()
    tb.Start(True)
    tb.Wait()


if __name__ == '__main__':
    main()
