#!/usr/bin/env python

#dial_tone_example.py

#import/include blocks from the main gnu radio package
from gnuradio import gr
from gnuradio import audio
from gnuradio import analog
# create the top block
class dial_tone(gr.top_block):
      def __init__(self):
            gr.top_block.__init__(self)
            # setup some parameters
            sampling_rate = 50000
            amplitude = 0.1
            # create two signals sources
            src0 = analog.sig_source_f(sampling_rate, analog.GR_SIN_WAVE, 440, amplitude)
            src1 = analog.sig_source_f(sampling_rate, analog.GR_SIN_WAVE, 640, amplitude)

            #create a signal link
            dst = audio.sink(sampling_rate)

            #connect all the blocks together
            self.connect(src0, (dst, 0))
            self.connect(src1, (dst, 1))
            

#run the flow graph, the main function
if __name__== '__main__':
      try:
          dial_tone().run()
      except KeyboardInterrupt:
          pass

