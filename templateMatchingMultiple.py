import cv2
import numpy as np
from matplotlib import pyplot as plt
import imutils

img_rgb = cv2.imread('F:\\Work\\CvTest\\images\\smashtest.jpg')
img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
template = cv2.imread('F:\\Work\\CvTest\\%.png')
template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
template = cv2.Canny(template, 50, 200)
#template is canny edge of % png
cv2.imshow("Template", template)
#img_gray = large image that will be scaled down
resized = imutils.resize(img_gray, width = int(img_gray.shape[1] * 0.326315789474))
#resized is rescaled to fit best scale from MatchT
cv2.imshow("resized",resized)
cv2.waitKey(0)
w, h = resized.shape[::-1]
edged = cv2.Canny(resized, 50, 200)
#edged is canny version of resized large image
res = cv2.matchTemplate(edged,template, cv2.TM_CCOEFF_NORMED)
threshold = 0.7
loc = np.where( res >= threshold)
for pt in zip(*loc[::-1]):
	print("found")
	cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)

cv2.imwrite('res.png',img_rgb)