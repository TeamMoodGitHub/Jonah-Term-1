import cv2
import numpy as np
from matplotlib import pyplot as plt
import imutils

img_rgb = cv2.imread('F:\\Work\\CvTest\\images\\smashtest2.jpg')
img_gray= cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
template = cv2.imread('F:\\Work\\CvTest\\Data\\%.png',0)
#template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
template = cv2.Canny(template, 50, 200)
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
		edged = cv2.Canny(resized, 50, 200)
		result = cv2.matchTemplate(edged, template, cv2.TM_CCOEFF)
		(_, maxVal, _, maxLoc) = cv2.minMaxLoc(result)
 
		# if we have found a new maximum correlation value, then ipdate
		# the bookkeeping variable
		if found is None or maxVal > found[0]:
			found = (maxVal, maxLoc, r)
			bScale = scale
	


#img_gray = large image that will be scaled down
resized = imutils.resize(img_gray, width = int(img_gray.shape[1] * bScale))
rgb_resize = imutils.resize(img_rgb, width = int(img_rgb.shape[1] * bScale))
edged = cv2.Canny(resized, 50, 200)
dataArray = ['0','1','2','3','4','5','6','7','8','9','%']
threshold = 0.4
for i in dataArray:
	template=cv2.imread('F:\\Work\\CvTest\\Data\\' + i + '.png',0)
	template = cv2.Canny(template, 50, 200)
	w, h = template.shape[::-1]
	res = cv2.matchTemplate(edged,template, cv2.TM_CCOEFF_NORMED)
	loc = np.where( res >= threshold)
	for pt in zip(*loc[::-1]):
		print(pt)
		cv2.rectangle(rgb_resize, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)

#resized is rescaled to fit best scale from MatchT

#edged is canny version of resized img_gray


cv2.imshow('res.png',rgb_resize)
cv2.waitKey(0)