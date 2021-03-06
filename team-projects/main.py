import tkinter as tk
import pygubu
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showerror
import wave
from myamp import amplifier
from pygame import mixer
from pydub import AudioSegment
from PIL import Image
from PIL import ImageTk
from scipy.io.wavfile import read, write
from scipy.signal.filter_design import butter
from scipy.signal import lfilter
import matplotlib.pyplot as plt
import numpy as np
import scipy.io.wavfile
import pydub

##sudo apt install python3-pil.imagetk
## sudo apt install python-imaging-tk ffmpeg
##ALso install ffmpeg

class Application:
	def __init__(self,master):
		self.builder = builder = pygubu.Builder()
		mixer.pre_init(44100, 16, 2, 4096) #frequency, size, channels, buffersize
		mixer.init()

		builder.add_from_file('teamProj.ui')
		

		self.mainwindow = builder.get_object('main-frame')

		builder.connect_callbacks(self) # Creates the call backs for the gui operations


		self.should_play=True
		
		self.canvas = self.builder.get_object('ShowGraphView',self.mainwindow)
		self.bgPic = ImageTk.PhotoImage(Image.open("backg.gif").resize((800,725)))
	
		self.canvas.create_image(0,0,image = self.bgPic,anchor = 'nw')
		


		self.lastskip=0		

		self.play_pause=False
		self.started=False
		
		
	def on_play_button_click(self):
		if not self.started:
			mixer.music.play()
			self.started = True
		else:	
			if self.play_pause:
				mixer.music.unpause()
				self.play_unpause=False
			else:
				mixer.music.pause()
				self.play_pause=True


	def on_ff_button_click(self):
		mixer.music.rewind()
		currentLengthPlayed = mixer.music.get_pos()/1000; 
		lengthToJump = 30;
		self.lastskip += lengthToJump + currentLengthPlayed;
		mixer.music.set_pos(self.lastskip);



	def on_import_click(self):
		self.fileName = askopenfilename(filetypes=[("Wav files" , "*.wav"), ("MP3 files",".mp3")])
		self.loadFile()

	def on_record_click(self):
		print("hello this wokrs")

	def on_stop_button_click(self):
		mixer.music.stop();


	def on_rewind_button_click(self):
		mixer.music.rewind()
		currentLengthPlayed = mixer.music.get_pos()/1000;
		lengthToJump = -30;

		self.lastskip = self.lastskip +  lengthToJump;
		mixer.music.set_pos(self.lastskip);

	def on_process_click(self):
	#	spf = wave.open(self.fileName,'r')
		

		#Extract Raw Audio from Wav File
	#	signal = spf.readframes(-1)
	#	signal = np.fromstring(signal, 'Int16')
	#	fs = spf.getframerate()



	#	Time=np.linspace(0, len(signal)/fs, num=len(signal))

	#	plt.figure(1)
	#	plt.title('Signal Wave...')
