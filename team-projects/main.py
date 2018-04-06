import tkinter as tk
import pygubu
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showerror
import wave
from pygame import mixer
from pydub import AudioSegment
from PIL import Image
from PIL import ImageTk
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
		
		mixer.init()

		builder.add_from_file('teamProj.ui')
		

		self.mainwindow = builder.get_object('main-frame')

		builder.connect_callbacks(self) # Creates the call backs for the gui operations


		self.should_play=True
		
		self.canvas = self.builder.get_object('ShowGraphView',self.mainwindow)
		self.bgPic = ImageTk.PhotoImage(Image.open("background.gif").resize((800,725)))
	
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
		self.fileName = askopenfilename(filetypes=[("MP3 files" ,"*.mp3"),("Wave files" , "*.wav")])
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
			plt.figure(1)
			plt.plot(time, channel1, linewidth=0.01, alpha=0.7, color='#ff7f00')
			plt.show()





			#code that converts to a mp3 for playback
			newFile = self.fileName.replace(".wav",".mp3")
			AudioSegment.from_wav(self.fileName).export(newFile,format="mp3")
			self.fileName = newFile
			self.loadFile()				

			



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

if __name__ == '__main__':
	root = tk.Tk()
	app = Application(root)
	root.mainloop()
