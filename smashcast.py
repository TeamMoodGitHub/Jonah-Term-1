import requests
import kivy
import shutil
import cv2
import numpy as np
import tkinter as tk
import tkinter.filedialog
import re
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
kivy.require('1.10.0')
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.uix.slider import Slider
from kivy.uix.image import Image
from kivy.network.urlrequest import UrlRequest
from kivy.graphics.texture import Texture
from kivy.uix.scrollview import ScrollView
import datetime
import subprocess as sp
# With a box layout we arrange widgets in a horizontal
# or vertical box

		
class CustomField(FloatLayout):
	pass

class URLButton(Button):
	pass

class URLField(TextInput):
	pass

class TimeInput(TextInput):
	pat = re.compile('[^0-9:]')
#	patFull = re.compile('\b\d{2}[:]?\d{2}[:]?\d{2}\b')
	def insert_text(self, substring, from_undo=False):
		pat = self.pat
		s = re.sub(pat, '', substring)
		return super(TimeInput, self).insert_text(s, from_undo=from_undo)


class VodCutterLayout(BoxLayout):
	def getFile(self):
		root.withdraw()
		dirname = tkinter.filedialog.askopenfile(parent=root, initialdir="/",
                                    title='Please select a directory')
		self.changeScreen(dirname.name)
	
	def changeScreen(self, dirName):
		print(self.ids)
		self.parent.manager.get_screen("Split_Vod").displayFirstFrameFromFile(dirName)
		self.parent.manager.current = "Split_Vod"							

class VodCutterApp(App):
	def build(self):
		screen_manager = ScreenManager()
		screen_manager.add_widget(GetVod(name="Get_Vod"))
		screen_manager.add_widget(SplitVod(name="Split_Vod"))
		screen_manager.add_widget(EnterURL(name="Enter_URL"))
		return screen_manager
		
		
class GetVod(Screen):
	pass

class SplitVod(Screen):
	INPUT_VOD_PATH = None
	video = None
	length = None
	fps = None
	ext= None
	lastValue = 0
	splitCount = 1
	timeArray = []
	
	def time_to_seconds(self, t):
		hms = t.count(':')
		if hms == 2:
			h, m, s = [int(i) for i in t.split(':')]
			return 3600*h + 60*m + s
		elif hms==1:
			m, s = [int(i) for i in t.split(':')]
			return 60*m + s
		else:
			return -1
	
	def initiateVod(self):
		self.video = cv2.VideoCapture(self.INPUT_VOD_PATH)
		self.length = int(self.video.get(cv2.CAP_PROP_FRAME_COUNT))
		self.fps= self.video.get(cv2.CAP_PROP_FPS)
		self.ext= self.INPUT_VOD_PATH.split(".")[1]
		self.addSplit()


	def displayFirstFrameFromFile(self, dirName):
		print(dirName)
		print("********")
		self.INPUT_VOD_PATH = dirName
		self.initiateVod()
		self.displayFrame(0)
	
	def displayFirstFrame(self, request, frame):
		self.INPUT_VOD_PATH = request.file_path
		self.initiateVod()
		self.displayFrame(0)
		
	def displayFrameSlide(self, slideVal, override):
		if slideVal != self.lastValue or override:
			self.lastValue = slideVal
			frameNum = self.length*slideVal/100
			self.setTime(frameNum)
			self.displayFrame(frameNum)
	
	def displayFrame(self, frameNum):
		if frameNum == self.length:
			frameNum -= 1
		self.video.set(1, frameNum)
		success, frame = self.video.read()
		frame = np.rot90(np.swapaxes(frame, 0, 1))
		myTexture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='rgb')
		myTexture.blit_buffer(frame.tostring(), colorfmt='bgr', bufferfmt='ubyte')
		self.ids['FrameDisplay'].texture=myTexture
	
	def displayFrameFromTime(self,time):
		frameNum=self.time_to_seconds(time)*self.fps
		self.displayFrame(frameNum)
		self.ids['mySlide'].value=frameNum/self.length*100
		
	
	def addSplit(self):
		lay = BoxLayout(orientation='horizontal', size_hint=(None,None), size=(200,40), pos_hint={'center_x': .5})
		start = TimeInput(multiline=False,text='00:00:00')
		end = TimeInput(multiline=False,text='00:00:00')
		lay.add_widget(start)
		lay.add_widget(end)
		self.ids['output'].add_widget(lay)
		self.splitCount += 1
		self.timeArray.append([start,end])
		print(self.timeArray)
	
	
	def Submit(self):
		count = 0
		print(self.ext)
		for time in self.timeArray:
			count = 0
			startSec = self.time_to_seconds(time[0].text)
			endSec = self.time_to_seconds(time[1].text)
			if startSec != -1 and endSec != -1:
				command= ['ffmpeg',  '-ss', str(startSec), '-i', self.INPUT_VOD_PATH, '-t', str(endSec-startSec), '-c', 'copy', 'out' + str(count) + '.'+self.ext]
				count += 1
				pipe=sp.Popen(command, stdin=sp.PIPE, stderr=sp.PIPE)
				print('out' + str(count) + '.'+self.ext)
			else:
				print("Error, invalid time. Enter HH:MM:SS")

	def setTime(self, frameNum):
		secs = int(frameNum/self.fps)
		time = str(datetime.timedelta(seconds=secs)) 
		
		self.ids['timer'].text= time
	
class EnterURL(Screen):
	def download_file(self, url):
		local_filename = url.split('/' )[-1]
		# NOTE the stream=True parameter
		req = UrlRequest(url, on_progress=self.update_progress, 
					 on_success=self.changeScreen,
					 on_error=self.displayError,
                     chunk_size=1024,
                     file_path=local_filename)
		return local_filename
	def update_progress(self, request, current_size, total_size):
			self.ids['downloadBar'].value = current_size / total_size
	
	def changeScreen(self, request, result):
		self.manager.get_screen("Split_Vod").displayFirstFrame(request, 1)
		self.manager.current = "Split_Vod"
		
	def displayError(self, request, result):
		print(self.ids)

if __name__ == '__main__':

	def getFrame(video, frame):
		pass
		
	root = tk.Tk()
	blApp = VodCutterApp()
	blApp.run()


'''
def TimeToFrames(time):
	return time*fps
	
#File_Name = download_file(My_URL)
ffmpeg_extract_subclip("myFile.m3u8&s=71788c26f01a0d12bd2b08eec8196169&t=1505066937&username=GcGaming_1335150", 0, 5, targetname="test.mp4")
'''