#		plt.plot(Time,signal)
#		plt.show()





	#	plt.figure(1)
	#	plt.title('Signal Wave...')
	#	plt.plot(signal)
	#	plt.show()
		
		





		if "mp3" not in self.fileName:
			#rate, data = wav.read(self.fileName)
			#plt.plot(data)
			#plt.show()

			rate,audData=scipy.io.wavfile.read(self.fileName)

			print(rate)
			print(audData)

			wav_length = audData.shape[0]/rate #rate in seconds
			data_type = audData.dtype #data type

			print(wav_length)
			print(data_type)
			

			channel1=audData[:,0]
			#create a time variable in seconds
			time = np.arange(0, float(audData.shape[0]), 1) / rate

			#plot amplitude (or loudness) over time
			plt.figure(2)
			plt.subplot(311)
			plt.title('Graph of ' + self.fileName)
			plt.xlabel('Time (Seconds');
			plt.ylabel('Amplitude')
			plt.plot(time, channel1, linewidth=0.02, alpha=0.7)
			

			fourier=np.fft.fft(channel1)
			plt.figure(2)
			plt.subplot(312)
			plt.plot(fourier)
			
			plt.ylabel('Amplitude')
			plt.xlabel('k')


			plt.figure(3)
			plt.title("Unfiltered")
			plt.subplot(411)
			Pxx, freqs, bins, im = plt.specgram(channel1, Fs=rate, NFFT=1024, cmap=plt.get_cmap('autumn_r'))
			cbar=plt.colorbar(im)
			plt.xlabel('Time (s)')
			plt.ylabel('Frequency (Hz)')
			cbar.set_label('Intensity dB')



			## Pydub does not
			inputAudio = AudioSegment.from_wav(self.fileName)
			print("Entered Bandpass Filter")
			lo,hi= 80,150
			sr,y=read(self.fileName)
			b,a=butter(N=2, Wn=[lo/sr, hi/sr], btype='band')
			x = lfilter(b,a,y)
			#newSong = song.low_pass_filter(3000)
			#newSong = newSong.low_pass_filter(3000)
			#newSong = newSong.low_pass_filter(3000)
			#newSong = newSong.low_pass_filter(3000)
			#newSong = newSong.low_pass_filter(5000)
			#newSong = newSong.low_pass_filter(5000)
			#newSong = newSong.apply_gain(+10.0)
			print("Exited Bandpass Filter")
			write(self.fileName + '_Filtered.wav', sr, x.astype(np.int16))
			
			#export(self.fileName + "Filtered" + ".wav",format="wav")
			self.fileName = self.fileName+"_Filtered.wav";
			#amplifier(self.fileName, self.fileName,10) 

			createGraphs(self.fileName,"Filtered");
			

			#code that converts to a mp3 for playback
			#newFile = self.fileName.replace(".wav",".mp3")
			#AudioSegment.from_wav(self.fileName).export(newFile,format="mp3")
			#self.fileName = newFile
			#newSong.export(self.fileName,format="mp3")
			self.loadFile()				
			plt.show()
			



	def loadFile(self):

		if self.fileName:
			#try:
			print(self.fileName)
			self.canRun = True
			#self.file_imported = vlc.MediaPlayer(self.fileName)
			mixer.music.load(self.fileName)
			self.started=False
			self.lastskip = 0;
			#except:
				#showerror("Cant open this type of File")


def createGraphs(filename_to_graph,title):
	print("Made it into createGraphs")
	rate,audData=scipy.io.wavfile.read(filename_to_graph)

	print(rate)
	print(audData)

	wav_length = audData.shape[0]/rate #rate in second
	data_type = audData.dtype #data type
	print(wav_length)
	print(data_type)


	channel1=audData[:,0]
	#create a time variable in seconds
	time = np.arange(0, float(audData.shape[0]), 1) / rate

	#plot amplitude (or loudness) over time
	plt.figure(1)
	plt.subplot(211)
	plt.title('Graph of ' + filename_to_graph)
	plt.xlabel('Time (Seconds');
	plt.ylabel('Amplitude')
	plt.plot(time, channel1, linewidth=0.02, alpha=0.7)


	fourier=np.fft.fft(channel1)
	plt.figure(1)
	plt.subplot(212)
	plt.plot(fourier)
	
	plt.ylabel('Amplitude')
	plt.xlabel('k')

	
	plt.figure(3)
	plt.subplot(412)
	Pxx, freqs, bins, im = plt.specgram(channel1, Fs=rate, NFFT=1024, cmap=plt.get_cmap('autumn_r'))
	cbar=plt.colorbar(im)
	plt.title("Filtered")
	plt.xlabel('Time (s)')
	plt.ylabel('Frequency (Hz)')
	cbar.set_label('Intensity dB')

	


if __name__ == '__main__':
	root = tk.Tk()
	app = Application(root)
	root.mainloop()
