import cv2
import numpy as np
from matplotlib import pyplot as plt
import imutils
from PIL import Image

'''DOUBLES RED VALUE IN IMAGES TO COVER HIGH PERCENT DARKNESS
img=Image.open('F:\\Work\\CvTest\\images\\smashtestDark.jpg')
img = img.convert("RGBA")
datas = img.getdata()
newData = []
for item in datas:
	if item[0]+item[0]<= 255:
		newData.append((item[0]+item[0],item[1],item[2],item[3]))
	else:
		newData.append((255,255,255,item[3]))
img.putdata(newData)
img.save('F:\\Work\\CvTest\\images\\testRed.png', "PNG")
'''

img_rgb = cv2.imread('F:\\Work\\CvTest\\images\\smashtestDark.jpg')
img_gray= cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
template = cv2.imread('F:\\Work\\CvTest\\blackData\\%.png',0)
#template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
template = cv2.Canny(template, 100, 200)
(tH, tW) = template.shape[:2]

#print("tH: " + str(tH) + "tW: " + str(tW))

#template is canny edge of % png
found = None;
for scale in np.linspace(0.2, 1.0, 20)[::-1]:
		# resize the image according to the scale, and keep track
		# of the ratio of the resizing
		resized = imutils.resize(img_gray, width = int(img_gray.shape[1] * scale))
		r = img_gray.shape[1] / float(resized.shape[1])
 
		# if the resized image is smaller than the template, then break
		# from the loop
		if resized.shape[0] < tH or resized.shape[1] < tW:
			break
# detect edges in the resized, grayscale image and apply template
		# matching to find the template in the image
		edged = cv2.Canny(resized, 100, 200)
		result = cv2.matchTemplate(edged, template, cv2.TM_CCOEFF)
		(_, maxVal, _, maxLoc) = cv2.minMaxLoc(result)
 
		# if we have found a new maximum correlation value, then ipdate
		# the bookkeeping variable
		if found is None or maxVal > found[0]:
			found = (maxVal, maxLoc, r)
			bScale = scale
	

print(bScale)
#img_gray = large image that will be scaled down
resized = imutils.resize(img_gray, width = int(img_gray.shape[1] * bScale))
rgb_resize = imutils.resize(img_rgb, width = int(img_rgb.shape[1] * bScale))
resized = rgb_resize[:,:,2]
resized = cv2.Canny(resized, 0, 500)
cv2.imshow("red", resized)
ret, edged = cv2.threshold(resized,80,255,cv2.THRESH_BINARY)


dataArray = ['0','1','2','3','4','5','6','7','8','9','1']
#dataArray = ['7']
threshold = 0.4
totalImages = 0
for i in dataArray:
	template=cv2.imread('F:\\Work\\CvTest\\blackData\\' + i + '.png',0)
	ret, template = cv2.threshold(template,80,255,cv2.THRESH_BINARY)
	template = cv2.Canny(template, 0, 500)
	w, h = template.shape[::-1]
	res = cv2.matchTemplate(edged,template, cv2.TM_CCOEFF_NORMED)
	cv2.imwrite('edged.png',edged)
	cv2.imwrite('template.png',template)
	loc = np.where( res >= threshold)
	unpacked = zip(*loc[::])
	sorted = []
	lastPt = 0
	for pt in unpacked:
		if pt[1] - lastPt < 15:
			unpacked.remove(pt)
		else:
			cv2.rectangle(rgb_resize, pt[::-1], (pt[1] + w, pt[0] + h), (0,0,255), 2)
			sorted.append(pt)
		lastPt = pt[1]

#resized is rescaled to fit best scale from MatchT

#edged is canny version of resized img_gray


cv2.imshow('res.png',rgb_resize)
cv2.imwrite('analyzed.png',rgb_resize)
cv2.waitKey(0)