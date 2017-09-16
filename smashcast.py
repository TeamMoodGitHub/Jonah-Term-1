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
	def displayFrame(self, INPUT_VOD_PATH, frame):
		print(INPUT_VOD_PATH)
		video = cv2.VideoCapture(INPUT_VOD_PATH)
		video.set(1,frame)
		success, frame = video.read()
		
class EnterURL(Screen):
	def download_file(self, url):
		local_filename = url.split('/' )[-1]
		# NOTE the stream=True parameter
		req = UrlRequest(url, on_progress=self.update_progress, 
					 on_success=self.changeScreen,
					 on_error=self.displayError,
                     chunk_size=1024,
                     file_path=local_filename)
		INPUT_VOD_PATH = local_filename
		return local_filename
	def update_progress(self, request, current_size, total_size):
			self.ids['downloadBar'].value = current_size / total_size
	
	def changeScreen(self, request, result):
		self.manager.current = "Split_Vod"
		
	def displayError(self, request, result):
		print(self.ids)

if __name__ == '__main__':

	def getFrame(video, frame):
		pass
		
	INPUT_VOD_PATH = None
	video = None
	root = tk.Tk()
	blApp = VodCutterApp()
	blApp.run()

'''
My_URL= "https://edge.bf.hitbox.tv/downloads/voddownload.php?path=/static/videos/vods/gcgaming/77f779a9e36721d30f6379d92db40cddd3e948be-593c86ca213a7/gcgaming/6644b20a3987f58c4f50ce63a0bf1a2d.m3u8&s=71788c26f01a0d12bd2b08eec8196169&t=1505066937&username=GcGaming_1335150"
#My_URL="https://www.smashingmagazine.com/wp-content/uploads/2015/06/10-dithering-opt.jpg"
FPS = 30


def TimeToFrames(time):
	return time*fps
	
#File_Name = download_file(My_URL)
ffmpeg_extract_subclip("myFile.m3u8&s=71788c26f01a0d12bd2b08eec8196169&t=1505066937&username=GcGaming_1335150", 0, 5, targetname="test.mp4")
'''