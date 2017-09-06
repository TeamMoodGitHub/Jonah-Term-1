# -*- coding: utf-8 -*-
import numpy as np
import imutils
import cv2

INPUT_VOD_PATH = "F:\\Work\\CvTest\\smashvid2.mp4"
VOD_NAME = "smashvid2"

def get_frames():
	video = cv2.VideoCapture(INPUT_VOD_PATH)
	# forward over to the frames you want to start reading from.
	video.set(1,12200);
	success, frame = video.read()
	count = 0
	file_count = 0
	success = True
	fps = int(video.get(cv2.CAP_PROP_FPS))
	total_frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
	print("Loading video %d seconds long with FPS %d and total frame count %d " % (total_frame_count/fps, fps, total_frame_count))

	while success:

		success, frame = video.read()
		if count % 100 == 0:
			print("Currently at frame ", count)

		# i save once every 15 frames, which comes out to 2 frames per second.
		# i think anymore than 2 FPS leads to to much repeat data.
		if count % 120 == 0:
			cv2.imwrite("F:\\Work\\CvTest\\frames2\\frame_%d.jpg" %  (file_count), frame)
			file_count += 1
		count += 1

	print("Saved %d frames" % (file_count) )
	video.release()

def find_location(imloc):
	img_rgb = cv2.imread(imloc)
	template=cv2.imread("F:\\Work\\CvTest\\Jonah-Term-1\\cropData\\%.png",0)
	img_gray = img_rgb[:,:,2]
	ret, img_gray = cv2.threshold(img_gray,80,255,cv2.THRESH_BINARY)
	(tH, tW) = template.shape[:2]
	w, h = img_gray.shape[::-1]
	#template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
	template = cv2.Canny(template, 100, 400)
	img_rgb = img_rgb[int(h*.75):h,0:w]
	img_gray = img_gray[int(h*.75):h,0:w]
	percents = 0
	arr = []
	valid = False
	while percents < 2:
		found = None
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
			edged = cv2.Canny(resized, 100, 400)
			result = cv2.matchTemplate(edged, template, cv2.TM_CCORR)
			(_, maxVal, _, maxLoc) = cv2.minMaxLoc(result)
			
			# if we have found a new maximum correlation value, then ipdate
			# the bookkeeping variable
			if found is None or maxVal > found[0]:
				found = (maxVal, maxLoc, r)
				print(maxVal)
				bScale = scale
				if (maxVal >= 4300000.0):
					valid = True
				(_, maxLoc, r) = found
				print(maxLoc)
				(startX, startY) = (int(maxLoc[0] * r), int(maxLoc[1] * r))
				(endX, endY) = (int((maxLoc[0] + tW) * r), int((maxLoc[1] + tH) * r))
		if startX <= 130:
			startX= 0
		else:
			startX= startX-130
		if startY <= 30:
			startY= 0
		else:
			startY= startY-30
		arr.append(((startX, startY), (endX+10, endY+30)))
		cv2.rectangle(img_gray, (startX, startY), (endX+10, endY+30), (0, 0, 255), -2)
		percents+=1
		print(bScale)
	startX=min(arr[0][0][0],arr[1][0][0])
	startY=min(arr[0][0][1],arr[1][0][1])
	endX=max(arr[0][1][0],arr[1][1][0])
	endY=max(arr[0][1][1],arr[1][1][1])
	img_rgb = cv2.rectangle(img_rgb,(startX,startY),(endX,endY),(0,0,255),2)
	img_rgb = img_rgb[startY:endY,startX:endX]
	cv2.imshow("r",img_rgb)
	cv2.waitKey(0)
	if valid == True:
		return img_rgb
	else:
		return None


if __name__ == "__main__":
	get_frames()
	
	#img=find_location('F:\\Work\\CvTest\\Jonah-Term-1\\frames2\\frame_3.jpg')
	#if type(img) != type(None):
	#	print "found"
	
