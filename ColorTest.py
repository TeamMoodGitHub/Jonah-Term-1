import cv2
import numpy as np
from matplotlib import pyplot as plt
import imutils
from PIL import Image
from PIL import Image
dataArray = ['0','1','2','3','4','5','6','7','8','9','%']


for x in dataArray:
	img = Image.open('F:\\Work\\CvTest\\Data\\'+x+'.png')
	img = img.convert("RGBA")
	datas = img.getdata()
	newData = []
	for item in datas:
		if item[3] == 0:
			newData.append((255, 255, 255, 255))
		else:
			newData.append(item)

	img.putdata(newData)
	img.save('F:\\Work\\CvTest\\newData\\'+x+'.png', "PNG")