???
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Uhd Am Tx
# Generated: Sun Sep 25 22:35:43 2016
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
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import uhd
from gnuradio import wxgui
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from gnuradio.wxgui import forms
from gnuradio.wxgui import scopesink2
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
import time
import wx


class uhd_am_tx(grc_wxgui.top_block_gui):

    def __init__(self):
        grc_wxgui.top_block_gui.__init__(self, title="Uhd Am Tx")

        ##################################################
        # Variables
        ##################################################
        self.Decimation = Decimation = 16
        self.samp_rate = samp_rate = 128e6/Decimation
        self.carrier_offset = carrier_offset = 0
        self.CenterFrequency = CenterFrequency = 430e6
        self.Carrier_Wave_Types = Carrier_Wave_Types = analog.GR_SIN_WAVE
        self.Amplitude = Amplitude = 1

        ##################################################
        # Blocks
        ##################################################
        self._carrier_offset_chooser = forms.radio_buttons(
        	parent=self.GetWin(),
        	value=self.carrier_offset,
        	callback=self.set_carrier_offset,
        	label='carrier_offset',
        	choices=[0,-0.5],
        	labels=['Sine','Other waves'],
        	style=wx.RA_HORIZONTAL,
        )
        self.GridAdd(self._carrier_offset_chooser, 4, 1, 1, 2)
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
        	minimum=410e6,
        	maximum=460e6,
        	num_steps=5,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.GridAdd(_CenterFrequency_sizer, 2, 0, 1, 4)
        self._Carrier_Wave_Types_chooser = forms.drop_down(
        	parent=self.GetWin(),
        	value=self.Carrier_Wave_Types,
        	callback=self.set_Carrier_Wave_Types,
        	label='Carrier_Wave_Types',
        	choices=[analog.???, analog.???, analog.???],
        	labels=['Sine', 'Square','Triangle'],
        )
        self.GridAdd(self._Carrier_Wave_Types_chooser, 4, 0, 1, 1)
        _Amplitude_sizer = wx.BoxSizer(wx.VERTICAL)
        self._Amplitude_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_Amplitude_sizer,
        	value=self.Amplitude,
        	callback=self.set_Amplitude,
        	label='Amplitude',
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._Amplitude_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_Amplitude_sizer,
        	value=self.Amplitude,
        	callback=self.set_Amplitude,
        	minimum=1,
        	maximum=1000,
        	num_steps=1,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.GridAdd(_Amplitude_sizer, 3, 0, 1, 4)
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
        self.uhd_usrp_sink_0 = uhd.usrp_sink(
        	",".join(("", "")),
        	uhd.stream_args(
        		cpu_format="fc32",
        		channels=range(1),
        	),
        )
        self.uhd_usrp_sink_0.set_samp_rate(samp_rate)
        self.uhd_usrp_sink_0.set_center_freq(CenterFrequency, 0)
        self.uhd_usrp_sink_0.set_gain(0, 0)
        self.uhd_usrp_sink_0.set_antenna("TX/RX", 0)
        self.modulation_sig = analog.sig_source_f(samp_rate, analog.GR_COS_WAVE, 500, 1, 0)
        self.carrier_wave = analog.sig_source_f(samp_rate, Carrier_Wave_Types, 10e3, 1, carrier_offset)
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_float*1, samp_rate,True)
        self.blocks_multiply_xx_0_0 = blocks.multiply_vff(1)
        self.blocks_multiply_xx_0 = blocks.multiply_vff(1)
        self.blocks_float_to_complex_0 = blocks.float_to_complex(1)
        self.blocks_add_xx_0 = blocks.add_vff(1)
        self.analog_const_source_x_1 = analog.sig_source_f(0, analog.GR_CONST_WAVE, 0, 0, Amplitude)
        self.analog_const_source_x_0_0 = analog.sig_source_f(0, analog.GR_CONST_WAVE, 0, 0, 1)
        self.amplitude_sig = analog.sig_source_f(0, analog.GR_CONST_WAVE, 0, 0, 0.5)
        self._Decimation_chooser = forms.radio_buttons(
        	parent=self.GetWin(),
        	value=self.Decimation,
        	callback=self.set_Decimation,
        	label='Decimation',
        	choices=[8, 16, 32, 64, 128 ,256],
        	labels=[],
        	style=wx.RA_HORIZONTAL,
        )
        self.GridAdd(self._Decimation_chooser, 4, 3, 1, 2)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.amplitude_sig, 0), (self.blocks_multiply_xx_0_0, 1))    
        self.connect((self.analog_const_source_x_0_0, 0), (self.blocks_add_xx_0, 1))    
        self.connect((self.analog_const_source_x_1, 0), (self.blocks_multiply_xx_0, 2))    
        self.connect((self.blocks_add_xx_0, 0), (self.blocks_multiply_xx_0, 0))    
        self.connect((self.blocks_float_to_complex_0, 0), (self.uhd_usrp_sink_0, 0))    
        self.connect((self.blocks_multiply_xx_0, 0), (self.blocks_throttle_0, 0))    
        self.connect((self.blocks_multiply_xx_0_0, 0), (self.blocks_add_xx_0, 0))    
        self.connect((self.blocks_throttle_0, 0), (self.blocks_float_to_complex_0, 0))    
        self.connect((self.blocks_throttle_0, 0), (self.wxgui_scopesink2_0, 0))    
        self.connect((self.carrier_wave, 0), (self.blocks_multiply_xx_0, 1))    
        self.connect((self.modulation_sig, 0), (self.blocks_multiply_xx_0_0, 0))    

    def get_Decimation(self):
        return self.Decimation

    def set_Decimation(self, Decimation):
        self.Decimation = Decimation
        self.set_samp_rate(128e6/self.Decimation)
        self._Decimation_chooser.set_value(self.Decimation)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.wxgui_scopesink2_0.set_sample_rate(self.samp_rate)
        self.uhd_usrp_sink_0.set_samp_rate(self.samp_rate)
        self.modulation_sig.set_sampling_freq(self.samp_rate)
        self.carrier_wave.set_sampling_freq(self.samp_rate)
        self.blocks_throttle_0.set_sample_rate(self.samp_rate)

    def get_carrier_offset(self):
        return self.carrier_offset

    def set_carrier_offset(self, carrier_offset):
        self.carrier_offset = carrier_offset
        self._carrier_offset_chooser.set_value(self.carrier_offset)
        self.carrier_wave.set_offset(self.carrier_offset)

    def get_CenterFrequency(self):
        return self.CenterFrequency

    def set_CenterFrequency(self, CenterFrequency):
        self.CenterFrequency = CenterFrequency
        self._CenterFrequency_slider.set_value(self.CenterFrequency)
        self._CenterFrequency_text_box.set_value(self.CenterFrequency)
        self.uhd_usrp_sink_0.set_center_freq(self.CenterFrequency, 0)

    def get_Carrier_Wave_Types(self):
        return self.Carrier_Wave_Types

    def set_Carrier_Wave_Types(self, Carrier_Wave_Types):
        self.Carrier_Wave_Types = Carrier_Wave_Types
        self._Carrier_Wave_Types_chooser.set_value(self.Carrier_Wave_Types)
        self.carrier_wave.set_waveform(self.Carrier_Wave_Types)

    def get_Amplitude(self):
        return self.Amplitude

    def set_Amplitude(self, Amplitude):
        self.Amplitude = Amplitude
        self._Amplitude_slider.set_value(self.Amplitude)
        self._Amplitude_text_box.set_value(self.Amplitude)
        self.analog_const_source_x_1.set_offset(self.Amplitude)


def main(top_block_cls=uhd_am_tx, options=None):

    tb = top_block_cls()
    tb.Start(True)
    tb.Wait()


if __name__ == '__main__':
    main()
