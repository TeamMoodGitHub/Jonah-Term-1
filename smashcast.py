import requests
import kivy
import shutil
import cv2
import numpy as np
import tkinter as tk
import tkinter.filedialog
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
kivy.require('1.10.0')
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
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
# With a box layout we arrange widgets in a horizontal
# or vertical box

		
class CustomField(FloatLayout):
	pass

class URLButton(Button):
	pass

class URLField(TextInput):
	pass

class VodCutterLayout(BoxLayout):
	def getFile(self):
		root.withdraw()
		dirname = tkinter.filedialog.askopenfile(parent=root, initialdir="/",
                                    title='Please select a directory')
		self.changeScreen(dirname)
	
	def changeScreen(self, dirName):
		print(self.ids)
		self.manager.get_screen("Split_Vod").displayFirstFrameFromFile(request, 1)
		self.manager.current = "Split_Vod"							

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
	def initiateVod(self):
		self.video = cv2.VideoCapture(self.INPUT_VOD_PATH)
		self.length = int(self.video.get(cv2.CAP_PROP_FRAME_COUNT))
	def displayFirstFrameFromFile(self, dirname):
		self.INPUT_VOD_PATH = dirname
		initiateVod()
		self.displayFrame(self, 0)
	
	def displayFirstFrame(self, request, frame):
		self.INPUT_VOD_PATH = request.file_path
		self.initiateVod()
		self.displayFrame(0)
		
	def displayFrame(self, frameNum):
		frameNum = self.length*frameNum/100
		self.video.set(1, frameNum)
		success, frame = self.video.read()
		frame = np.rot90(np.swapaxes(frame, 0, 1))
		myTexture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='rgb')
		myTexture.blit_buffer(frame.tostring(), colorfmt='bgr', bufferfmt='ubyte')
		self.ids['FrameDisplay'].texture=myTexture
	
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


My_URL= "https://edge.bf.hitbox.tv/downloads/voddownload.php?path=/static/videos/vods/gcgaming/77f779a9e36721d30f6379d92db40cddd3e948be-593c86ca213a7/gcgaming/6644b20a3987f58c4f50ce63a0bf1a2d.m3u8&s=71788c26f01a0d12bd2b08eec8196169&t=1505066937&username=GcGaming_1335150"
#My_URL="https://www.smashingmagazine.com/wp-content/uploads/2015/06/10-dithering-opt.jpg"
FPS = 30

'''
def TimeToFrames(time):
	return time*fps
	
#File_Name = download_file(My_URL)
ffmpeg_extract_subclip("myFile.m3u8&s=71788c26f01a0d12bd2b08eec8196169&t=1505066937&username=GcGaming_1335150", 0, 5, targetname="test.mp4")
'''