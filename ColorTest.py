import cv2
import numpy as np
from matplotlib import pyplot as plt
import imutils
from PIL import Image
from PIL import Image
#dataArray = ['0','1','2','3','4','5','6','7','8','9']
dataArray=['%']

for x in dataArray:
	img = Image.open('F:\\Work\\CvTest\\Data\\'+x+'.png')
	img = img.convert("RGBA")
	datas = img.getdata()
	newData = []
	for item in datas:
		if item[3] == 0:
			newData.append((0, 0, 0, 255))
		else:
			newData.append(item)

	img.putdata(newData)
	img.save('F:\\Work\\CvTest\\cropData\\'+x+'.png', "PNG")
	imgG=cv2.imread('F:\\Work\\CvTest\\cropData\\'+x+'.png',0)
	img = cv2.imread('F:\\Work\\CvTest\\cropData\\'+x+'.png')
	w,h=imgG.shape[::-1]
	img = img[4:h-4,4:w-4] #6 for all except percent (4)
	cv2.imwrite('F:\\Work\\CvTest\\cropData\\'+x+'.png', img)
	cv2.waitKey(0)