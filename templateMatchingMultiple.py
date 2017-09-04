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
template = cv2.imread('F:\\Work\\CvTest\\cropData\\%.png',0)
(tH, tW) = template.shape[:2]
w, h = img_gray.shape[::-1]
#template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
template = cv2.Canny(template, 100, 200)
img_rgb = img_rgb[int(h*.75):h,0:w]
img_gray = img_gray[int(h*.75):h,0:w]
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
cv2.imshow("r",resized)
#resized = cv2.Canny(resized, 0, 500)
ret, edged = cv2.threshold(resized,80,255,cv2.THRESH_BINARY)
copy = edged
#edged = cv2.Canny(edged,100,200)

dataArray = ['0','1','2','3','4','5','6','7','8','9']
#dataArray = ['%']
threshold = 0.85
totalImages = 0
arranged = []
unpacked = []
for i in dataArray:
	template=cv2.imread('F:\\Work\\CvTest\\cropData\\' + i + '.png',0)
	ret, template = cv2.threshold(template,80,255,cv2.THRESH_BINARY)
	
	#template = cv2.Canny(template, 100, 200)
	w, h = template.shape[::-1]
	res = cv2.matchTemplate(edged,template, cv2.TM_CCOEFF_NORMED)
	cv2.imwrite('edged.png',edged)
	cv2.imwrite('template.png',template)
	loc = (np.where( res >= threshold), i)
	unpacked = zip(*loc[::1])
	print unpacked
	for pt in unpacked:
		arranged.append(pt)
arranged = sorted(arranged,key=lambda tup: tup[1])
lastPt = (0,0)
print arranged
print(len(arranged))
finalRects = []
while arranged:
	pt = arranged.pop(0)
	print("Comparing " + str(pt[0][1]) + " to " + str(lastPt))
	if pt[1] - lastPt[1] < 10:
		print "DISQUALIFIED"
	else:
		print "SCHWIFTY"
		finalRects.append(pt)
		cv2.rectangle(rgb_resize, pt[::-1], (pt[1] + w, pt[0] + h), (0,0,255), 2)
		lastPt = pt
print finalRects
#resized is rescaled to fit best scale from MatchT

#edged is canny version of resized img_gray


cv2.imshow('res.png',rgb_resize)
cv2.imwrite('analyzed.png',copy)
cv2.waitKey(0)